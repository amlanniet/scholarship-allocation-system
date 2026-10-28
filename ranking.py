"""Unit 1 - eligibility check and heap-based ranking."""
import csv, heapq

MIN_ATTENDANCE = 75
MIN_CGPA = 7.0


def load_applicants(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["cgpa"] = float(r["cgpa"])
        r["family_income"] = int(r["family_income"])
        r["attendance"] = int(r["attendance"])
        r["requested"] = int(r["requested"])      # in units (1 unit = Rs 10,000)
        r["slot"] = int(r["slot"])
    return rows


def priority_score(a):
    """Integer score 0-100: 50% academics, 30% financial need, 20% attendance."""
    need = max(0.0, 1 - a["family_income"] / 800000)
    return round(50 * a["cgpa"] / 10 + 30 * need + 20 * a["attendance"] / 100)


def is_eligible(a):
    return a["attendance"] >= MIN_ATTENDANCE and a["cgpa"] >= MIN_CGPA


def rank_applicants(applicants):
    """Return (ranked eligible list, rejected list). Max-heap on score."""
    eligible, rejected = [], []
    for a in applicants:
        a["score"] = priority_score(a)
        (eligible if is_eligible(a) else rejected).append(a)
    heap = [(-a["score"], a["id"], a) for a in eligible]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[2] for _ in range(len(heap))], rejected
