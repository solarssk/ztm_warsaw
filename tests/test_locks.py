"""The hash-locked requirement files in .github/locks agree with the pins people edit."""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
LOCKS = ROOT / ".github" / "locks"
PIN = re.compile(r"^([A-Za-z0-9_.\-]+)==(\S+)", re.MULTILINE)


def _pins(path: Path) -> dict[str, str]:
    """Return the exact `name==version` pins of a requirements file, names in lower case."""
    return {name.lower().replace("_", "-"): version for name, version in PIN.findall(path.read_text())}


def test_inputs_are_the_pins_people_edit() -> None:
    """The .in files hold exactly the pins of requirements_test.txt and .github/compat/min-ha.txt, so they cannot drift."""
    tools = _pins(ROOT / "requirements_test.txt")
    assert tools, "requirements_test.txt has no pins"
    assert _pins(LOCKS / "test.in") == tools
    assert _pins(LOCKS / "ruff.in") == {"ruff": tools["ruff"]}
    assert _pins(LOCKS / "pip-audit.in") == {"pip-audit": tools["pip-audit"]}
    assert _pins(LOCKS / "min-ha.in") == _pins(ROOT / ".github" / "compat" / "min-ha.txt")


def test_every_lock_pins_its_inputs_with_hashes() -> None:
    """Each lock contains the pin of every input and every pin in it carries a hash (what `--require-hashes` needs)."""
    for name in ("test", "ruff", "pip-audit", "min-ha", "ha-current"):
        wanted = _pins(LOCKS / f"{name}.in")
        locked = _pins(LOCKS / f"{name}.txt")
        assert wanted, name
        for package, version in wanted.items():
            assert locked.get(package) == version, f"{name}.txt does not lock {package}=={version}: regenerate it"
        text = (LOCKS / f"{name}.txt").read_text()
        assert text.count("--hash=sha256:") >= len(locked), name
