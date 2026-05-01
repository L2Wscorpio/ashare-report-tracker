# A股研报跟踪数据 API

> 本项目由 AI 编程助手「小派」（DeepSeek 驱动）为主完成开发、文档撰写与日常维护。

基于 A 股真实研报的六窗口跟踪数据，免费开放。

不预测，不建议——只提供可溯源的历史统计。

## 访问

```
Base URL: https://api.ocshare.cc
文档:     https://api.ocshare.cc/v1/docs
认证:     无需 API Key，按 IP 限制调用次数
限流:     每 IP 每天 100 次
```

## 快速开始

```bash
# 查一篇报告的六窗口数据
curl https://api.ocshare.cc/v1/report/outcome?report_id=21669

# 搜索分析师
curl "https://api.ocshare.cc/v1/reports?analyst=陈显帆&limit=3"
```

搜索接口支持 `limit`（默认20，最大100）和 `offset` 分页。完整参数见 `docs/api.md`。

Python 示例依赖 `requests`：`pip install requests`

## 数据结构

每篇研报对应六个时间窗口：**30 / 90 / 180 / 270 / 360 / 450 天**。

每个窗口输出：

| 字段 | 说明 |
|:---|:---|
| `ret` | 窗口末收益率 |
| `peak_ret` | 窗口内峰值收益率 |
| `peak_day` | 峰值出现日（从 T+1 起的交易日偏移，0=入场日） |
| `peak_date` | 峰值出现实际日期 |
| `n` | 窗口内实际交易日数 |

收益率统一使用**后复权中间价**计算： `(开盘价 + 收盘价) / 2`

## 项目结构

```
├── README.md
├── LICENSE            MIT
├── docs/
│   ├── api.md         完整 API 文档
│   └── openapi.yaml   OpenAPI 3.0 规范
└── examples/
    ├── python/         Python 调用示例
    ├── curl/           Shell 示例
    └── javascript/     JS fetch 示例
```

## 数据覆盖

- 来源：东方财富研报
- 时间：2017-01-02 至今
- 总量：约 13.6 万篇报告
- 更新：每日增量

## 许可

MIT

## 免责

- 本 API 仅提供研报公开元数据（标题、来源链接）及历史统计数据，**不提供研报全文**
- 收益率数据均为历史统计结果，不代表未来表现
- 不构成任何投资建议，用户应自行判断和承担风险
- 代码许可（MIT）仅适用于本仓库中的代码和文档，不适用于 API 服务本身
