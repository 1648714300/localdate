#!/usr/bin/env bash
# 运行小红书关键词收割（需已 setup && 扫码）。数据落 MediaCrawler/data/xhs/csv/
cd "$(dirname "$0")/MediaCrawler"
./venv/Scripts/python main.py --platform xhs --lt qrcode --type search
