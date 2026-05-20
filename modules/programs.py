"""Programs module — curated rotating list of summer schools, insight events
and sponsored programs for a French Grade-12 (Terminale) student interested in
finance, astronomy or coding/technology.

The list is hand-curated and rotates 5 entries daily based on day-of-year, so
the user sees a different selection each morning. Verify deadlines on each
program's official site before applying.
"""
from __future__ import annotations

from datetime import date
from typing import Any


PROGRAMS: list[dict[str, str]] = [
    # ---------- FINANCE ----------
    {
        "field": "Finance",
        "name": "LSE Summer School — Pre-University",
        "url": "https://www.lse.ac.uk/study-at-lse/Summer-Schools/LSE-Summer-School",
        "desc": "Two-week London School of Economics programme in finance/economics with university-level teaching. Open to high-schoolers; partial scholarships available.",
    },
    {
        "field": "Finance",
        "name": "Yale Young Global Scholars — Politics, Law & Economics",
        "url": "https://globalscholars.yale.edu/",
        "desc": "Two-week residential at Yale exploring economics, law and global affairs. Full financial aid for admitted students who need it.",
    },
    {
        "field": "Finance",
        "name": "Wharton Global Youth — Future of the Business World",
        "url": "https://globalyouth.wharton.upenn.edu/",
        "desc": "Wharton's pre-college business and finance programme (in-person or online). Strong fit for future quants and entrepreneurs.",
    },
    {
        "field": "Finance",
        "name": "J.P. Morgan Spring Insight Programme (EMEA)",
        "url": "https://careers.jpmorgan.com/global/en/students/programs/spring-week-emea",
        "desc": "Multi-day spring insight week in Paris/London for early-year students; a great first look inside investment banking. Applications open in autumn.",
    },
    {
        "field": "Finance",
        "name": "Goldman Sachs Possibilities Summit",
        "url": "https://www.goldmansachs.com/careers/students/programs/index.html",
        "desc": "One-day sponsored event introducing finance careers to underrepresented and rising university students. Travel often covered.",
    },
    {
        "field": "Finance",
        "name": "Morgan Stanley Step In, Step Up, Step Forward",
        "url": "https://www.morganstanley.com/people-opportunities/students-graduates",
        "desc": "Free three-day insight programme aimed at school leavers and first-year students in Europe; exposure to trading, banking and research.",
    },
    {
        "field": "Finance",
        "name": "HEC Paris Summer School",
        "url": "https://www.hec.edu/en/summer-school",
        "desc": "Two-week summer programme on the HEC Jouy-en-Josas campus in finance, entrepreneurship or management — a top French business school.",
    },
    {
        "field": "Finance",
        "name": "ESSEC Global BBA Summer Programme",
        "url": "https://www.essec.edu/en/program/global-bba/summer-programs/",
        "desc": "ESSEC's pre-bachelor summer programme around business, finance and innovation in Cergy or Singapore — taught in English.",
    },
    {
        "field": "Finance",
        "name": "BlackRock Future Discovery Series",
        "url": "https://careers.blackrock.com/students/",
        "desc": "Free virtual events for high-school and first-year students introducing asset management and ESG investing. Multiple sessions per year.",
    },
    {
        "field": "Finance",
        "name": "UBS Apprentice Insight Days",
        "url": "https://www.ubs.com/global/en/careers/students/insights-and-discovery.html",
        "desc": "Sponsored insight days across Europe focused on wealth management and investment banking. Open to senior secondary students.",
    },

    # ---------- ASTRONOMY / SPACE ----------
    {
        "field": "Astronomy",
        "name": "Summer Science Program (SSP) — Astrophysics",
        "url": "https://summerscience.org/",
        "desc": "Six-week residential research programme where teams compute the orbit of a near-Earth asteroid from telescope data. Need-based aid covers 100% of cost.",
    },
    {
        "field": "Astronomy",
        "name": "International Astronomical Youth Camp (IAYC)",
        "url": "https://www.iayc.org/",
        "desc": "Three-week summer camp in Europe with small research groups on observational and theoretical astronomy. Open to 16–24 year olds.",
    },
    {
        "field": "Astronomy",
        "name": "ESA Academy — Summer Workshops",
        "url": "https://www.esa.int/Education/ESA_Academy",
        "desc": "European Space Agency runs short residential training weeks at ESEC-Galaxia in Belgium on satellites, mission design and space science. Travel reimbursed.",
    },
    {
        "field": "Astronomy",
        "name": "Observatoire de Paris — Ateliers lycéens",
        "url": "https://www.obspm.fr/-public-scolaire-.html",
        "desc": "Free workshops and tours at Meudon and Paris observatories aimed at lycée students. Excellent for Terminale spé maths/physique projects.",
    },
    {
        "field": "Astronomy",
        "name": "Royal Observatory Greenwich — Astronomy Schools",
        "url": "https://www.rmg.co.uk/royal-observatory",
        "desc": "Short residential astronomy programmes in London for 14–18 year olds, including telescope observing and astrophysics lectures.",
    },
    {
        "field": "Astronomy",
        "name": "CNES — Cités de l'espace / Stages lycéens",
        "url": "https://cnes.fr/fr/jeunes",
        "desc": "The French space agency runs internships, conferences and the C'Space rocketry week for French students passionate about space.",
    },
    {
        "field": "Astronomy",
        "name": "International Olympiad on Astronomy and Astrophysics (IOAA)",
        "url": "https://www.ioaastrophysics.org/",
        "desc": "World-level competition in astrophysics; the French team is selected via national olympiad training camps run by INRAP & SAF.",
    },
    {
        "field": "Astronomy",
        "name": "ESO Astronomy Camp",
        "url": "https://www.esoastronomycamp.com/",
        "desc": "Week-long winter camp in the Italian Alps run by ESO with observatory nights, lectures and astrophotography. ~50 places worldwide.",
    },
    {
        "field": "Astronomy",
        "name": "NASA Space Apps Challenge",
        "url": "https://www.spaceappschallenge.org/",
        "desc": "Free 48-hour global hackathon with NASA datasets, including a Paris node. No experience needed; great for cross-over coding + space projects.",
    },
    {
        "field": "Astronomy",
        "name": "Olympiades de Physique France",
        "url": "https://odpf.org/",
        "desc": "French national physics competition where lycée teams present an experimental project — an astrophysics topic is a strong angle.",
    },

    # ---------- CODING / TECHNOLOGY ----------
    {
        "field": "Coding / Tech",
        "name": "MIT Beaver Works Summer Institute (BWSI)",
        "url": "https://beaverworks.ll.mit.edu/CMS/bw/bwsi",
        "desc": "Free four-week MIT programme on AI, autonomous vehicles, cybersecurity, etc. Highly selective; international students accepted in some tracks.",
    },
    {
        "field": "Coding / Tech",
        "name": "École 42 — La Piscine",
        "url": "https://42.fr/en/the-program/piscine/",
        "desc": "Free, intense four-week coding bootcamp in Paris that doubles as the admission test for 42's tuition-free CS school. Open from age 18.",
    },
    {
        "field": "Coding / Tech",
        "name": "École Polytechnique — Bachelor Summer School",
        "url": "https://programmes.polytechnique.edu/en/bachelor/bachelor-summer-school",
        "desc": "Three-week residential summer programme on the X campus covering CS, maths and data science for international high-school students.",
    },
    {
        "field": "Coding / Tech",
        "name": "Stanford Pre-Collegiate Summer Institutes — CS tracks",
        "url": "https://spcs.stanford.edu/programs/stanford-pre-collegiate-summer-institutes",
        "desc": "Two-week intensive in machine learning, algorithms or cybersecurity at Stanford. Need-based financial aid is available.",
    },
    {
        "field": "Coding / Tech",
        "name": "Inspirit AI Scholars Program",
        "url": "https://www.inspiritai.com/",
        "desc": "Online programme run by MIT/Stanford AI grad students where high-schoolers build a real AI project. Some scholarships available.",
    },
    {
        "field": "Coding / Tech",
        "name": "Apple Swift Student Challenge (WWDC)",
        "url": "https://developer.apple.com/wwdc/swift-student-challenge/",
        "desc": "Annual worldwide challenge: build a Swift Playground; winners get a free trip to WWDC at Apple Park. Open to students 13+.",
    },
    {
        "field": "Coding / Tech",
        "name": "Google Code-in / Summer of Code (CS50x for younger)",
        "url": "https://summerofcode.withgoogle.com/",
        "desc": "Paid Google programme to contribute to open-source projects over the summer (18+). For 17 and under: try CS50x or Hack Club.",
    },
    {
        "field": "Coding / Tech",
        "name": "Microsoft DigiGirlz / Code; Without Barriers",
        "url": "https://www.microsoft.com/en-us/diversity/programs/digigirlz",
        "desc": "Free Microsoft events introducing girls in high school to tech careers, including coding workshops and mentor sessions in EMEA.",
    },
    {
        "field": "Coding / Tech",
        "name": "AI4ALL Summer Program",
        "url": "https://ai-4-all.org/",
        "desc": "Free summer AI research programme at universities like Stanford, Princeton and BU, focused on underrepresented students in AI.",
    },
    {
        "field": "Coding / Tech",
        "name": "Hack Club + Github YC Workshops",
        "url": "https://hackclub.com/",
        "desc": "Free year-round programming events, sponsored coding weekends, scholarships and hackathons run by Hack Club worldwide.",
    },
    {
        "field": "Coding / Tech",
        "name": "Concours Alkindi & Algorea",
        "url": "https://concours-alkindi.fr/",
        "desc": "Free French national competitions in cryptography (Alkindi) and algorithms (Algorea) — perfect Terminale projects and Parcoursup boosters.",
    },
]


def get_daily_programs(today: date | None = None, n: int = 5) -> list[dict[str, str]]:
    """Return `n` programs for today, deterministically rotating through PROGRAMS."""
    if today is None:
        today = date.today()
    day_of_year = today.timetuple().tm_yday
    start = (day_of_year * n) % len(PROGRAMS)
    picks = []
    for i in range(n):
        picks.append(PROGRAMS[(start + i) % len(PROGRAMS)])
    return picks


def format_programs_html(picks: list[dict[str, str]]) -> str:
    rows = []
    for p in picks:
        rows.append(
            f"""
            <li style="margin-bottom:10px">
              <strong>[{p['field']}] <a href="{p['url']}">{p['name']}</a></strong><br>
              <span style="color:#444">{p['desc']}</span>
            </li>
            """
        )
    return "<ol>" + "\n".join(rows) + "</ol>"


if __name__ == "__main__":
    from pprint import pprint
    pprint(get_daily_programs())
