#!/usr/bin/env python
"""把 MediaCrawler 收割的小红书 CSV 整理成城市包候选条目（markdown 表行）。
用法: python csv2catalog.py [csv目录] [关键词过滤] > harvest.md
合规提醒：产物仅限个人内部候选参考，不得进入公开发布的城市包（见 COMPLIANCE.md）。
"""
import csv, glob, sys, re
csv_dir = sys.argv[1] if len(sys.argv) > 1 else "MediaCrawler/data/xhs/csv"
keyword = sys.argv[2] if len(sys.argv) > 2 else ""
rows = []
for f in glob.glob(f"{csv_dir}/*.csv"):
    with open(f, encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            title = (r.get("title") or r.get("Title") or "").strip()
            nickname = (r.get("nickname") or r.get("Nickname") or "").strip()
            liked = r.get("liked_count") or r.get("Liked_Count") or "0"
            desc = (r.get("desc") or r.get("Desc") or "").strip()
            if keyword and keyword not in title + desc:
                continue
            rows.append((int(re.sub(r"\D", "", liked) or 0), title, nickname, desc[:60]))
rows.sort(reverse=True)
print("| 条目/笔记 | 作者 | 赞 | 用途 |")
print("|---|---|---|---|")
for liked, title, nickname, desc in rows[:60]:
    print(f"| {title[:40] or desc[:40]} | {nickname} | {liked} | 探店线索，需现搜核实 |")
print(f"\n共 {len(rows)} 条，展示前 {min(60, len(rows))} 条（按赞排序）。")
