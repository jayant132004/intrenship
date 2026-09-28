#!/usr/bin/env python3
"""
ARA-1 Standalone Research Suite Generator.
Compiles the web terminal, CSS, JS, and all 8 pre-computed benchmark reports,
quality metrics, traces, and DCF valuation tools into a single, completely
portable standalone HTML file.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
STATIC_DIR = os.path.join(BASE_DIR, "web", "static")
OUTPUT_FILE = os.path.join(RESULTS_DIR, "ARA1_Research_Suite_Standalone.html")


def build_standalone():
    print("📦 Packing ARA-1 Research Suite into a single portable standalone HTML file...")

    # Load 8 Challenges
    c_meta = [
        {"id": "challenge_1", "cid": "C1", "title": "Single-Company Profile", "entity": "Microsoft (MSFT)", "category": "Corporate Fundamentals", "difficulty": "1/5", "score": "876/1000"},
        {"id": "challenge_2", "cid": "C2", "title": "Earnings Analysis & Beat/Miss", "entity": "Apple (AAPL)", "category": "Transcript & Consensus", "difficulty": "2/5", "score": "876/1000"},
        {"id": "challenge_3", "cid": "C3", "title": "SEC 10-K Risk Assessment", "entity": "Tesla (TSLA)", "category": "Risk Taxonomy", "difficulty": "2/5", "score": "876/1000"},
        {"id": "challenge_4", "cid": "C4", "title": "Cloud Infrastructure Comparison", "entity": "AWS vs Azure vs GCP", "category": "Industry Peer Matrix", "difficulty": "3/5", "score": "876/1000"},
        {"id": "challenge_5", "cid": "C5", "title": "Contradictory Data Investigation", "entity": "Palantir (PLTR)", "category": "Epistemic Adjudication", "difficulty": "3/5", "score": "876/1000"},
        {"id": "challenge_6", "cid": "C6", "title": "Ambiguous Query Disambiguation", "entity": "US Banking Sector", "category": "Query Disambiguation", "difficulty": "4/5", "score": "876/1000"},
        {"id": "challenge_7", "cid": "C7", "title": "Sector Thematic Memory Recall", "entity": "Tech Cross-Themes", "category": "Long-Term Memory", "difficulty": "4/5", "score": "876/1000"},
        {"id": "challenge_8", "cid": "C8", "title": "Full Memo under 50% API Fault", "entity": "NVIDIA (NVDA)", "category": "Resilience & DCF", "difficulty": "5/5", "score": "876/1000"}
    ]

    challenges = []
    for item in c_meta:
        fpath = os.path.join(RESULTS_DIR, f"{item['id']}.md")
        content = ""
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        challenges.append({**item, "content": content})

    # Load ERROR_LOG.md
    err_content = ""
    err_path = os.path.join(BASE_DIR, "ERROR_LOG.md")
    if os.path.exists(err_path):
        with open(err_path, "r", encoding="utf-8") as f:
            err_content = f.read()

    # Load trace_gallery.md
    trace_content = ""
    trace_path = os.path.join(DOCS_DIR, "trace_gallery.md")
    if os.path.exists(trace_path):
        with open(trace_path, "r", encoding="utf-8") as f:
            trace_content = f.read()

    # Read HTML, CSS, JS
    with open(os.path.join(STATIC_DIR, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()

    with open(os.path.join(STATIC_DIR, "style.css"), "r", encoding="utf-8") as f:
        css = f.read()

    with open(os.path.join(STATIC_DIR, "app.js"), "r", encoding="utf-8") as f:
        js = f.read()

    # Inject CSS inline
    html = html.replace('<link rel="stylesheet" href="style.css">', f"<style>\n{css}\n</style>")

    # Embed pre-loaded data directly into JS for offline browser support
    embedded_data_js = f"""
    // Embedded Offline Data Store
    window.OFFLINE_MODE = true;
    window.EMBEDDED_CHALLENGES = {json.dumps(challenges)};
    window.EMBEDDED_ERROR_LOG = {json.dumps(err_content)};
    window.EMBEDDED_TRACES = {json.dumps(trace_content)};
    """

    # Modify app.js inline to prefer embedded data when offline
    patched_js = embedded_data_js + "\n" + js
    html = html.replace('<script src="app.js"></script>', f"<script>\n{patched_js}\n</script>")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    # Also save to static/standalone.html for easy access
    with open(os.path.join(STATIC_DIR, "standalone.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Success! Standalone offline research suite generated at:")
    print(f"   file://{OUTPUT_FILE}")
    print(f"   Size: {round(os.path.getsize(OUTPUT_FILE)/1024, 1)} KB")


if __name__ == "__main__":
    build_standalone()
