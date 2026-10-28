"""Unit 3 - LCS (DP) to flag duplicate applications."""


def lcs_length(a, b):
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j-1] + 1 if a[i-1] == b[j-1] else max(prev[j], cur[j-1])
        prev = cur
    return prev[-1]


def find_duplicates(applicants, threshold=0.9):
    sig = lambda a: (a["name"] + a["phone"]).lower().replace(" ", "")
    dups = []
    for i in range(len(applicants)):
        for j in range(i + 1, len(applicants)):
            x, y = sig(applicants[i]), sig(applicants[j])
            ratio = lcs_length(x, y) / max(len(x), len(y))
            if ratio >= threshold:
                dups.append((applicants[i]["id"], applicants[j]["id"], round(ratio, 2)))
    return dups


def remove_duplicates(applicants, dups):
    drop = {b for _, b, _ in dups}          # keep the first submission
    return [a for a in applicants if a["id"] not in drop]
