import sys
from datetime import datetime
from sar_system.agents.scout import run_scout
from sar_system.agents.auditor import run_auditor
from sar_system.agents.reporter import run_reporter


def run_pipeline() -> str | None:
    """
    Main orchestrator — runs the full SAR pipeline:
    Scout → Auditor → Reporter
    """
    print("\n" + "="*50)
    print("🚀 SAR Pipeline starting...")
    print(f"   {datetime.now().strftime('%B %d, %Y — %H:%M')}")
    print("="*50 + "\n")

    # ─── STEP 1: SCOUT ────────────────────────────────
    raw_jobs = run_scout()

    if not raw_jobs:
        print("⚠️  Scout found no new jobs today. Exiting.")
        return None

    # ─── STEP 2: AUDITOR ──────────────────────────────
    scored_jobs = run_auditor(raw_jobs)

    if not scored_jobs:
        print("⚠️  Auditor found no relevant jobs today. Exiting.")
        return None

    # ─── STEP 3: REPORTER ─────────────────────────────
    report_path = run_reporter(scored_jobs)

    # ─── DONE ─────────────────────────────────────────
    print("="*50)
    print("✅ SAR Pipeline completed successfully!")
    print(f"   📊 Report saved to: {report_path}")
    print(f"   🔍 {len(raw_jobs)} jobs found by Scout")
    print(f"   ⚖️  {len(scored_jobs)} jobs passed Auditor")
    print("="*50 + "\n")

    return report_path

if __name__ == "__main__":
    run_pipeline()