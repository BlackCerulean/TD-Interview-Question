import os
import sys
from pathlib import Path
from collections import Counter
import pytest

# Import your script (replace `app` with your actual filename, without .py)
import text_sanitize  


def test_full_local_pipeline(tmp_path, capsys):
    # --- Arrange ---
    # Create a temporary input file
    input_text = "Hello\tWorld!\nTabs\tare\there"
    source = tmp_path / "input.txt"
    source.write_text(input_text, encoding="utf-8")

    target = tmp_path / "output.txt"

    # Simulate CLI arguments
    sys.argv = [
        "text_sanitize.py",
        "--source", str(source),
        "--target", str(target),
    ]

    # --- Act ---
    text_sanitize.main()

    # Capture console output
    captured = capsys.readouterr()
    print("=== Captured Console Output ===")
    print(captured.out)   # <- will show in pytest output if run with -s

    # --- Assert ---
    # Check sanitized text is printed
    assert "hello____world!\ntabs____are____here" in captured.out.lower()

    # Check alphabet statistics are printed
    assert "h: " in captured.out
    assert "e: " in captured.out

    # Check output file exists
    assert target.exists()
    print("Output file path:", target)

    # Read back output file
    content = target.read_text(encoding="utf-8")

    # Verify structure of file
    assert "=== Sanitized Text ===" in content
    assert "=== Alphabet Statistics ===" in content
    assert "a: " in content
    assert "t: " in content