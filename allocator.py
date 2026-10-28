"""Unit 3 - Dynamic Programming allocation."""


def knapsack(students, W):
    """0/1 Knapsack. weight = requested amount, value = priority score. O(nW)."""
    n = len(students)
    c = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = students[i-1]["requested"], students[i-1]["score"]
        for j in range(W + 1):
            c[i][j] = c[i-1][j]
            if w <= j:
                c[i][j] = max(c[i][j], v + c[i-1][j-w])
    chosen, j = [], W
    for i in range(n, 0, -1):               # traceback
        if c[i][j] != c[i-1][j]:
            chosen.append(students[i-1])
            j -= students[i-1]["requested"]
    return c[n][W], chosen[::-1]


def greedy(students, W):
    """Baseline: best score-per-amount first."""
    total, chosen = 0, []
    for s in sorted(students, key=lambda s: s["score"] / s["requested"], reverse=True):
        if s["requested"] <= W:
            W -= s["requested"]; total += s["score"]; chosen.append(s)
    return total, chosen


def category_allocation(students, W):
    """Multistage DP: split fund W among categories (stages).
    benefit[cat][k] = best knapsack value inside that category with k units."""
    cats = sorted({s["category"] for s in students})
    benefit = {c: [knapsack([s for s in students if s["category"] == c], k)[0]
                   for k in range(W + 1)] for c in cats}
    dp = [[0] * (W + 1) for _ in range(len(cats) + 1)]
    pick = [[0] * (W + 1) for _ in range(len(cats) + 1)]
    for i, c in enumerate(cats, 1):
        for j in range(W + 1):
            for k in range(j + 1):
                v = benefit[c][k] + dp[i-1][j-k]
                if v > dp[i][j]:
                    dp[i][j], pick[i][j] = v, k
    split, j = {}, W
    for i in range(len(cats), 0, -1):
        split[cats[i-1]] = pick[i][j]
        j -= pick[i][j]
    return dp[len(cats)][W], split
