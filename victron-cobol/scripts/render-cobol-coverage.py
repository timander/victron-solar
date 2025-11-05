#!/usr/bin/env python3
"""Render COBOL coverage report with COBOL source highlighting."""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
from typing import Dict, List, Optional

LINE_COMMENT_RE = re.compile(r"/\* Line:\s*(\d+)\s*:.*:\s*(.+?)\s*\*/")
BRANCH_TAKEN_RE = re.compile(r"branch\s+(\d+)\s+taken\s+(\d+)%")
BRANCH_NEVER_RE = re.compile(r"branch\s+(\d+)\s+never executed")

CoverageMap = Dict[int, Dict[str, object]]


def parse_gcov(gcov_path: pathlib.Path, source_basename: str) -> CoverageMap:
    results: CoverageMap = {}
    current_line: Optional[int] = None
    counts: List[int] = []
    branches: Dict[int, Dict[str, object]] = {}

    def flush() -> None:
        nonlocal current_line, counts, branches
        if current_line is None:
            return
        entry = results.setdefault(
            current_line,
            {"hits": None, "executable": False, "branches": {}},
        )
        if counts:
            entry["executable"] = True
            hit_value = max(counts)
            if entry["hits"] is None or hit_value > int(entry["hits"]):
                entry["hits"] = hit_value
        elif entry["hits"] is None:
            entry["hits"] = None
        for branch_id, info in branches.items():
            existing = entry.setdefault("branches", {}).get(branch_id)
            if existing is None or info["pct"] > existing["pct"]:
                entry["branches"][branch_id] = info
        current_line = None
        counts = []
        branches = {}

    with gcov_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            raw_line = raw_line.rstrip("\n")

            match = LINE_COMMENT_RE.search(raw_line)
            if match:
                flush()
                source_name = pathlib.Path(match.group(2)).name
                if source_name != source_basename:
                    current_line = None
                    continue
                current_line = int(match.group(1))
                counts = []
                branches = {}
                continue

            if current_line is None:
                continue

            stripped = raw_line.strip()
            if not stripped:
                continue

            branch_taken = BRANCH_TAKEN_RE.search(stripped)
            if branch_taken:
                branch_id = int(branch_taken.group(1))
                pct = int(branch_taken.group(2))
                branches[branch_id] = {"pct": pct, "detail": stripped}
                continue

            branch_never = BRANCH_NEVER_RE.search(stripped)
            if branch_never:
                branch_id = int(branch_never.group(1))
                branches[branch_id] = {"pct": 0, "detail": stripped}
                continue

            if stripped.startswith("call") or stripped.startswith("function"):
                continue

            parts = raw_line.split(":", 2)
            if len(parts) < 3:
                continue

            count_field = parts[0].strip()
            line_field = parts[1].strip()
            if not line_field.isdigit() or not count_field:
                continue

            if count_field in {"-"}:
                continue
            if count_field in {"#####", "====="}:
                counts.append(0)
                continue
            try:
                counts.append(int(count_field))
            except ValueError:
                continue

    flush()
    return results


def compute_summary(coverage: CoverageMap) -> Dict[str, Dict[str, int]]:
    line_totals = {"total": 0, "covered": 0}
    branch_totals = {"total": 0, "covered": 0}

    for entry in coverage.values():
        if not entry.get("executable"):
            continue
        line_totals["total"] += 1
        hits = entry.get("hits")
        if isinstance(hits, int) and hits > 0:
            line_totals["covered"] += 1
        for info in entry.get("branches", {}).values():
            branch_totals["total"] += 1
            if info.get("pct", 0) > 0:
                branch_totals["covered"] += 1

    return {"lines": line_totals, "branches": branch_totals}


def percent(covered: int, total: int) -> str:
    if total == 0:
        return "100.0%"
    return f"{(covered / total) * 100:.1f}%"


def build_json_payload(coverage: CoverageMap, cobol_lines: List[str]) -> Dict[str, object]:
    summary = compute_summary(coverage)
    payload: Dict[str, object] = {
        "summary": {
            "lines": {
                "covered": summary["lines"]["covered"],
                "total": summary["lines"]["total"],
                "percent": percent(summary["lines"]["covered"], summary["lines"]["total"]),
            },
            "branches": {
                "covered": summary["branches"]["covered"],
                "total": summary["branches"]["total"],
                "percent": percent(summary["branches"]["covered"], summary["branches"]["total"]),
            },
        },
        "lines": [],
    }

    for idx, text in enumerate(cobol_lines, start=1):
        entry = coverage.get(idx, {"hits": None, "executable": False, "branches": {}})
        executable = bool(entry.get("executable"))
        hits = entry.get("hits")
        branches = entry.get("branches", {})
        branch_items = []
        for branch_id in sorted(branches):
            info = branches[branch_id]
            branch_items.append({
                "id": branch_id,
                "pct": info.get("pct", 0),
                "detail": info.get("detail", ""),
            })
        if not executable:
            status = "noncode"
        elif isinstance(hits, int) and hits > 0:
            if branch_items and any(item["pct"] == 0 for item in branch_items):
                status = "partial"
            else:
                status = "covered"
        else:
            status = "missed"
        payload["lines"].append({
            "line": idx,
            "hits": hits,
            "executable": executable,
            "status": status,
            "branches": branch_items,
            "source": text,
        })
    return payload


def render_html(coverage: CoverageMap, cobol_lines: List[str], title: str) -> str:
    summary = compute_summary(coverage)
    line_totals = summary["lines"]
    branch_totals = summary["branches"]
    line_percent = percent(line_totals["covered"], line_totals["total"])
    branch_percent = percent(branch_totals["covered"], branch_totals["total"])

    rows: List[str] = []
    for idx, text in enumerate(cobol_lines, start=1):
        entry = coverage.get(idx, {"hits": None, "executable": False, "branches": {}})
        executable = bool(entry.get("executable"))
        hits = entry.get("hits")
        branches = entry.get("branches", {})
        branch_total = len(branches)
        branch_covered = sum(1 for info in branches.values() if info.get("pct", 0) > 0)

        if not executable:
            css_class = "nonexec"
            hits_display = "-"
        elif isinstance(hits, int) and hits > 0:
            css_class = "partial" if branch_total and branch_covered < branch_total else "covered"
            hits_display = str(hits)
        else:
            css_class = "missed"
            hits_display = "0"

        if branch_total:
            branch_info = f"{branch_covered}/{branch_total}"
            branch_tooltip = " | ".join(
                info.get("detail", "") for _, info in sorted(branches.items())
            )
            branch_tooltip = html.escape(branch_tooltip)
            branch_cell = (
                f'<td class="branch-cell" title="{branch_tooltip}">{branch_info}</td>'
            )
        else:
            branch_cell = '<td class="branch-cell">-</td>'

        rows.append(
            "<tr class=\"{cls}\"><td class=\"line-no\">{line}</td>"
            "<td class=\"hit-count\">{hits}</td>{branch}<td class=\"code\">{code}</td></tr>".format(
                cls=css_class,
                line=idx,
                hits=hits_display,
                branch=branch_cell,
                code=html.escape(text),
            )
        )

    rows_html = "\n    ".join(rows)

    style = """
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; margin: 1.5rem; }
h1 { margin: 0 0 0.25rem; font-size: 1.75rem; }
.summary { margin: 1rem 0 1.5rem; display: flex; gap: 1.5rem; flex-wrap: wrap; }
.summary-card { background: #1e293b; padding: 0.75rem 1.25rem; border-radius: 0.75rem; box-shadow: 0 8px 20px rgba(15, 23, 42, 0.45); }
.summary-card h2 { margin: 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; }
.summary-card p { margin: 0.45rem 0 0; font-size: 1.25rem; font-weight: 600; }
table { width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 0.85rem; }
th, td { padding: 0.3rem 0.5rem; text-align: left; border-bottom: 1px solid rgba(148, 163, 184, 0.12); }
th { position: sticky; top: 0; background: #0b1120; z-index: 2; }
.line-no { width: 3.5rem; color: #94a3b8; }
.hit-count { width: 4.5rem; text-align: right; }
.branch-cell { width: 6rem; }
.code { white-space: pre; color: #e2e8f0; }
.covered { background: rgba(34, 197, 94, 0.16); }
.missed { background: rgba(248, 113, 113, 0.22); }
.partial { background: rgba(250, 204, 21, 0.20); }
.nonexec { background: rgba(148, 163, 184, 0.08); color: #94a3b8; }
.legend { margin-top: 1.25rem; display: flex; gap: 1rem; font-size: 0.8rem; color: #cbd5f5; }
.legend span { display: inline-flex; align-items: center; gap: 0.35rem; }
.legend .swatch { width: 0.9rem; height: 0.9rem; border-radius: 0.25rem; display: inline-block; }
.legend .covered { background: #22c55e; }
.legend .partial { background: #facc15; }
.legend .missed { background: #f87171; }
.legend .nonexec { background: #94a3b8; }
    """

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset=\"UTF-8\">
<title>{html.escape(title)}</title>
<style>{style}</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
<div class=\"summary\">
  <div class=\"summary-card\">
    <h2>Line Coverage</h2>
    <p>{line_percent} ({line_totals['covered']} / {line_totals['total']})</p>
  </div>
  <div class=\"summary-card\">
    <h2>Branch Coverage</h2>
    <p>{branch_percent} ({branch_totals['covered']} / {branch_totals['total']})</p>
  </div>
</div>
<table>
  <thead>
    <tr><th class=\"line-no\">Line</th><th class=\"hit-count\">Hits</th><th class=\"branch-cell\">Branches</th><th>Code</th></tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>
<div class=\"legend\">
  <span><span class=\"swatch covered\"></span>Covered</span>
  <span><span class=\"swatch partial\"></span>Partial Branch</span>
  <span><span class=\"swatch missed\"></span>Missed</span>
  <span><span class=\"swatch nonexec\"></span>Non-executable</span>
</div>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Render COBOL coverage HTML from gcov output")
    parser.add_argument("--gcov", required=True, type=pathlib.Path, help="Path to SOLARCOST.c.gcov")
    parser.add_argument("--source", required=True, type=pathlib.Path, help="Path to COBOL source file")
    parser.add_argument("--output", required=True, type=pathlib.Path, help="Output HTML report path")
    parser.add_argument("--json", type=pathlib.Path, help="Optional JSON output path")
    parser.add_argument("--title", default="COBOL Coverage", help="Report title")
    args = parser.parse_args()

    coverage = parse_gcov(args.gcov, args.source.name)
    cobol_lines = args.source.read_text(encoding="utf-8").splitlines()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    html_report = render_html(coverage, cobol_lines, args.title)
    args.output.write_text(html_report, encoding="utf-8")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        payload = build_json_payload(coverage, cobol_lines)
        args.json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    summary = compute_summary(coverage)
    line_totals = summary["lines"]
    branch_totals = summary["branches"]
    print(
        "Line coverage: "
        f"{line_totals['covered']} / {line_totals['total']} "
        f"({percent(line_totals['covered'], line_totals['total'])})"
    )
    print(
        "Branch coverage: "
        f"{branch_totals['covered']} / {branch_totals['total']} "
        f"({percent(branch_totals['covered'], branch_totals['total'])})"
    )


if __name__ == "__main__":
    main()
