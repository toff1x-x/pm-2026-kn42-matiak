"""Monte Carlo прогноз за velocity (ЛР9). Запуск:
   python simulate.py <velocity.csv> <залишок_points> [прогонів]
Приклад для навчальних даних: python simulate.py lr09_reference_velocity.csv 220
"""
import csv, math, random, sys

def load(path, first=None, last=None):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    if first is not None:
        rows = [r for r in rows if first <= int(r["sprint"]) <= last]
    return [float(r["points_done"]) for r in rows]

def simulate(velocity, remaining, runs=10000, seed=42):
    random.seed(seed)
    results = []
    for _ in range(runs):
        left, sprints = remaining, 0
        while left > 0:
            left -= random.choice(velocity)
            sprints += 1
            if sprints > 200:      # захист від нульової velocity
                break
        results.append(sprints)
    results.sort()
    def pct(p):                    # найменше N, до якого вкладається p% прогонів
        return math.ceil(results[math.ceil(p * runs) - 1])
    return pct(0.50), pct(0.85)

if __name__ == "__main__":
    path, remaining = sys.argv[1], float(sys.argv[2])
    runs = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
    v = load(path)
    print("velocity:", v, "середня", sum(v) / len(v))
    print("P50, P85 (спринтів):", simulate(v, remaining, runs))
