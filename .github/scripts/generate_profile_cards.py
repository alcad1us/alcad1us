"""Generate dependency-free Matrix-themed SVG cards from GitHub REST data."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import UTC, datetime
from html import escape
from pathlib import Path
from typing import Any


API_ROOT = "https://api.github.com"
BACKGROUND = "#050805"
BORDER = "#123d22"
PRIMARY = "#00ff41"
ACCENT = "#39ff14"
TEXT = "#c9ffd5"
MUTED = "#6b8e73"
BAR_COLORS = ("#00ff41", "#00c853", "#00a82d", "#008f11", "#006b2b", "#004d20")


def api_get(path: str, token: str | None) -> Any:
    request = urllib.request.Request(
        f"{API_ROOT}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-card-generator",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API returned {error.code} for {path}: {body}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"GitHub API request failed for {path}: {error.reason}") from error


def fetch_repositories(username: str, token: str | None) -> list[dict[str, Any]]:
    repositories: list[dict[str, Any]] = []
    for page in range(1, 11):
        query = urllib.parse.urlencode(
            {"per_page": 100, "page": page, "type": "owner", "sort": "updated"}
        )
        batch = api_get(f"/users/{urllib.parse.quote(username)}/repos?{query}", token)
        repositories.extend(batch)
        if len(batch) < 100:
            break
    return repositories


def aggregate_languages(language_maps: list[dict[str, int]]) -> Counter[str]:
    totals: Counter[str] = Counter()
    for language_map in language_maps:
        totals.update(language_map)
    return totals


def account_age_years(created_at: str, now: datetime | None = None) -> int:
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    current = now or datetime.now(UTC)
    years = current.year - created.year
    if (current.month, current.day) < (created.month, created.day):
        years -= 1
    return max(years, 0)


def svg_shell(width: int, height: int, title: str, body: str) -> str:
    safe_title = escape(title)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" role="img" aria-label="{safe_title}">
  <title>{safe_title}</title>
  <rect width="100%" height="100%" rx="10" fill="{BACKGROUND}" stroke="{BORDER}"/>
  <style>
    .title {{ fill: {PRIMARY}; font: 700 18px 'Segoe UI', sans-serif; }}
    .label {{ fill: {MUTED}; font: 12px 'Segoe UI', sans-serif; }}
    .value {{ fill: {TEXT}; font: 700 22px 'Cascadia Code', monospace; }}
    .mono {{ fill: {TEXT}; font: 600 12px 'Cascadia Code', monospace; }}
  </style>
  <text x="22" y="30" class="title">{safe_title}</text>
  {body}
</svg>
"""


def render_stats(profile: dict[str, Any], repositories: list[dict[str, Any]]) -> str:
    original = [repo for repo in repositories if not repo.get("fork")]
    values = (
        ("REPOSITORIES", profile.get("public_repos", len(repositories))),
        ("TOTAL STARS", sum(repo.get("stargazers_count", 0) for repo in original)),
        ("FOLLOWERS", profile.get("followers", 0)),
        ("TOTAL FORKS", sum(repo.get("forks_count", 0) for repo in original)),
    )
    blocks = []
    for index, (label, value) in enumerate(values):
        x = 22 + (index % 2) * 210
        y = 72 + (index // 2) * 65
        blocks.append(
            f'<text x="{x}" y="{y}" class="value">{escape(str(value))}</text>'
            f'<text x="{x}" y="{y + 20}" class="label">{escape(label)}</text>'
        )
    return svg_shell(440, 170, "GitHub Stats", "\n  ".join(blocks))


def render_languages(languages: Counter[str], limit: int = 6) -> str:
    top = languages.most_common(limit)
    total = sum(value for _, value in top) or 1
    if not top:
        top = [("No language data", 1)]
    rows = []
    for index, (name, value) in enumerate(top):
        y = 58 + index * 18
        percentage = value / total * 100
        bar_width = max(2, round(percentage * 2.3))
        color = BAR_COLORS[index % len(BAR_COLORS)]
        rows.append(
            f'<text x="22" y="{y}" class="mono">{escape(name)}</text>'
            f'<rect x="145" y="{y - 10}" width="{bar_width}" height="8" rx="4" fill="{color}"/>'
            f'<text x="392" y="{y}" class="label" text-anchor="end">{percentage:.1f}%</text>'
        )
    return svg_shell(440, 170, "Top Languages", "\n  ".join(rows))


def render_highlights(profile: dict[str, Any], repositories: list[dict[str, Any]]) -> str:
    original = [repo for repo in repositories if not repo.get("fork")]
    values = (
        ("PROJECTS", len(original)),
        ("STARS EARNED", sum(repo.get("stargazers_count", 0) for repo in original)),
        ("FOLLOWERS", profile.get("followers", 0)),
        ("YEARS ON GITHUB", account_age_years(profile["created_at"])),
    )
    blocks = []
    for index, (label, value) in enumerate(values):
        x = 112 + index * 222
        blocks.append(
            f'<circle cx="{x}" cy="76" r="38" fill="none" stroke="{BAR_COLORS[index]}" stroke-width="3"/>'
            f'<text x="{x}" y="82" class="value" text-anchor="middle">{escape(str(value))}</text>'
            f'<text x="{x}" y="132" class="label" text-anchor="middle">{escape(label)}</text>'
        )
    return svg_shell(890, 150, "GitHub Highlights", "\n  ".join(blocks))


def write_cards(username: str, output_dir: Path, token: str | None) -> None:
    profile = api_get(f"/users/{urllib.parse.quote(username)}", token)
    repositories = fetch_repositories(username, token)
    language_maps = []
    for repository in repositories:
        if repository.get("fork") or repository.get("archived"):
            continue
        language_maps.append(api_get(f"/repos/{repository['full_name']}/languages", token))

    output_dir.mkdir(parents=True, exist_ok=True)
    cards = {
        "github-stats.svg": render_stats(profile, repositories),
        "top-languages.svg": render_languages(aggregate_languages(language_maps)),
        "github-highlights.svg": render_highlights(profile, repositories),
    }
    for filename, contents in cards.items():
        (output_dir / filename).write_text(contents, encoding="utf-8", newline="\n")
        print(f"Generated {output_dir / filename}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    write_cards(args.username, args.output_dir, os.getenv("GITHUB_TOKEN"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
