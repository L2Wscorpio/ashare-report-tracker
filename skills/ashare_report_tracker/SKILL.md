---
name: ashare_report_tracker
description: "Query A-share research report tracking data. Use when the user asks about analyst reports, research report accuracy, analyst performance, or post-report stock returns. Provides six-window (30/90/180/270/360/450 day) return tracking for each report."
metadata:
  emoji: "📊"
---

# A股研报跟踪数据

## 触发条件

用户询问以下内容时调用本 API：
- 某只股票的研报覆盖情况
- 某分析师或机构的历史预测表现
- 研报发布后股票的收益率跟踪
- "看看这只票最近有没有研报"
- "某分析师推的票后来涨了吗"

## API 信息

- **Base URL**: `https://api.ocshare.cc`
- **认证**: 无需 API Key（按 IP 限流 100 次/天）
- **响应头**: `X-RateLimit-Remaining` 显示剩余次数

## 端点

### 1. 查询报告跟踪数据
```
GET /v1/report/outcome?report_id={id}
```

返回单份报告的完整六窗口跟踪数据。

响应字段：
```
report_id, title, source_url     → 报告标识与来源链接
stock_code, stock_name           → 股票信息
analysts: [{id, name}]          → 分析师列表
institution, institution_id     → 机构信息
rating                          → 原始评级
t1_date                         → 入场日（报告发布后首个交易日）

windows: [30, 90, 180, 270, 360, 450] 天
  ret       → 窗口末收益率
  peak_ret  → 窗口内峰值收益率
  peak_date → 峰值出现实际日期
  peak_day  → 峰值偏移交易日数（0 = 入场日）
  n         → 窗口内实际交易日数
```

### 2. 搜索报告
```
GET /v1/reports?analyst={name}&stock={code}&limit=20&offset=0
```

- `analyst`: 分析师姓名，模糊匹配
- `stock`: 股票代码，6 位精确匹配
- `limit`: 每页条数，默认 20，最大 100
- `offset`: 分页偏移

返回报告元数据列表（不含窗口数据）。

## 常见查询流程

1. **某分析师的历史记录**：先 `/v1/reports?analyst=名字` 拿报告列表，再逐篇查 outcome
2. **某只股票的研报覆盖**：`/v1/reports?stock=代码`
3. **直接看窗口收益率**：`/v1/report/outcome?report_id=N`

## 数据解读原则

- 所有收益率为历史统计，不代表未来
- 只陈述事实，不做预测或投资建议
- 每个数字可溯源：`source_url` 链接到东方财富研报原文
- 多窗口对比可观察"短期信号 vs 长期衰减"

## 安装到你的 Agent

### QwenPaw 用户

将本文件夹放入 agent 的 skills 目录：

```bash
cp -r skills/ashare_report_tracker ~/.qwenpaw/workspaces/<agent_id>/skills/
```

然后重启 agent，skill 自动加载。

### OpenClaw 用户

```bash
cp -r skills/ashare_report_tracker ~/.openclaw/skills/
```

### 其他 Agent 框架

只需 `skills/ashare_report_tracker/SKILL.md` 这一个文件。支持 Markdown frontmatter 标准格式的框架都能直接读取。
