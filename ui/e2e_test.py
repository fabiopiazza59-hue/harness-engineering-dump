#!/usr/bin/env python3
"""End-to-end browser test of the UI: upload a paper + CSV, build the task, run the harness,
judge, save a verdict, and screenshot each stage. Requires the server on localhost:8765.

    python ui/e2e_test.py [paper.pdf data.csv] [--shots DIR]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paper", nargs="?", default=str(ROOT / "evalkit/truth/dev/dev_002_ttest/paper.pdf"))
    ap.add_argument("data", nargs="?", default=str(ROOT / "tasks/dev/dev_002_ttest/data.csv"))
    ap.add_argument("--shots", default=str(ROOT / "runs" / "ui_shots"))
    ap.add_argument("--url", default="http://127.0.0.1:8765")
    a = ap.parse_args()
    shots = Path(a.shots)
    shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium" if Path("/opt/pw-browsers/chromium").is_file() else None)
        page = b.new_page(viewport={"width": 1360, "height": 900})
        page.goto(a.url)
        page.wait_for_selector("#tasks-table tbody tr, #tasks-table")
        page.set_input_files("#file-paper", a.paper)
        page.set_input_files("#file-data", a.data)
        page.fill("#up-name", "e2e_glucose_trial")
        page.screenshot(path=str(shots / "01_drop.png"))
        page.click("#btn-upload")
        page.wait_for_function("document.querySelector('#up-status').textContent.includes('uploaded')", timeout=30000)
        page.wait_for_selector("[data-build]", timeout=10000)
        page.screenshot(path=str(shots / "02_uploaded.png"))
        page.click("[data-build]")
        print("building task with the LLM task builder ...", flush=True)
        page.wait_for_selector("[data-validate]", timeout=400000)
        page.screenshot(path=str(shots / "03_task_built.png"))
        page.click("[data-validate]")
        page.wait_for_timeout(500)
        val = page.input_value("#val-task")
        print("validate task:", val, flush=True)
        page.click("#btn-run")
        print("running harness ...", flush=True)
        page.wait_for_function("document.querySelector('#run-status').textContent.startsWith('done') || document.querySelector('#run-status').textContent.startsWith('error')", timeout=1800000)
        page.wait_for_timeout(800)
        print("run status:", page.text_content("#run-status"), flush=True)
        page.screenshot(path=str(shots / "04_run_result.png"), full_page=True)
        page.click("#btn-judge")
        print("judging ...", flush=True)
        page.wait_for_function("document.querySelector('#judge-status').textContent.startsWith('done') || document.querySelector('#judge-status').textContent.startsWith('error')", timeout=600000)
        page.wait_for_timeout(500)
        # human verdict on first two claims
        for i in range(2):  # the table re-renders after each click, so re-query every time
            page.locator(".verdict button[data-v=correct]").nth(i).click()
            page.wait_for_timeout(150)
        page.click("#btn-save-verdict")
        page.wait_for_timeout(600)
        page.screenshot(path=str(shots / "05_judged.png"), full_page=True)
        print("score:", page.text_content("#k-score"), "raw:", page.text_content("#k-raw"), "prov:", page.text_content("#k-prov"),
              "judge:", page.text_content("#k-judge"), "human:", page.text_content("#k-human"), flush=True)
        page.click("nav button[data-tab=versions]")
        page.wait_for_timeout(800)
        page.screenshot(path=str(shots / "06_versions.png"), full_page=True)
        page.click("nav button[data-tab=runs]")
        page.wait_for_timeout(800)
        page.screenshot(path=str(shots / "07_runs.png"), full_page=True)
        b.close()
    print("screenshots in", shots)


if __name__ == "__main__":
    sys.exit(main())
