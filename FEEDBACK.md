# 反馈闭环：项目怎么靠真实使用自己长

这个项目不猜你喜欢什么，也不发问卷。**它只认一件事：你把上一轮哪几个留下了。**

## 一、每轮交付完，写一行

技能在给出 15 个方案后，会自动往 `feedback/feedback.jsonl` 追加一行：

```json
{"date":"2026-11-16","round":12,"kept":["picking","boat","sport_light"],"rejected":["mall","movie"],"note":"草莓棚想再去一次"}
```

`kept` / `rejected` 写的是**特征标签**，不是具体地点——地点会倒闭，特征不会。常用标签见下表。

## 二、把它算成权重

```bash
python tools/feedback.py add --kept picking,boat --rejected mall --note "草莓棚想再去"
python tools/feedback.py build      # jsonl -> rounds.json
python tools/score_lite.py rounds.json
```

`build` 会顺手算出每个特征的评分变化，直接告诉你"这次排序让哪一类升了、哪一类降了"。

## 三、三条反馈通道

| 通道 | 适合 | 怎么走 |
|---|---|---|
| **本地闭环** | 自己用，最快 | 每轮追加一行 jsonl，`build` 一下，权重自己会动 |
| **Issue：一轮排序** | 想让作者把这个信号并进框架先验 | 用 `round-feedback` 模板贴一轮 kept/rejected |
| **Issue：地点报错** | 店倒了、涨价了、搬了 | 用 `venue-report` 模板，写城市＋店名＋你看到的证据 |

## 四、特征标签表（写 kept/rejected 时用这些词）

| 标签 | 含义 |
|---|---|
| `event_limited` | 限定时刻（候鸟/花期/初雪/灯会） |
| `animal` | 看动物 |
| `performance` | 演出、脱口秀、实景剧 |
| `sport_light` | 有输赢的轻运动（射箭/台球/保龄球） |
| `picking` | 采摘、动手做东西 |
| `cycling` | 骑行、步行、走一段路 |
| `boat` | 坐船、轮渡、游湖 |
| `park` | 公园、湿地、大草坪 |
| `night_market` | 夜市、小吃街、扫街吃 |
| `static_sight` | 站着看的风景（观景台/灯光秀/日落） |
| `old_street` | 老街、古镇 |
| `handcraft` | 手作、工坊、非遗课 |
| `mall` | 商场内消费（超市/商场餐饮/影院） |
| `passive_service` | 躺着被服务（汗蒸/足疗/SPA） |
| `movie` | 电影院 |
| `home_routine` | 家内流水（做饭/家务/办事） |
| `far_trip` | 单程 3 小时以上 |

## 五、这些样本最后去哪了

1. 你在本地的 jsonl → `score_lite.py` 更新你个人的特征评分；
2. 你贴的 issue → 作者人工判断是否改**框架先验**（`PRIOR` 表），改了就写进 `CHANGELOG.md`；
3. 报错的店 → 直接从 `catalog/` 删或标"已停业"，不让下一个人白跑。

## 六、为什么不做遥测

不做。城市包里写着"她腰不好""她不喜欢强互动"这类东西，上传就是事故。所以收集方式是**你主动贴**，不是它偷偷传。宁可样本少，不要样本脏。
