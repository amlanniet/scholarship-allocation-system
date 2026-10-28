"""Intelligent Scholarship Allocation System - DSA-II (CCSE0301) PBL
Author: Amlan Chakrabarty

Usage:  python main.py [--file data/applicants.csv] [--budget 20] [--panels 3]
Budget is in units (1 unit = Rs 10,000).
"""
import argparse
from ranking import load_applicants, rank_applicants
from duplicates import find_duplicates, remove_duplicates
from allocator import knapsack, greedy, category_allocation
from backtracking import sum_of_subsets, schedule_interviews


def show(title):
    print(f"\n{'=' * 8} {title} {'=' * 8}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", default="data/applicants.csv")
    p.add_argument("--budget", type=int, default=20)
    p.add_argument("--panels", type=int, default=3)
    args = p.parse_args()

    applicants = load_applicants(args.file)
    print(f"Loaded {len(applicants)} applications | Budget: {args.budget} units "
          f"(Rs {args.budget * 10000:,})")

    show("1. Duplicate check (LCS)")
    dups = find_duplicates(applicants)
    for a, b, r in dups:
        print(f"  {a} and {b} look duplicate (similarity {r}) -> {b} removed")
    applicants = remove_duplicates(applicants, dups)
    if not dups:
        print("  No duplicates found")

    show("2. Eligibility + ranking (heap)")
    ranked, rejected = rank_applicants(applicants)
    for a in rejected:
        print(f"  REJECTED {a['id']} {a['name']} (cgpa {a['cgpa']}, attendance {a['attendance']}%)")
    print(f"  {'Rank':<5}{'ID':<5}{'Name':<15}{'Category':<9}{'Score':<6}Requested")
    for i, a in enumerate(ranked, 1):
        print(f"  {i:<5}{a['id']:<5}{a['name']:<15}{a['category']:<9}{a['score']:<6}{a['requested']}")

    show("3. Optimal selection (0/1 Knapsack DP)")
    best, chosen = knapsack(ranked, args.budget)
    used = sum(s["requested"] for s in chosen)
    for s in chosen:
        print(f"  {s['id']} {s['name']:<15} amount={s['requested']}  score={s['score']}")
    print(f"  Total score: {best} | Budget used: {used}/{args.budget}")
    g, gc = greedy(ranked, args.budget)
    print(f"  Greedy baseline score: {g} -> DP is better by {best - g}")

    show("4. Category-wise fund split (multistage DP)")
    total, split = category_allocation(ranked, args.budget)
    for cat, units in split.items():
        print(f"  {cat:<8}: {units} units (Rs {units * 10000:,})")
    print(f"  Max total benefit: {total}")

    show("5. Exact-fit groups (Sum of Subsets, backtracking)")
    groups = sum_of_subsets(ranked, args.budget)
    if groups:
        for g_ in groups:
            print("  ", g_)
    else:
        print("  No group uses the budget exactly")

    show("6. Interview scheduling (Graph Colouring, backtracking)")
    selected = chosen
    plan = schedule_interviews(selected, args.panels)
    if plan:
        for s in selected:
            print(f"  {s['id']} {s['name']:<15} preferred time {s['slot']} -> Panel {plan[s['id']]}")
    else:
        print(f"  Cannot schedule with {args.panels} panels; increase --panels")


if __name__ == "__main__":
    main()
