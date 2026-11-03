"""Paleta compartilhada: tema nativo alimenta CSS e gráficos sem duplicação."""
from pathlib import Path
import tomllib
from types import MappingProxyType

_theme = tomllib.loads((Path(__file__).resolve().parents[2] / ".streamlit/config.toml").read_text("utf-8"))["theme"]
COLORS = MappingProxyType({
    "ink": _theme["textColor"], "accent": _theme["primaryColor"],
    "ground": _theme["backgroundColor"], "border": _theme["borderColor"],
    "navy": _theme["sidebar"]["backgroundColor"], "surface": "#FFFFFF",
    "muted": "#4B6074", "tint": "#E0F5F3", "success": "#076B50",
    "success_bg": "#E2F4EB", "warning": "#854A08", "warning_bg": "#FFF3DB",
    "danger": "#AC2430", "danger_bg": "#FDECEF", "focus": "#006970",
})


def stylesheet() -> str:
    tokens = ";".join(f"--gh-{name.replace('_', '-')}: {value}" for name, value in COLORS.items())
    css = (Path(__file__).parent / "styles.css").read_text("utf-8")
    return f"<style>:root {{{tokens}}}\n{css}</style>"
