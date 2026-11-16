#!/usr/bin/env bash
# 一键安装探店收割器（基于开源 MediaCrawler）。仅限个人内部使用，见 COMPLIANCE.md。
set -e
CITY="${1:-huainan}"
DIR="$(dirname "$0")/MediaCrawler"
git clone --depth 1 https://github.com/NanmiCoder/MediaCrawler.git "$DIR" || true
cd "$DIR"
python -m venv venv
./venv/Scripts/python -m pip install -r requirements.txt
# 国内网络用镜像装 Chromium
export PLAYWRIGHT_DOWNLOAD_HOST=https://cdn.npmmirror.com/binaries/playwright
./venv/Scripts/python -m playwright install chromium
# 改关键词为你的城市
sed -i "s/KEYWORDS = .*/KEYWORDS = \"${CITY}探店,${CITY}约会,${CITY}美食,${CITY}周末去哪\"/" config/base_config.py
echo "安装完成。运行: ./venv/Scripts/python main.py --platform xhs --lt qrcode --type search"
echo "浏览器会弹出二维码，用小红书 App 扫码。"
