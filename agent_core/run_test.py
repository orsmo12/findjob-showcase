"""
run_test.py — Full pipeline: Job Finder → Scout → Mentor → Daily Assistant
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()
from agent_core.graph import career_graph

MY_RESUME = """
Or Smolarchik — Givatayim, Israel

Third-year Computer Science student at HIT, with strong analytical thinking,
quick learning ability, and a passion for software development.
Seeking a junior developer role to apply academic knowledge and grow professionally.

Technical Skills:
Languages: Python, JavaScript, Java, C++
Web Technologies: React, Vite, Socket.IO, HTML, CSS
Libraries & Frameworks: NumPy, OpenCV, TensorFlow, Keras
Tools & Platforms: Git, VS Code, Linux, SQL, Google Colab

Projects:
- AI Smart Crosswalk: Full-stack AI system with React, Vite, Socket.IO.
- Computer Vision & Deep Learning: OpenCV, TensorFlow, Keras image processing.
- Robotics Integration (Blackjack): Python + Dynamixel motors, image recognition.
- Lifeboard (In Progress): Autonomous AI agents platform using LangGraph and FastAPI.

Military: Logistics Officer & Deputy Company Commander, IDF 2016–2021.
Languages: Hebrew (Native), English (Excellent)
"""

initial_state = {
    "search_query": "Junior Python Developer",
    "location": "Tel Aviv",
    "resume_text": MY_RESUME,
    "max_results": 8,
    "raw_jobs": [], "filtered_jobs": [],
    "company_signals": [], "skill_gaps": [],
    "daily_summary": "",
    "iteration": 0, "should_refine": False,
    "refined_query": None, "messages": [],
}

print("=" * 55)
print("  Life Board — Full Agent Pipeline")
print("  Finder → Scout → Mentor → Daily Assistant")
print("=" * 55)

result = career_graph.invoke(initial_state)

print("\n" + "=" * 55)
print(f"DONE — {result['iteration']} round(s) | {len(result['raw_jobs'])} jobs | {len(result['filtered_jobs'])} matches")

print("\n── Top Matches ──")
for job in sorted(result['filtered_jobs'], key=lambda j: j['ats_score'], reverse=True)[:5]:
    print(f"  [{job['ats_score']:3d}%] {job['title']} @ {job['company']}  ({job['source']})")
    print(f"         {job['url'][:70]}")

if result.get("company_signals"):
    print("\n── Company Intelligence ──")
    for s in sorted(result["company_signals"], key=lambda x: x.get("fit_score", 0), reverse=True):
        p = s.get("apply_priority", "?").upper()
        fit = s.get("fit_score", "?")
        stage = s.get("company_stage", "?")
        jr = "✓ junior" if s.get("junior_friendly") else "✗ senior"
        print(f"  [{p:6s}] {s['company']} | fit={fit}% | {stage} | {jr}")
        if s.get("culture_signal"):
            print(f"           → {s['culture_signal']}")

if result.get("skill_gaps"):
    print("\n── Skill Gaps ──")
    for g in result["skill_gaps"]:
        print(f"  [{g.get('priority','?').upper():6s}] {g['skill']}: {g['reason']}")

if result.get("daily_summary"):
    print("\n" + "━" * 55)
    print("  📋 MORNING BRIEFING")
    print("━" * 55)
    print(result["daily_summary"])
    print("━" * 55)

print("\n── Log ──")
for msg in result['messages']:
    print(f"  • {msg}")
