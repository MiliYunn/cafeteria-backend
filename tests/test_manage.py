from unittest.mock import patch

from manage import run_command


def test_command_interrupt_exits_cleanly(capsys):
    with patch("manage.subprocess.run", side_effect=KeyboardInterrupt):
        exit_code = run_command(["run.py"])

    captured = capsys.readouterr()
    assert exit_code == 130
    assert "Command stopped by user." in captured.err
