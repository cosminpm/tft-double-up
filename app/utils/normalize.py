import re


def normalize_champ_name(name: str) -> str:
    """Normalize champion name to lower case and without spaces."""
    cleaned = re.sub(r"[^A-Za-z\s]", "", name)
    return re.sub(r"^(.)(.*)", lambda m: m.group(1) + m.group(2).lower(), cleaned)
