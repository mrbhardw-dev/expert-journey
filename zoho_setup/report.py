"""Collects what a run did, prints it, and writes a GitHub Actions job summary."""
import os


class Report:
    def __init__(self, dry_run):
        self.dry_run = dry_run
        self.rows = []  # (area, name, outcome, detail)
        self.manual_steps = []

    def add(self, area, name, outcome, detail=""):
        self.rows.append((area, name, outcome, detail))
        suffix = f" ({detail})" if detail else ""
        print(f"  [{outcome}] {area}: {name}{suffix}")

    @property
    def failed(self):
        return [r for r in self.rows if r[2] in ("failed", "blocked")]

    def summary_markdown(self):
        mode = "DRY RUN: nothing was changed" if self.dry_run else "APPLIED"
        lines = [f"## Zoho setup ({mode})", "", "| Area | Item | Outcome | Detail |", "|---|---|---|---|"]
        for area, name, outcome, detail in self.rows:
            lines.append(f"| {area} | {name} | {outcome} | {detail} |")
        if self.manual_steps:
            lines += ["", "### Manual steps (no Zoho API for these)", ""]
            lines += [f"- [ ] {s}" for s in self.manual_steps]
        return "\n".join(lines) + "\n"

    def finish(self):
        counts = {}
        for r in self.rows:
            counts[r[2]] = counts.get(r[2], 0) + 1
        print("\nSummary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        if self.manual_steps:
            print("\nManual steps still to do:")
            for s in self.manual_steps:
                print(f"  - {s}")
        path = os.environ.get("GITHUB_STEP_SUMMARY")
        if path:
            with open(path, "a", encoding="utf-8") as f:
                f.write(self.summary_markdown())
        return 1 if self.failed else 0
