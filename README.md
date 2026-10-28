Intelligent Scholarship Allocation System

DSA-II (CCSE0301) PBL | BTech CSE | SDG 4 - Quality Education Author: Amlan Chakrabarty

Reads scholarship applications from a CSV, removes duplicates, checks eligibility, ranks applicants, and allocates a limited budget optimally.

Pipeline
Step	Technique	File
Duplicate detection	LCS (DP), O(nm)	duplicates.py
Eligibility + ranking	Max-heap (Unit 1)	ranking.py
Best set within budget	0/1 Knapsack DP, O(nW) + greedy comparison	allocator.py
Fund split by category	Multistage Resource Allocation DP	allocator.py
Exact budget use	Sum of Subsets, backtracking with pruning	backtracking.py
Interview panels	Graph Colouring, backtracking	backtracking.py

Priority score = 50% CGPA + 30% financial need + 20% attendance. Eligibility: attendance >= 75% and CGPA >= 7.0. 1 unit = Rs 10,000.

Run
bash
python main.py --budget 20 --panels 3

Python 3.8+, no external libraries. Replace data/applicants.csv with your own data (columns: id, name, phone, category, cgpa, family_income, attendance, requested, slot).
