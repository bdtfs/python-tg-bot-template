import ast
from pathlib import Path

ROOT = Path(__file__).parents[2]
APP = ROOT / "app"


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def test_use_cases_and_models_are_transport_independent() -> None:
    forbidden_imports = (
        "telegram",
        "app.clients",
        "app.config",
        "app.container",
        "app.handlers",
        "app.runtime",
    )
    forbidden_semantics = (
        "<b>",
        "acknowledgement",
        "callback_data",
        "edit_message",
        "parse_mode",
    )

    paths = [APP / "model.py", *(APP / "usecases").rglob("*.py")]
    for path in paths:
        modules = imported_modules(path)
        source = path.read_text().lower()
        assert not any(module.startswith(forbidden_imports) for module in modules), path
        assert not any(term in source for term in forbidden_semantics), path


def test_handlers_depend_on_ports_not_concrete_adapters() -> None:
    for path in (APP / "handlers").glob("*.py"):
        if path.stem == "__init__":
            continue
        modules = imported_modules(path)
        assert not any(module.startswith("app.clients") for module in modules), path
        assert not any(module.startswith("app.container") for module in modules), path


def test_clients_do_not_import_handlers_or_use_cases() -> None:
    for path in (APP / "clients").rglob("*.py"):
        modules = imported_modules(path)
        assert not any(module.startswith("app.handlers") for module in modules), path
        assert not any(module.startswith("app.usecases") for module in modules), path


def test_only_container_imports_concrete_clients() -> None:
    offenders: list[Path] = []
    for path in APP.rglob("*.py"):
        if path == APP / "container.py" or (APP / "clients") in path.parents:
            continue
        if any(module.startswith("app.clients") for module in imported_modules(path)):
            offenders.append(path)

    assert not offenders


def test_only_container_constructs_application_services() -> None:
    service_classes: set[str] = set()
    for path in [*(APP / "clients").glob("*.py"), *(APP / "usecases").glob("*.py")]:
        tree = ast.parse(path.read_text(), filename=str(path))
        service_classes.update(node.name for node in tree.body if isinstance(node, ast.ClassDef))

    offenders: list[tuple[Path, str]] = []
    for path in APP.rglob("*.py"):
        if (
            path == APP / "container.py"
            or (APP / "clients") in path.parents
            or (APP / "usecases") in path.parents
        ):
            continue
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in service_classes:
                    offenders.append((path, node.func.id))

    assert not offenders


def test_container_build_is_straight_line_composition() -> None:
    path = APP / "container.py"
    tree = ast.parse(path.read_text(), filename=str(path))
    build = next(
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "build"
    )
    forbidden = (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.Match, ast.Lambda)

    assert not any(isinstance(node, forbidden) for node in ast.walk(build))
    assert len(build.body) <= 32
