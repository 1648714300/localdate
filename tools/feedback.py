#!/usr/bin/env python
"""feedback.py —— 把真实排序收成可训练的样本（零依赖）。

用法:
  python feedback.py add --kept picking,boat --rejected mall --note "草莓棚想再去"
  python feedback.py build      # feedback.jsonl -> rounds.json，并打印权重变化
  python feedback.py report     # 生成可粘贴到 issue 的匿名摘要

数据只在本机 feedback/feedback.jsonl，不上传。
"""
import argparse, json, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JSONL = os.path.join(ROOT, "feedback", "feedback.jsonl")
ROUNDS = os.path.join(ROOT, "feedback", "rounds.json")

PRIOR = {
    "event_limited": 1600, "animal": 1580, "performance": 1580, "park": 1560,
    "night_market": 1520, "sport_light": 1500, "picking": 1500, "cycling": 1500,
    "boat": 1500, "static_sight": 1450, "old_street": 1440, "handcraft": 1430,
    "home_routine": 1400, "mall": 1400, "passive_service": 1400, "movie": 1400,
}
K = 24.0

def load_jsonl():
    if not os.path.exists(JSONL):
        return []
    out = []
    with open(JSONL, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out

def cmd_add(a):
    os.makedirs(os.path.dirname(JSONL), exist_ok=True)
    rows = load_jsonl()
    rec = {
        "date": a.date or datetime.date.today().isoformat(),
        "round": a.round or (len(rows) + 1),
        "kept": [x for x in (a.kept or "").split(",") if x],
        "rejected": [x for x in (a.rejected or "").split(",") if x],
        "note": a.note or "",
    }
    if not rec["kept"] and not rec["rejected"]:
        sys.exit("至少要给 --kept 或 --rejected")
    with open(JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"已记录第 {rec['round']} 轮：留 {len(rec['kept'])} 个特征，否 {len(rec['rejected'])} 个")

def expected(ra, rb):
    return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))

def cmd_build(a):
    rows = load_jsonl()
    if not rows:
        sys.exit("还没有样本，先 add 一轮")
    rating = dict(PRIOR)
    before = dict(PRIOR)
    for r in rows:
        for f in r.get("kept", []):
            rating.setdefault(f, 1500)
        for g in r.get("rejected", []):
            rating.setdefault(g, 1500)
        for f in r.get("kept", []):
            for g in r.get("rejected", []):
                e = expected(rating[f], rating[g])
                rating[f] += K * (1 - e)
                rating[g] -= K * (1 - e)
    rounds = [{"round": r.get("round", i + 1), "kept": r.get("kept", []),
               "rejected": r.get("rejected", [])} for i, r in enumerate(rows)]
    with open(ROUNDS, "w", encoding="utf-8") as f:
        json.dump(rounds, f, ensure_ascii=False, indent=1)
    print(f"{'特征':<18}{'先验':>7}{'现在':>8}{'变化':>8}")
    for k, v in sorted(rating.items(), key=lambda x: -x[1]):
        d = v - before.get(k, 1500)
        flag = "↑" if d > 1 else ("↓" if d < -1 else "·")
        print(f"{k:<18}{before.get(k,1500):>7}{v:>8.1f}{d:>+8.1f} {flag}")
    print(f"\n{len(rows)} 轮样本 -> {ROUNDS}")
    if os.path.exists(os.path.join(HERE, "score_lite.py")):
        print("下一步：python tools/score_lite.py feedback/rounds.json")

def cmd_report(a):
    rows = load_jsonl()
    if not rows:
        sys.exit("还没有样本")
    kept, rej = {}, {}
    for r in rows:
        for f in r.get("kept", []):
            kept[f] = kept.get(f, 0) + 1
        for f in r.get("rejected", []):
            rej[f] = rej.get(f, 0) + 1
    print(f"## 我的排序样本（{len(rows)} 轮）\n")
    print("**反复留下的**：" + "、".join(f"{k}({v})" for k, v in sorted(kept.items(), key=lambda x: -x[1])))
    print("\n**反复否掉的**：" + "、".join(f"{k}({v})" for k, v in sorted(rej.items(), key=lambda x: -x[1])))
    notes = [r["note"] for r in rows if r.get("note")]
    if notes:
        print("\n**我自己写的备注**：")
        for n in notes[-5:]:
            print(f"- {n}")
    print("\n（以上可直接粘进 round-feedback issue）")

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("add"); pa.add_argument("--kept"); pa.add_argument("--rejected")
    pa.add_argument("--note"); pa.add_argument("--date"); pa.add_argument("--round", type=int)
    pa.set_defaults(fn=cmd_add)
    pb = sub.add_parser("build"); pb.set_defaults(fn=cmd_build)
    pr = sub.add_parser("report"); pr.set_defaults(fn=cmd_report)
    a = p.parse_args(); a.fn(a)

if __name__ == "__main__":
    main()
