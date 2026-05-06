"""
A股研报跟踪数据 API 使用示例 — Python
"""
import requests

BASE = "https://api.ocshare.cc"


def get_report_outcome(report_id: int):
    """获取单份报告的六窗口数据"""
    r = requests.get(f"{BASE}/v1/report/outcome", params={"report_id": report_id})
    r.raise_for_status()
    return r.json()


def get_factors(code: str, start_date: str, end_date: str):
    """获取复权三件套：不复权收盘价 + 前复权因子 + 后复权因子"""
    r = requests.get(f"{BASE}/v1/factors", params={
        "code": code, "start_date": start_date, "end_date": end_date
    })
    r.raise_for_status()
    return r.json()


def get_macro(indicator: str = None, start_period: str = None, end_period: str = None):
    """获取宏观经济指标"""
    params = {}
    if indicator:
        params["indicator"] = indicator
    if start_period:
        params["start_period"] = start_period
    if end_period:
        params["end_period"] = end_period
    r = requests.get(f"{BASE}/v1/macro", params=params)
    r.raise_for_status()
    return r.json()


def search_reports(analyst: str = None, stock: str = None, limit: int = 20):
    """搜索报告"""
    params = {"limit": limit}
    if analyst:
        params["analyst"] = analyst
    if stock:
        params["stock"] = stock
    r = requests.get(f"{BASE}/v1/reports", params=params)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    # 查一篇报告
    data = get_report_outcome(21669)
    d = data["data"]
    print(f"报告 {d['report_id']}: {d['stock_name']} ({d['stock_code']})")
    print(f"机构: {d['institution']}")
    print(f"分析师: {', '.join(a['name'] for a in d['analysts'])}")
    print(f"T+1 入场: {d['t1_date']}")
    print()
    print("窗口    交易日    收益      峰值收益   峰值日")
    for w in d["windows"]:
        print(f"{w['days']:4d}d  {w['n']:4d}     {w['ret']:+.4f}   {w['peak_ret']:+.4f}    {w['peak_day']}")

    # 查复权因子
    print(f"\n{'-'*50}\n平安银行 2026年4月 复权三件套:")
    factors = get_factors("000001", "20260401", "20260430")
    for row in factors["data"]["rows"][:3]:
        qfq_price = row["close"] * row["qfq_factor"]
        hfq_price = row["close"] * row["hfq_factor"]
        print(f"  {row['trade_date']}: close={row['close']:.2f} 前复权价={qfq_price:.2f} 后复权价={hfq_price:.2f}")

    # 查宏观指标
    print(f"\n{'-'*50}\n最近三个月 CPI:")
    macro = get_macro(indicator="CPI", end_period="2025-12")
    for r in macro["data"]["rows"][:3]:
        print(f"  {r['period']}: {r['value']}%")
