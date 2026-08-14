import ast
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[2]
APP = ROOT / "app"


def test_canonical_python_service_shape() -> None:
    required = {
        ROOT / "__main__.py",
        ROOT / "architecture.toml",
        APP / "config.py",
        APP / "container.py",
        APP / "runtime.py",
        APP / "model.py",
        APP / "clients" / "telegram.py",
        ROOT / "tests" / "unit",
        ROOT / "tests" / "integration",
    }

    missing = {path for path in required if not path.exists()}

    assert not (ROOT / "bot").exists(), "implementation ownership must be app/, not bot/"
    assert not missing, f"canonical Python service paths are missing: {sorted(missing)}"


def test_root_entrypoint_is_lifecycle_only() -> None:
    source = (ROOT / "__main__.py").read_text()

    assert source == "from app.runtime import main\n\nmain()\n"


def test_no_root_level_implementation_modules() -> None:
    root_modules = {path.name for path in ROOT.glob("*.py")}

    assert root_modules == {"__main__.py"}


def test_storage_is_absent_until_persistence_is_real() -> None:
    contract = tomllib.loads((ROOT / "architecture.toml").read_text())

    assert contract["service"]["persistence"] is False
    assert not (APP / "storage").exists(), (
        "this template has no persistence behavior; add an actually used adapter, "
        "its use-case port, "
        "and integration coverage before setting persistence=true"
    )


def test_each_operation_and_use_case_has_an_owning_unit_test() -> None:
    handlers = {
        path.stem
        for path in (APP / "handlers").glob("*.py")
        if path.stem != "__init__" and not path.stem.startswith("_")
    }
    use_cases = {
        path.stem
        for path in (APP / "usecases").glob("*.py")
        if path.stem != "__init__" and not path.stem.startswith("_")
    }
    handler_tests = {
        path.stem.removeprefix("test_")
        for path in (ROOT / "tests" / "unit" / "handlers").glob("test_*.py")
    }
    use_case_tests = {
        path.stem.removeprefix("test_")
        for path in (ROOT / "tests" / "unit" / "usecases").glob("test_*.py")
    }

    assert handlers
    assert use_cases
    assert handlers == handler_tests
    assert use_cases == use_case_tests


def test_container_owns_every_handler_and_use_case_registration() -> None:
    container_tree = ast.parse((APP / "container.py").read_text())
    handler_imports: set[str] = set()
    use_case_imports: set[str] = set()
    for node in ast.walk(container_tree):
        if not isinstance(node, ast.ImportFrom) or node.module is None:
            continue
        if node.module == "app.handlers":
            handler_imports.update(alias.name for alias in node.names)
        elif node.module.startswith("app.usecases."):
            use_case_imports.add(node.module.rsplit(".", maxsplit=1)[-1])

    handlers = {
        path.stem
        for path in (APP / "handlers").glob("*.py")
        if path.stem != "__init__" and not path.stem.startswith("_")
    }
    use_cases = {
        path.stem
        for path in (APP / "usecases").glob("*.py")
        if path.stem != "__init__" and not path.stem.startswith("_")
    }

    assert handlers == handler_imports
    assert use_cases == use_case_imports


def test_each_handler_module_exposes_one_operation_factory() -> None:
    for path in (APP / "handlers").glob("*.py"):
        if path.stem == "__init__" or path.stem.startswith("_"):
            continue
        tree = ast.parse(path.read_text(), filename=str(path))
        public_functions = [
            node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and not node.name.startswith("_")
        ]
        assert [node.name for node in public_functions] == ["build_handler"], path


def test_integration_suite_is_not_empty() -> None:
    assert list((ROOT / "tests" / "integration").glob("test_*.py"))
