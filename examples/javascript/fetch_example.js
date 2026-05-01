/**
 * 验真器 API 使用示例 — JavaScript (fetch)
 */
const BASE = "https://api.ocshare.cc";

// 获取单报告六窗口数据
async function getReportOutcome(reportId) {
  const r = await fetch(`${BASE}/v1/report/outcome?report_id=${reportId}`);
  if (!r.ok) throw new Error(`HTTP ${r.status}: ${await r.text()}`);
  return r.json();
}

// 搜索报告
async function searchReports({ analyst, stock, limit = 20 }) {
  const params = new URLSearchParams({ limit });
  if (analyst) params.set("analyst", analyst);
  if (stock) params.set("stock", stock);
  const r = await fetch(`${BASE}/v1/reports?${params}`);
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

// 示例
(async () => {
  try {
    // 查一篇报告
    const { data: d } = await getReportOutcome(21669);
    console.log(`报告 ${d.report_id}: ${d.stock_name} (${d.stock_code})`);
    console.log(`机构: ${d.institution}`);
    console.log(`T+1 入场: ${d.t1_date}`);

    d.windows.forEach(w => {
      console.log(
        `${w.days}d | n=${w.n} | ret=${w.ret.toFixed(4)} | peak=${w.peak_ret.toFixed(4)}`
      );
    });

    // 搜索
    const { data: reports } = await searchReports({ analyst: "陈显帆", limit: 3 });
    console.log(`\n找到 ${reports.length} 篇报告`);
    reports.forEach(r => console.log(`  [${r.report_id}] ${r.stock_name} ${r.rating_text}`));
  } catch (e) {
    console.error(e);
  }
})();
