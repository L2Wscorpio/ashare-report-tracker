#!/bin/bash
# 验真器 API 使用示例 — curl

BASE="https://api.ocshare.cc"

echo "=== 1. 单报告六窗口数据 ==="
curl -s "${BASE}/v1/report/outcome?report_id=21669" | python3 -m json.tool

echo ""
echo "=== 2. 搜索分析师报告 ==="
curl -s "${BASE}/v1/reports?analyst=陈显帆&limit=3" | python3 -m json.tool

echo ""
echo "=== 3. 搜索股票报告 ==="
curl -s "${BASE}/v1/reports?stock=000925&limit=2" | python3 -m json.tool

echo ""
echo "=== 4. 健康检查 ==="
curl -s "${BASE}/health" | python3 -m json.tool
