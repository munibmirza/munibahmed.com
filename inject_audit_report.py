with open('InterAudit-P1.html', encoding='utf-8') as f:
    content = f.read()

# ── 1. CDN for html-docx-js (insert before </head>) ──────────────────────────
content = content.replace(
    '</head>',
    '<script src="https://cdn.jsdelivr.net/npm/html-docx-js@0.3.1/dist/html-docx.js"></script>\n</head>'
)

# ── 2. TILE (insert before tile-c) ───────────────────────────────────────────
TILE = """
        <!-- ============ Tile — Audit Report Generator ============ -->
        <a href="#/audit-report" class="tile" style="background: linear-gradient(160deg, #2a1c0e 0%, #1a1008 100%);">
          <div class="aurora"></div>
          <svg style="position:absolute;right:-20px;bottom:-20px;width:280px;opacity:.7;z-index:1;" viewBox="0 0 280 220" fill="none">
            <rect x="55" y="30" width="140" height="175" rx="8" stroke="rgba(205,160,80,.45)" stroke-width="1.4" fill="rgba(205,160,80,.05)"/>
            <rect x="55" y="30" width="140" height="22" rx="8" fill="rgba(205,160,80,.22)" stroke="none"/>
            <g stroke="rgba(205,160,80,.4)" stroke-width="1.2">
              <line x1="70" y1="72"  x2="180" y2="72"/>
              <line x1="70" y1="88"  x2="160" y2="88"/>
              <line x1="70" y1="104" x2="175" y2="104"/>
              <line x1="70" y1="120" x2="150" y2="120"/>
              <line x1="70" y1="136" x2="178" y2="136"/>
              <line x1="70" y1="152" x2="155" y2="152"/>
              <line x1="70" y1="168" x2="170" y2="168"/>
            </g>
            <rect x="70" y="76" width="8" height="8" rx="1" fill="rgba(80,200,120,.55)" stroke="none"/>
            <rect x="70" y="108" width="8" height="8" rx="1" fill="rgba(255,100,100,.55)" stroke="none"/>
            <rect x="70" y="140" width="8" height="8" rx="1" fill="rgba(255,200,50,.55)" stroke="none"/>
            <g stroke="rgba(255,216,77,.7)" stroke-width="1.6" fill="none" stroke-linecap="round">
              <path d="M210 40 L240 40 L240 80" stroke-dasharray="4 5">
                <animate attributeName="stroke-dashoffset" from="0" to="-36" dur="2.8s" repeatCount="indefinite"/>
              </path>
              <path d="M235 74 l7 8 m-7 0 l7-8"/>
            </g>
          </svg>
          <div class="tile-body">
            <div class="tile-meta">
              <div class="orb">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
              </div>
              <span class="tag live">Live</span>
            </div>
            <h3 class="h-serif text-2xl mt-5 text-white leading-tight">
              Audit <span class="italic text-yellow-300">Report</span>
            </h3>
            <p class="text-sm text-blue-100/80 mt-2 leading-relaxed max-w-[28ch]">
              Upload working-paper Excel for auto-extraction, fill observations, and export a fully formatted
              <b class="text-yellow-300">.docx</b> audit report.
            </p>
            <div class="flex flex-wrap gap-2 mt-4">
              <span class="micro-stat">Excel auto-fill</span>
              <span class="micro-stat">Word export</span>
            </div>
            <div class="mt-auto">
              <span class="cta">Open workflow
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
                </svg>
              </span>
            </div>
          </div>
        </a>

"""
content = content.replace(
    '        <!-- ============ Tile C — Add new workflow ============ -->',
    TILE + '        <!-- ============ Tile C — Add new workflow ============ -->'
)

# ── 3. PAGE HTML ──────────────────────────────────────────────────────────────
PAGE = """
  <!-- ====================== AUDIT REPORT GENERATOR ====================== -->
  <div id="page-audit-report" class="space-y-6 hidden">

    <div class="flex items-center gap-3 text-blue-200/80 text-sm">
      <a href="#/app" class="crumb-link">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
        </svg>Workspace
      </a>
      <span class="text-blue-200/40">/</span>
      <span class="text-blue-100">Audit Report Generator</span>
    </div>

    <section class="glass p-7">
      <div class="flex items-center gap-3 mb-2">
        <div class="gold-bar"></div>
        <span class="text-[11px] uppercase tracking-[0.28em] text-yellow-300/90">Workflow</span>
      </div>
      <div class="flex items-center gap-3 mt-2">
        <h2 class="h-serif text-4xl text-white leading-tight">
          Audit <span class="italic text-yellow-300">Report Generator</span>
        </h2>
        <span class="tip tip-sign" data-tip="Upload your working-paper Excel to auto-fill analysis tables. Fill in checklist and observations, then export a formatted Word document.">i</span>
      </div>
      <p class="text-sm text-blue-100/70 mt-2">Service Center Internal Audit Report — fills from Excel working papers, exports .docx.</p>
    </section>

    <!-- REPORT INFO + EXCEL UPLOAD -->
    <section class="glass p-6">
      <div class="flex items-center gap-3 mb-5">
        <div class="gold-bar"></div>
        <h2 class="h-serif text-2xl text-white">Report Information</h2>
        <button id="arGenBtn" class="btn-primary ml-auto">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3M5 20h14a2 2 0 002-2v-2H3v2a2 2 0 002 2z"/>
          </svg>Generate Report (.docx)
        </button>
      </div>

      <!-- Excel upload bar -->
      <div class="bg-white/5 border border-white/10 rounded-xl p-4 mb-5 flex flex-wrap items-center gap-4">
        <div class="flex-1 min-w-[220px]">
          <p class="text-xs uppercase tracking-widest text-yellow-300/90 mb-1">Step 1 — Upload Working Paper Excel (optional)</p>
          <p class="text-xs text-blue-100/60">Automatically extracts: notifications, warranty, aging, revenue, expenses from your SHL working-paper file.</p>
        </div>
        <label class="btn-accent cursor-pointer">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M12 4v12m0-12l-4 4m4-4l4 4"/>
          </svg>Upload Excel
          <input id="arExcelInput" type="file" accept=".xlsx,.xls" class="hidden"/>
        </label>
        <div id="arExcelBadge" class="text-xs text-blue-100/60">No file loaded</div>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div><label class="shl-label">Branch / Service Center</label><input id="ar_branch" class="shl-input" value="Rawalpindi"/></div>
        <div><label class="shl-label">Category</label><input id="ar_category" class="shl-input" value="Service Center"/></div>
        <div><label class="shl-label">Report Date</label><input id="ar_report_date" class="shl-input" value=""/></div>
        <div><label class="shl-label">Audit Period — From</label><input id="ar_cur_from" class="shl-input" value="December 1, 2025"/></div>
        <div><label class="shl-label">Audit Period — To</label><input id="ar_cur_to" class="shl-input" value="March 31, 2026"/></div>
        <div><label class="shl-label">Cutoff Date</label><input id="ar_cutoff" class="shl-input" value="April 13, 2026"/></div>
        <div><label class="shl-label">Previous Period — From</label><input id="ar_prev_from" class="shl-input" value="June 1, 2025"/></div>
        <div><label class="shl-label">Previous Period — To</label><input id="ar_prev_to" class="shl-input" value="November 30, 2025"/></div>
        <div><label class="shl-label">Days in Period</label><input id="ar_days" type="number" class="shl-input" value="120"/></div>
        <div><label class="shl-label">Prepared By</label><input id="ar_prepared_by" class="shl-input" value="Munib Ahmed"/></div>
        <div><label class="shl-label">Reviewed By</label><input id="ar_reviewed_by" class="shl-input" value="Muhammad Ahmad Hanif"/></div>
        <div><label class="shl-label">Service Center In-Charge</label><input id="ar_sc_incharge" class="shl-input" value=""/></div>
        <div><label class="shl-label">SC In-Charge Email</label><input id="ar_sc_email" class="shl-input" value=""/></div>
        <div><label class="shl-label">SC In-Charge Mobile</label><input id="ar_sc_mobile" class="shl-input" value=""/></div>
        <div><label class="shl-label">No. of Technicians</label><input id="ar_technicians" type="number" class="shl-input" value="8"/></div>
      </div>
    </section>

    <!-- TABS -->
    <section class="glass p-6">
      <div class="flex gap-1 flex-wrap border-b border-white/10 mb-5">
        <button class="tab-btn active" data-ar-tab="ar-tab-checklist">Checklist</button>
        <button class="tab-btn" data-ar-tab="ar-tab-analysis">Analysis</button>
        <button class="tab-btn" data-ar-tab="ar-tab-obs">Observations</button>
        <button class="tab-btn" data-ar-tab="ar-tab-conclusion">Conclusion</button>
      </div>

      <!-- ── CHECKLIST ── -->
      <div id="ar-tab-checklist" class="ar-pane">
        <p class="text-xs text-blue-100/60 mb-3 uppercase tracking-widest">Edit remarks; particulars are fixed per company audit standard.</p>
        <div class="overflow-x-auto data-surface rounded-xl">
          <table class="w-full text-sm" id="arChecklistTable">
            <thead><tr>
              <th class="px-3 py-2 w-10">Sr.</th>
              <th class="text-left px-4 py-2">Particulars</th>
              <th class="px-4 py-2 min-w-[180px]">Remarks</th>
            </tr></thead>
            <tbody id="arChecklistBody"></tbody>
          </table>
        </div>
      </div>

      <!-- ── ANALYSIS ── -->
      <div id="ar-tab-analysis" class="ar-pane hidden">
        <p class="text-xs text-blue-100/60 mb-4 uppercase tracking-widest">Auto-filled from Excel upload. Edit any cell directly.</p>

        <!-- 1.1 Notification Analysis -->
        <div class="mb-6">
          <p class="text-yellow-300/90 text-xs uppercase tracking-widest mb-2 font-bold">1.1 CS Notification Analysis</p>
          <div class="overflow-x-auto data-surface rounded-xl mb-3">
            <table class="w-full text-sm"><thead><tr>
              <th class="text-left px-4 py-2 min-w-[230px]">Particulars</th>
              <th class="px-3 py-2">AC</th><th class="px-3 py-2">REF</th><th class="px-3 py-2">WD</th>
              <th class="px-3 py-2">WM</th><th class="px-3 py-2">OVEN</th><th class="px-3 py-2">LED</th>
              <th class="px-3 py-2">Total</th>
            </tr></thead><tbody id="arNotifBody"></tbody></table>
          </div>
          <div class="grid sm:grid-cols-3 gap-3">
            <div><label class="shl-label">Total In-House Complaints</label><input id="ar_ih_total" type="number" class="shl-input" value="1829"/></div>
            <div><label class="shl-label">Total Contract Workshop</label><input id="ar_cw_total" type="number" class="shl-input" value="3185"/></div>
            <div><label class="shl-label">Avg Age — In-House (days)</label><input id="ar_avg_age_ih" type="number" class="shl-input" value="5"/></div>
            <div><label class="shl-label">Avg Age — Contract Workshop (days)</label><input id="ar_avg_age_cw" type="number" class="shl-input" value="2"/></div>
            <div><label class="shl-label">CWS AC Installation</label><input id="ar_cws_ac" type="number" class="shl-input" value="2108"/></div>
            <div><label class="shl-label">CWS Other Complaints</label><input id="ar_cws_other" type="number" class="shl-input" value="5041"/></div>
          </div>
        </div>

        <!-- 1.2 Warranty Analysis -->
        <div class="mb-6">
          <p class="text-yellow-300/90 text-xs uppercase tracking-widest mb-2 font-bold">1.2 Cases vs. Warranty Analysis</p>
          <div class="overflow-x-auto data-surface rounded-xl">
            <table class="w-full text-sm"><thead><tr>
              <th class="text-left px-4 py-2 min-w-[250px]">Particulars</th>
              <th class="px-3 py-2">AC</th><th class="px-3 py-2">REF</th><th class="px-3 py-2">WD</th>
              <th class="px-3 py-2">WM</th><th class="px-3 py-2">OVEN</th><th class="px-3 py-2">LED</th>
              <th class="px-3 py-2">Total</th>
            </tr></thead><tbody id="arWarrantyBody"></tbody></table>
          </div>
        </div>

        <!-- 1.3 Aging Analysis -->
        <div class="mb-6">
          <p class="text-yellow-300/90 text-xs uppercase tracking-widest mb-2 font-bold">1.3 Cases Aging Analysis</p>
          <div class="overflow-x-auto data-surface rounded-xl">
            <table class="w-full text-sm"><thead><tr>
              <th class="text-left px-4 py-2 min-w-[150px]">Particulars</th>
              <th class="px-3 py-2">In-House Cases</th><th class="px-3 py-2">In-House %</th>
              <th class="px-3 py-2">Contract Cases</th><th class="px-3 py-2">Contract %</th>
            </tr></thead><tbody id="arAgingBody"></tbody></table>
          </div>
        </div>

        <!-- 1.4 Units/Parts Replaced -->
        <div class="mb-6">
          <p class="text-yellow-300/90 text-xs uppercase tracking-widest mb-2 font-bold">1.4 Division-wise Parts and Units Replacement</p>
          <div class="overflow-x-auto data-surface rounded-xl">
            <table class="w-full text-sm"><thead><tr>
              <th class="px-3 py-2">Sr.</th>
              <th class="text-left px-4 py-2 min-w-[160px]">Particulars</th>
              <th class="px-3 py-2">AC</th><th class="px-3 py-2">REF</th><th class="px-3 py-2">WD</th>
              <th class="px-3 py-2">WM</th><th class="px-3 py-2">OVEN</th><th class="px-3 py-2">LED</th>
              <th class="px-3 py-2">Total</th>
            </tr></thead><tbody id="arReplacedBody"></tbody></table>
          </div>
        </div>

        <!-- 1.5 Revenue -->
        <div class="mb-2">
          <p class="text-yellow-300/90 text-xs uppercase tracking-widest mb-2 font-bold">1.5 Revenue for the Period</p>
          <div class="overflow-x-auto data-surface rounded-xl">
            <table class="w-full text-sm"><thead><tr>
              <th class="text-left px-4 py-2 min-w-[220px]">Particulars</th>
              <th class="px-3 py-2">Current Period</th><th class="px-3 py-2">Previous Period</th>
              <th class="px-3 py-2">Variance</th><th class="px-3 py-2">Variance %</th>
            </tr></thead><tbody id="arRevenueBody"></tbody></table>
          </div>
        </div>
      </div>

      <!-- ── OBSERVATIONS ── -->
      <div id="ar-tab-obs" class="ar-pane hidden">
        <div class="flex items-center gap-3 mb-4">
          <p class="text-xs text-blue-100/60 uppercase tracking-widest flex-1">Add, remove or reorder observations. Toggle to include/exclude from report.</p>
          <button id="arAddObsBtn" class="btn-accent text-sm py-2 px-4">+ Add Observation</button>
        </div>
        <div id="arObsList" class="space-y-3"></div>
      </div>

      <!-- ── CONCLUSION ── -->
      <div id="ar-tab-conclusion" class="ar-pane hidden">
        <div class="grid sm:grid-cols-2 gap-4 mb-6">
          <div><label class="shl-label">Total Audit Queries</label><input id="ar_total_queries" type="number" class="shl-input" value="8"/></div>
          <div><label class="shl-label">Open</label><input id="ar_open" type="number" class="shl-input" value="0"/></div>
          <div><label class="shl-label">In Process</label><input id="ar_in_process" type="number" class="shl-input" value="3"/></div>
          <div><label class="shl-label">Closed</label><input id="ar_closed" type="number" class="shl-input" value="5"/></div>
          <div><label class="shl-label">Revenue Target (Audit Period)</label><input id="ar_rev_target" class="shl-input" value="N/A"/></div>
          <div><label class="shl-label">Target Achieved (Rs.)</label><input id="ar_target_achieved" class="shl-input" value="1,095,254"/></div>
          <div><label class="shl-label">Invoices Cleared as at</label><input id="ar_inv_cleared_date" class="shl-input" value="22.04.2026"/></div>
          <div><label class="shl-label">Invoices Cleared Amount (Rs.)</label><input id="ar_inv_cleared" class="shl-input" value="649,609"/></div>
          <div><label class="shl-label">Total Complaints</label><input id="ar_total_complaints" type="number" class="shl-input" value="5031"/></div>
          <div><label class="shl-label">Cancelled</label><input id="ar_cancelled" type="number" class="shl-input" value="159"/></div>
          <div><label class="shl-label">No. of Units Replaced</label><input id="ar_units_replaced" type="number" class="shl-input" value="2"/></div>
          <div><label class="shl-label">Pending for Resolution</label><input id="ar_pending" type="number" class="shl-input" value="17"/></div>
        </div>
        <p class="text-yellow-300/90 text-xs uppercase tracking-widest mb-2 font-bold">Audit Query Summary</p>
        <div id="arQueriesContainer" class="space-y-2 mb-3">
          <!-- rows added dynamically -->
        </div>
        <button id="arAddQueryBtn" class="btn-ghost text-xs py-2 px-4">+ Add Query Row</button>
      </div>
    </section>
  </div><!-- end page-audit-report -->

"""
content = content.replace('<!-- DETAIL MODAL -->', PAGE + '<!-- DETAIL MODAL -->')

# ── 4. ROUTER ─────────────────────────────────────────────────────────────────
content = content.replace(
    '  "/shl-report-db":         "page-shl-db",',
    '  "/shl-report-db":         "page-shl-db",\n  "/audit-report":           "page-audit-report",'
)
content = content.replace(
    'const ALL_PAGES = "#page-home, #page-projects, #page-contact, #page-app, #page-c-grade, #page-expense, #page-cash-cleaner, #page-cs-notif, #page-shl-db";',
    'const ALL_PAGES = "#page-home, #page-projects, #page-contact, #page-app, #page-c-grade, #page-expense, #page-cash-cleaner, #page-cs-notif, #page-shl-db, #page-audit-report";'
)

# ── 5. CSS ────────────────────────────────────────────────────────────────────
AR_CSS = """
  /* ===== Audit Report Generator ===== */
  .ar-pane {}
  .ar-obs-card { border:1px solid rgba(255,255,255,.10); border-radius:14px; background:rgba(255,255,255,.04); overflow:hidden; }
  .ar-obs-head { display:flex; align-items:center; gap:10px; padding:12px 16px; cursor:pointer; }
  .ar-obs-body { padding:14px 16px; border-top:1px solid rgba(255,255,255,.08); display:none; }
  .ar-obs-body.open { display:block; }
  .ar-obs-title { font-size:13px; font-weight:600; color:#efe9dc; flex:1; }
  .ar-obs-toggle { display:flex; align-items:center; gap:6px; }
  .ar-textarea { width:100%; padding:8px 10px; border-radius:8px; border:1px solid rgba(255,255,255,.12);
                 background:rgba(255,255,255,.06); color:#efe9dc; font-size:12px; resize:vertical;
                 outline:none; min-height:70px; }
  .ar-textarea:focus { border-color:rgba(205,185,142,.55); }
  .ar-select { padding:6px 10px; border-radius:8px; border:1px solid rgba(255,255,255,.12);
               background:rgba(30,25,15,.9); color:#efe9dc; font-size:12px; outline:none; }
  .ar-check { width:16px; height:16px; cursor:pointer; }
  .ar-query-row { display:grid; grid-template-columns:1fr auto auto auto; gap:8px; align-items:center; }
"""
idx = content.find('</style>', content.find('<style>'))
content = content[:idx] + AR_CSS + content[idx:]

with open('InterAudit-P1.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Phase 1 done')
