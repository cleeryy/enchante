from typer.testing import CliRunner

from enchante.cli import app

runner = CliRunner()


def test_list_modules_command():
    """Test that the list-modules command executes without errors"""
    result = runner.invoke(app, ["list-modules"])
    assert result.exit_code == 0
