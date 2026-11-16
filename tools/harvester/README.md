# harvester —— 把一个城市的探店内容收成候选条目

用开源项目 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 按关键词收割公开笔记，再转成城市包的候选表行。仅为自己搭库用，账号和平台规则自担。

```bash
bash setup_harvester.sh huainan     # 装环境 + 把关键词改成 "<城市>探店"
bash run_xhs.sh                     # 弹二维码，扫码登录
python csv2catalog.py 路径/to/csv   # CSV -> markdown 表行（按赞排序）
```

产出怎么用：先当"线索表"，逐条拆出店名地址价格再进 `catalog/`。别把笔记原文直接贴进库——标题党跑不进方案。
