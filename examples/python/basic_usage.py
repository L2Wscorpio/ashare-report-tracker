"""
验真器 API 使用示例 — Python
"""
import requests

BASE = "https://api.ocshare.cc"


def get_report_outcome(report_id: int):
    """获取单份报告的六窗口数据"""
    r = requests.get(f"{BASE}/v1/report/outcome", params={"report_id": report_id})
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

    # 搜索某分析师的报告
    print(f"\n{'-'*50}\n搜索分析师「陈显帆」:")
    result = search_reports(analyst="陈显帆", limit=5)
    for r in result["data"]:
        print(f"  [{r['report_id']}] {r['stock_name']} {r['rating_text']} {r['publish_date']}")
    print(f"  共 {result['meta']['total']} 篇")
