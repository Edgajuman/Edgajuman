"""Refresh public repository metadata as dependency-free, theme-aware SVG cards."""
import argparse
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "Edgajuman"


def repositories():
    result = []
    for page in range(1, 11):
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "Edgajuman-profile", "X-GitHub-Api-Version": "2022-11-28"}
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = Request(f"https://api.github.com/users/{USERNAME}/repos?type=owner&per_page=100&sort=updated&page={page}", headers=headers)
        with urlopen(request, timeout=30) as response:
            content = response.read(2_000_001)
        if len(content) > 2_000_000:
            raise ValueError("Repository response exceeds size limit")
        chunk = json.loads(content)
        if not isinstance(chunk, list):
            raise ValueError("Unexpected repository response")
        result.extend(chunk)
        if len(chunk) < 100:
            return result
    raise ValueError("Repository pagination limit reached")


def graphic(repos, light):
    repos = [r for r in repos if not r.get("private") and r.get("name", "").casefold() != USERNAME.casefold()]
    own = sum(not r.get("fork", False) for r in repos)
    languages = sorted({r["language"] for r in repos if r.get("language")})
    recent = sorted(repos, key=lambda r: r.get("updated_at", ""), reverse=True)[:3]
    bg, border, text, muted, accent = ("#f6f8fa", "#dce3ec", "#17243b", "#596b82", "#1462c4") if light else ("#0b1320", "#26364c", "#eff5ff", "#94a8c2", "#58ded5")
    date = datetime.now(timezone.utc).strftime("%d.%m.%Y")
    values = [(len(repos), "REPOSITORIOS PÚBLICOS"), (own, "PROYECTOS PROPIOS"), (len(repos)-own, "FORKS"), (len(languages), "LENGUAJES PRINCIPALES")]
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 240" role="img" aria-labelledby="title desc">
<title id="title">Mapa de proyectos públicos de Edgajuman</title><desc id="desc">{len(repos)} repositorios públicos, {own} propios, {len(repos)-own} forks y {len(languages)} lenguajes principales. Actualizado el {date}.</desc>
<rect x="1" y="1" width="1198" height="238" rx="14" fill="{bg}" stroke="{border}"/>
<g font-family="Segoe UI,Arial,sans-serif"><text x="29" y="34" fill="{accent}" font-size="13" font-weight="600" letter-spacing="2">MAPA PÚBLICO / EDGAJUMAN</text><text x="1168" y="34" text-anchor="end" fill="{muted}" font-size="13">{date}</text>''']
    for index, (value, label) in enumerate(values):
        x = 29 + index * 297
        parts.append(f'<text x="{x}" y="109" fill="{text}" font-size="48" font-weight="600">{value}</text><text x="{x}" y="140" fill="{muted}" font-size="12" letter-spacing="1">{escape(label)}</text>')
    names = "   /   ".join(r.get("name", "") for r in recent)
    parts.append(f'<path d="M29 167H1170" stroke="{border}"/><text x="29" y="195" fill="{muted}" font-size="13">ACTUALIZADOS RECIENTEMENTE</text><text x="29" y="219" fill="{text}" font-size="15">{escape(names)}</text></g></svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, help="Use a local public-repository snapshot for offline generation")
    args = parser.parse_args()
    repos = json.loads(args.snapshot.read_text(encoding="utf-8-sig")) if args.snapshot else repositories()
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    for light in (False, True):
        output = assets / f"activity-{'light' if light else 'dark'}.svg"
        output.write_text(graphic(repos, light), encoding="utf-8")
    print("Updated public repository cards; profile repository excluded")
