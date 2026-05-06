# A股研报跟踪数据 API v1

**Base URL**: `https://api.ocshare.cc`

## 概述

本 API 提供基于真实研报的六窗口跟踪数据、复权因子（前复权+后复权）、宏观经济指标。每份数据对应一篇研报，包含报告发布后 30/90/180/270/360/450 天的收益率和峰值数据。

### 核心原则

- **可溯源**：每份数据对应原始研报，点开可查
- **不预测**：所有数据为历史统计，不构成投资建议
- **统一算法**：后复权中间价 = (当日开盘价 + 当日收盘价) / 2

### 限流

- **免费层**：每个 IP 每天 100 次请求
- 响应头返回用量信息：
  - `X-RateLimit-Limit`: 上限值（100）
  - `X-RateLimit-Remaining`: 剩余次数
  - `X-RateLimit-Reset`: 重置时间（UTC ISO8601）
- 超限返回 HTTP 429

### 认证

无需 API Key。按 IP 限流。

---

## 端点

### 1. 单报告六窗口数据

```
GET /v1/report/outcome?report_id={id}
```

返回单份报告的完整六窗口跟踪数据。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `report_id` | integer | 是 | 报告 ID |

**响应**

```json
{
  "code": 0,
  "data": {
    "report_id":      21669,
    "title":          "公司点评：城轨信号国产化+环保PPP助力公司未来增长",
    "source_url":     "https://pdf.dfcfw.com/pdf/H3_AP201701030232344245_1.pdf",
    "publish_date":   "2017-01-03",
    "stock_code":     "000925",
    "stock_name":     "众合科技",
    "rating":         "增持",
    "analysts":       [
      {"id": 1139, "name": "陈显帆"},
      {"id": 1249, "name": "王皓"}
    ],
    "institution_id": 1,
    "institution":    "东吴证券",
    "t1_date":        "2017-01-04",
    "windows": [
      {
        "days":      30,
        "n":         13,
        "ret":       -0.1035,
        "peak_ret":  0.0000,
        "peak_day":  0,
        "peak_date": "2017-01-04"
      },
      {
        "days":      90,
        "n":         53,
        "ret":       -0.0451,
        "peak_ret":  0.0135,
        "peak_day":  41,
        "peak_date": "2017-03-06"
      }
    ]
  }
}
```

**字段说明**

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `report_id` | integer | 报告唯一 ID |
| `title` | string | 研报标题 |
| `source_url` | string | 东方财富研报原文链接 |
| `publish_date` | string | 报告发布日期 |
| `stock_code` | string | 股票代码（6位） |
| `stock_name` | string | 股票名称 |
| `rating` | string | 研报原始评级（如"买入""增持"） |
| `analysts` | array | 分析师列表，每个含 `id` 和 `name` |
| `institution_id` | integer | 机构唯一 ID |
| `institution` | string | 机构名称 |
| `t1_date` | string | 入场日期（T+1，即报告发布后首个交易日） |
| `windows` | array | 六窗口数据 |

**窗口字段**

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `days` | integer | 日历窗口大小（30/90/180/270/360/450） |
| `n` | integer | 窗口内实际交易日数 |
| `ret` | float | 窗口末收益率。按后复权中间价计算 |
| `peak_ret` | float | 窗口内峰值收益率。窗口内最高中间价日 |
| `peak_day` | integer | 峰值出现日（从 t1_date 起的交易日偏移，0 = 入场日） |
| `peak_date` | string | 峰值出现实际日期 |

**收益计算**

```
入场价 = (T+1开盘价 + T+1收盘价) / 2（后复权）
每日价格 = (当日开盘价 + 当日收盘价) / 2（后复权）
ret = (窗口末价格 - 入场价) / 入场价
peak_ret = (窗口内最高价格 - 入场价) / 入场价
```

---

### 2. 报告发现

```
GET /v1/reports?analyst={name}&stock={code}
```

搜索报告元数据（不含窗口数据）。至少提供一个查询条件。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `analyst` | string | 条件 | 分析师姓名（模糊匹配） |
| `stock` | string | 条件 | 股票代码（精确匹配） |
| `limit` | integer | 否 | 每页条数，默认 20，最大 100 |
| `offset` | integer | 否 | 偏移量，默认 0 |

**响应**

```json
{
  "code": 0,
  "data": [
    {
      "report_id":      139917,
      "publish_date":   "2026-04-29",
      "analyst_name":   "刘海荣,李金凤",
      "institution":    "中邮证券",
      "stock_code":     "300839",
      "stock_name":     "博汇股份",
      "rating_text":    "买入",
      "title":          "主业营收稳健扩容，液冷新局打开增长空间"
    }
  ],
  "meta": {
    "total":  25,
    "limit":  20,
    "offset": 0
  }
}
```

---

### 3. 复权三件套

```
GET /v1/factors?code={code}&start_date={YYYYMMDD}&end_date={YYYYMMDD}
```

返回指定股票的不复权收盘价、前复权因子、后复权因子。用户可自行计算任意复权价格，验证收益计算逻辑。

```
后复权价格 = close × hfq_factor
前复权价格 = close × qfq_factor
```

**参数**

| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `code` | string | 是 | 股票代码，6位数字（如 000001） |
| `start_date` | string | 是 | 起始日期，YYYYMMDD |
| `end_date` | string | 是 | 结束日期，YYYYMMDD |
| `page` | integer | 否 | 页码，默认 1 |
| `page_size` | integer | 否 | 每页条数，默认 100，最大 1000 |

**响应**

```json
{
  "code": 0,
  "data": {
    "code": "000001.SZ",
    "rows": [
      {
        "trade_date": "2026-04-01",
        "close": 11.15,
        "qfq_factor": 1.0,
        "hfq_factor": 5.646637
      }
    ],
    "meta": {
      "total": 17,
      "page": 1,
      "page_size": 100,
      "description": "close=none(不复权), qfq_price=close*qfq_factor, hfq_price=close*hfq_factor"
    }
  }
}
```

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `close` | float | 不复权收盘价 |
| `qfq_factor` | float | 前复权因子。将不复权价格转换为前复权价格 |
| `hfq_factor` | float | 后复权因子。将不复权价格转换为后复权价格 |

> **与 Tushare 的差异**：Tushare 的 `adj_factor` 接口仅提供前复权因子，不提供后复权因子。本接口同时提供两个因子，用户无需分别调取价格和因子接口再反推。

---

### 4. 宏观指标

```
GET /v1/macro?indicator={name}&start_period={YYYY-MM}&end_period={YYYY-MM}
```

查询宏观经济指标历史数据。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `indicator` | string | 否 | 指标名（CPI/PMI/M2等），不传返回全部 |
| `start_period` | string | 否 | 起始月份，YYYY-MM |
| `end_period` | string | 否 | 结束月份，YYYY-MM |
| `page` | integer | 否 | 页码，默认 1 |
| `page_size` | integer | 否 | 每页条数，默认 100，最大 1000 |

**响应**

```json
{
  "code": 0,
  "data": {
    "rows": [
      {"indicator": "CPI", "period": "2025-08", "value": 0.4},
      {"indicator": "CPI", "period": "2025-07", "value": -0.1}
    ],
    "meta": {"total": 354, "page": 1, "page_size": 100}
  }
}
```

**可用指标**

| 指标 | 时间范围 | 行数 |
|:---|:---|:---|
| CPI | 1996-02 ~ 2025-08 | 354 |
| PPI | — | 363 |
| PMI_* | — | 220 |
| M2_* | 2008-01 ~ 2026-03 | 1,971 |

---

### 5. 健康检查

```
GET /health
```

```json
{"status": "ok"}
```

---

## 错误码

| HTTP 状态码 | 说明 | 响应体 |
|:---|:---|:---|
| 200 | 成功 | `{"code": 0, "data": ...}` |
| 400 | 参数错误 | `{"code": 400, "error": "...", "message": "..."}` |
| 404 | 报告未找到 | `{"code": 404, "error": "not_found", "message": "报告 XXX 未找到"}` |
| 429 | 请求频率超限 | `{"code": 429, "error": "rate_limit_exceeded", "message": "免费层每日 100 次调用已用完", "usage": {"used": 101, "limit": 100, "reset": "2026-05-02"}}` |
| 500 | 服务器内部错误 | — |

---

## 数据覆盖

- 报告来源：东方财富研报数据
- 时间范围：2017-01-02 至今
- 总报告数：约 13.6 万篇
- 行情数据：全 A 股日线（不复权）+ 复权因子（前复权、后复权）
- 宏观数据：CPI、PPI、PMI、M2
- 指数数据：沪深300、创业板指
- 更新频率：行情及复权因子每日更新，宏观指标每月更新

## 免责声明

- 本 API 仅提供研报公开元数据（标题、来源链接）及历史统计数据，不提供研报全文
- 收益率数据均为历史统计结果，不代表未来表现
- 不构成任何投资建议，用户应自行判断和承担风险
