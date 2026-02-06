import pytest

from helloworld.main import say_hello


def test_say_hello(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that say_hello prints the correct message."""
    say_hello()
    captured = capsys.readouterr()
    assert captured.out == "hello world\n"
