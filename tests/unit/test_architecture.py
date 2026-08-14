import ast
from pathlib import Path


ROOT = Path(__file__).parents[2]


def test_entrypoint_is_thin() -> None:
    source = (ROOT / "bot" / "__main__.py").read_text()
    assert len(source.splitlines()) <= 5
    assert "container" not in source
    assert "telegram" not in source


def test_usecases_do_not_import_transport() -> None:
    for path in (ROOT / "bot" / "usecases").glob("*.py"):
        tree = ast.parse(path.read_text())
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        for node in imports:
            module = getattr(node, "module", "") or ""
            assert not module.startswith("telegram")
            assert not module.startswith("bot.handlers")


def test_handler_modules_are_operation_scoped() -> None:
    handlers = {path.stem for path in (ROOT / "bot" / "handlers").glob("*.py")}
    assert {"start", "help", "ping", "messages", "callbacks"} <= handlers
