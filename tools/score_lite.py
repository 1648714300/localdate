#!/usr/bin/env python
"""score_lite —— Bradley-Terry/Elo 降权学习（零依赖）。
输入 rounds.json: [{"round":1,"kept":["event_bird"],"rejected":["static_lake"]}, ...]
输出: 特征评分表 + 候选排序。
"""
import json, math, sys, os

K, LAM, C, HEAT_W = 24.0, 0.05, 40.0, 0.15
PRIOR = {  # 先验评分（Elo 尺度，1500 均值）
    "event_limited": 1600, "animal": 1580, "performance": 1580, "park": 1560,
    "night_market": 1520, "sport_light": 1500, "static_sight": 1450,
    "old_street": 1440, "handcraft": 1430, "home_routine": 1400,
}
SLEEP_THRESHOLD = 1440

def expected(ra, rb):
    return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def main(path="rounds.json", heat=None, out_n=15):
    rounds = load(path)
    rating = dict(PRIOR)
    counts = {k: 0 for k in PRIOR}
    for r in rounds:
        for f in r.get("kept", []):
            rating.setdefault(f, 1500); counts.setdefault(f, 0)
            for g in r.get("rejected", []):
                rating.setdefault(g, 1500); counts.setdefault(g, 0)
                e = expected(rating[f], rating[g])
                rating[f] += K * (1 - e)
                rating[g] += K * (0 - (1 - e))
                counts[f] += 1; counts[g] += 1
    # 时间衰减回 1500
    n = len(rounds)
    for f in rating:
        rating[f] = 1500 + (rating[f] - 1500) * math.exp(-LAM * max(0, n - counts.get(f, 0) / 2))
    total = sum(counts.values()) or 1
    print(f"{'特征':<18}{'评分':>8}{'比较次数':>10}{'状态':>8}")
    for f, r in sorted(rating.items(), key=lambda x: -x[1]):
        ln_n = math.log(max(total, 2))
        bonus = C * math.sqrt(ln_n / max(counts.get(f, 0), 1))
        state = "休眠" if r + bonus < SLEEP_THRESHOLD else "活跃"
        print(f"{f:<18}{r:>8.1f}{counts.get(f,0):>10}{state:>8}")
    if heat and os.path.exists(heat):
        print("\n热度加权（前 10）:")
        h = json.load(open(heat, encoding="utf-8"))
        scored = [(k, v + HEAT_W * hv) for k, v in h.items() for hv in [h[k]]]
        for k, s in sorted(scored, key=lambda x: -x[1])[:out_n]:
            print(f"  {k:<20}{s:.1f}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "rounds.json",
         sys.argv[2] if len(sys.argv) > 2 else None)
