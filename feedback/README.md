# feedback/

每轮交付完，技能往 `feedback.jsonl` 追加一行：

```json
{"date":"2026-11-16","round":12,"kept":["picking","boat"],"rejected":["mall"],"note":"草莓棚想再去"}
```

然后 `python tools/feedback.py build` 把它算成特征评分。这里的数据只在本机，别推到仓库。
