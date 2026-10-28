"""Unit 4 - Backtracking: exact-fit budget and interview slot scheduling."""


def sum_of_subsets(students, X, limit=5):
    """Find groups whose requested amounts add up exactly to X (with pruning)."""
    items = sorted(students, key=lambda s: s["requested"])
    out = []

    def solve(i, cur, total, remaining):
        if len(out) >= limit:
            return
        if total == X:
            out.append([s["id"] for s in cur]); return
        if i == len(items) or total + items[i]["requested"] > X or total + remaining < X:
            return                                         # prune
        cur.append(items[i])
        solve(i + 1, cur, total + items[i]["requested"], remaining - items[i]["requested"])
        cur.pop()
        solve(i + 1, cur, total, remaining - items[i]["requested"])

    solve(0, [], 0, sum(s["requested"] for s in items))
    return out


def schedule_interviews(students, m):
    """Graph colouring: students with the same preferred time clash.
    Colours = parallel panels. Returns {id: panel} or None."""
    n = len(students)
    adj = [[i != j and students[i]["slot"] == students[j]["slot"] for j in range(n)]
           for i in range(n)]
    colour = [0] * n

    def solve(v):
        if v == n:
            return True
        for c in range(1, m + 1):
            if all(not (adj[v][u] and colour[u] == c) for u in range(n)):
                colour[v] = c
                if solve(v + 1):
                    return True
                colour[v] = 0
        return False

    return {students[i]["id"]: colour[i] for i in range(n)} if solve(0) else None
