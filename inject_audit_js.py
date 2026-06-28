JS = r"""
  // =====================================================================
  // AUDIT REPORT GENERATOR
  // =====================================================================
  (function () {
    'use strict';

    /* ── constants ─────────────────────────────────────────────── */
    const PRODS = ['AC','REF','WD','WM','OVEN','LED'];

    const CHECKLIST = [
      ["Cutoff Date for Notification taken at",""],
      ["Cutoff Date of Last Stock Taking conducted at",""],
      ["Verification of Opening Stock","Not Conducted"],
      ["Stock Count performed on",""],
      ["Counting Sheets Obtained","Yes"],
      ["Counting Sheets Signed by Auditee","Yes"],
      ["Physical count of A-Grade Stock – Difference noted",""],
      ["Verification of C-Grade Stock – SAP vs Physical",""],
      ["C-Grade Stock Uploaded on Lotus Notes","Yes"],
      ["C Pair Not Updated in SAP",""],
      ["Petty Cash Balance as per SAP",""],
      ["Physical Cash Count as on",""],
      ["Denomination-wise Cash Count obtained","Yes"],
      ["Cash Count Form Signed","Yes"],
      ["Last Cash Count Form Verified",""],
      ["Differences in Cash Count if any",""],
      ["Cleared CS Invoices Verified","Yes"],
      ["Outstanding CS Invoices Reviewed","Yes"],
      ["Amount of Overdue CS Invoices",""],
      ["PDC/Cheques in Hand Verified","Yes"],
      ["MIGO Status Verified","Yes"],
      ["Pending MIGOs Discussed","Yes"],
      ["BSR (Business Summary Report) Reviewed","Yes"],
      ["Latest Notification Discrepancy Report Obtained","Yes"],
      ["Discrepancy Trend Discussed","Yes"],
      ["Warranty Analysis Obtained from SAP","Yes"],
      ["Warranty Ratio reviewed for anomalies","Yes"],
      ["Parts Replacement Records Reviewed","Yes"],
      ["Units Replacement Records Reviewed","Yes"],
      ["Aging Analysis Obtained","Yes"],
      ["Cases Pending Above 10 Days reviewed","Yes"],
      ["Revenue Data for Current Period","Obtained"],
      ["Revenue Data for Previous Period","Obtained"],
      ["Variance Analysis performed","Yes"],
      ["GL Expense Report Obtained","Yes"],
      ["Abnormal Expense Items Noted",""],
      ["Technician Count Verified","Yes"],
      ["CWS Vendor List Reviewed","Yes"],
      ["Installation Complaints Segregated","Yes"],
      ["Cases per Day computed","Yes"],
      ["Average Age computed","Yes"],
      ["Exit Meeting conducted","Yes"],
    ]

    const DEF_NOTIF = {
      total:     [2697,871,81,42,15,38],
      cancelled: [11,9,4,5,1,0],
      resolved:  [2677,852,77,37,14,38],
    };
    const DEF_WARRANTY = {
      withW:    [2278,150,38,10,9,10],
      partialW: [74,453,2,0,0,3],
      withoutW: [56,73,14,18,2,2],
    };
    const DEF_AGING = [
      {label:'0 – 3 Days',  ih: 1611, cw: 3089},
      {label:'4 – 7 Days',  ih: 154,  cw: 54},
      {label:'8 – 10 Days', ih: 64,   cw: 42},
      {label:'Above 10 Days',ih:17,   cw: 3},
    ];
    const DEF_REPLACED = {
      units: [2,0,0,0,0,0],
      parts: [0,0,0,0,0,0],
    };
    const DEF_REVENUE = [
      {label:'Service Revenue',  cur:1095254, prev:2078984},
      {label:'Parts Revenue',    cur:198540,  prev:280320},
      {label:'Total Revenue',    cur:1293794, prev:2359304},
    ];

    const OBS_DEFAULTS = [
      {id:'o1', title:'Notifications Related Discrepancies', enabled:true,
       observation:'During the audit, notification discrepancies were observed between the SAP database and the latest discrepancy report. Some notifications were found cancelled or resolved without proper documentary evidence.',
       implication:'This may indicate improper handling of customer complaints and could affect the accuracy of complaint resolution statistics.',
       risk:'Medium', recommendation:'All notification discrepancies should be investigated and justified. Notification cancellations must be supported by valid reasons and approved by the Service Center In-Charge.',
       responsibility_primary:'Service Center In-Charge', responsibility_secondary:'Regional Service Manager',
       target_date:'', followup:''},
      {id:'o2', title:'CS Invoices / Collection Not Cleared', enabled:true,
       observation:'Customer Service invoices raised during the audit period were not fully cleared as at the cutoff date. Outstanding amount of Rs. [AMOUNT] remains pending for collection/clearance.',
       implication:'Uncleared invoices affect cash flow and may indicate issues with collection efficiency or invoice accuracy.',
       risk:'High', recommendation:'All CS invoices should be cleared within 30 days of generation. Outstanding invoices should be followed up immediately with customers. A weekly reconciliation of cleared vs. pending invoices should be maintained.',
       responsibility_primary:'Service Center In-Charge', responsibility_secondary:'Finance Officer',
       target_date:'', followup:''},
      {id:'o3', title:'A/B/C-pair Stock Difference', enabled:true,
       observation:'During the physical count of A-Grade stock, differences were noted between the SAP system balance and the physical count. Details are provided in Annexure 1.2.',
       implication:'Stock differences may result in incorrect inventory valuations and potential financial losses.',
       risk:'High', recommendation:'An immediate investigation should be conducted to reconcile stock differences. All movements must be recorded in SAP on a real-time basis. Monthly stock counts should be performed and documented.',
       responsibility_primary:'Service Center In-Charge', responsibility_secondary:'Warehouse Staff',
       target_date:'', followup:''},
      {id:'o4', title:'C Pair Not Uploaded', enabled:true,
       observation:'Several C-pair items were found not uploaded on the designated system (Lotus Notes) as required by company policy. These items had been accumulated at the service center without proper recording.',
       implication:'Failure to upload C-pair items leads to inventory discrepancies and potential misuse of returned/defective components.',
       risk:'Medium', recommendation:'All C-pair items must be uploaded within 24 hours of receipt. The Service Center In-Charge should perform weekly verification of C-pair uploads.',
       responsibility_primary:'Service Center In-Charge', responsibility_secondary:'',
       target_date:'', followup:''},
      {id:'o5', title:'Pending Notifications', enabled:true,
       observation:'As at the cutoff date, [NUMBER] notifications were pending resolution for more than 10 days. Details per product category are provided in the Aging Analysis (Section 1.3).',
       implication:'Pending notifications beyond stipulated turnaround times indicate service delivery delays affecting customer satisfaction.',
       risk:'Medium', recommendation:'All pending notifications beyond 10 days should be escalated immediately. Daily monitoring reports should be reviewed by the Service Center In-Charge to ensure timely resolution.',
       responsibility_primary:'Service Center In-Charge', responsibility_secondary:'Workshop Supervisor',
       target_date:'', followup:''},
      {id:'o6', title:'Physical Cash Count', enabled:true,
       observation:'A physical cash count was conducted at the service center. The following differences were observed between SAP cash balance and physical cash on hand:\n\nSAP Balance: Rs. [SAP_AMOUNT]\nPhysical Count: Rs. [PHYSICAL_AMOUNT]\nDifference: Rs. [DIFFERENCE]',
       implication:'Cash count differences may indicate unauthorized transactions or inadequate cash management controls.',
       risk:'High', recommendation:'All cash differences must be immediately investigated and reconciled. Daily cash counts should be performed and signed off by the Service Center In-Charge. Cash should be deposited on a daily basis.',
       responsibility_primary:'Service Center In-Charge', responsibility_secondary:'Cashier',
       target_date:'', followup:''},
      {id:'o7', title:'Expenses Analysis', enabled:true,
       observation:'A review of petty cash expenses for the audit period was performed. Certain GL codes showed significant variances compared to the previous period. Abnormal items were noted in [GL_CODES].',
       implication:'Unexplained expense variances may indicate unauthorized or fictitious expenditures.',
       risk:'Medium', recommendation:'All expense variances above 20% of the previous period should be adequately explained and documented. Petty cash vouchers should be verified against supporting documents.',
       responsibility_primary:'Service Center In-Charge', responsibility_secondary:'Finance Officer',
       target_date:'', followup:''},
      {id:'o8', title:'Pending MIGO', enabled:true,
       observation:'MIGO (Material Issue Goods Out) transactions were found pending in SAP. A total of [NUMBER] MIGOs remain unprocessed as at the cutoff date.',
       implication:'Pending MIGOs result in inaccurate inventory records and may affect the accuracy of stock reports generated from SAP.',
       risk:'Medium', recommendation:'All MIGO transactions should be processed on the same day as material issuance. A weekly review of pending MIGOs should be conducted and escalated to the Regional Manager if not resolved within 3 days.',
       responsibility_primary:'Service Center In-Charge', responsibility_secondary:'Warehouse Staff',
       target_date:'', followup:''},
    ];

    /* ── state ─────────────────────────────────────────────── */
    let arNotifData = JSON.parse(JSON.stringify(DEF_NOTIF));
    let arWarrantyData = JSON.parse(JSON.stringify(DEF_WARRANTY));
    let arAgingData = JSON.parse(JSON.stringify(DEF_AGING));
    let arReplacedData = JSON.parse(JSON.stringify(DEF_REPLACED));
    let arRevenueData = JSON.parse(JSON.stringify(DEF_REVENUE));
    let arObservations = JSON.parse(JSON.stringify(OBS_DEFAULTS));
    let arObsCounter = OBS_DEFAULTS.length;

    /* ── helpers ─────────────────────────────────────────────── */
    function v(id) { return $('#'+id).val() || ''; }
    function n(id) { return parseFloat($('#'+id).val()) || 0; }
    function fmt(x) {
      if (x === null || x === undefined || x === '') return '-';
      const num = parseFloat(x);
      if (isNaN(num)) return x;
      return num.toLocaleString('en-PK');
    }
    function pct(num, den) {
      if (!den) return '-';
      return (num/den*100).toFixed(1)+'%';
    }

    /* ── init checklist ─────────────────────────────────────────── */
    function buildChecklist() {
      const tbody = $('#arChecklistBody');
      tbody.empty();
      CHECKLIST.forEach(([particulars, defaultRemark], i) => {
        tbody.append(`<tr>
          <td class="text-center px-3 py-1.5 text-xs text-blue-100/60">${i+1}</td>
          <td class="px-4 py-1.5 text-sm text-blue-100/90">${particulars}</td>
          <td class="px-3 py-1 text-center">
            <input class="shl-input-sm ar-cl-remark" data-idx="${i}"
              value="${defaultRemark}" style="width:160px;text-align:center;"/>
          </td>
        </tr>`);
      });
    }

    /* ── init analysis tables ─────────────────────────────────── */
    function buildNotifTable() {
      const rows = [
        {label:'Total Notifications', key:'total'},
        {label:'Cancelled',           key:'cancelled'},
        {label:'Resolved (Net)',       key:'resolved'},
        {label:'Pending',             key:null},
      ];
      const tbody = $('#arNotifBody'); tbody.empty();
      rows.forEach(r => {
        let cells = '';
        let tot = 0;
        PRODS.forEach((p,i) => {
          const val = r.key ? (arNotifData[r.key]?.[i] ?? 0) : (arNotifData.total[i] - arNotifData.resolved[i] - arNotifData.cancelled[i]);
          tot += val;
          if (r.key) {
            cells += `<td class="text-center px-2 py-1"><input class="shl-input-sm ar-notif-inp" data-key="${r.key}" data-idx="${i}" value="${val}" style="width:58px;text-align:center;"/></td>`;
          } else {
            cells += `<td class="text-center px-2 py-1 ar-notif-pending" data-idx="${i}">${val}</td>`;
          }
        });
        tbody.append(`<tr>
          <td class="px-4 py-1.5 text-sm">${r.label}</td>
          ${cells}
          <td class="text-center px-3 py-1 font-semibold ar-notif-rowtotal" data-key="${r.key || 'pending'}">${fmt(tot)}</td>
        </tr>`);
      });
    }

    function buildWarrantyTable() {
      const rows = [
        {label:'Cases With Warranty',           key:'withW'},
        {label:'Cases With Partial Warranty',   key:'partialW'},
        {label:'Cases Without Warranty',        key:'withoutW'},
        {label:'Total',                         key:null},
      ];
      const tbody = $('#arWarrantyBody'); tbody.empty();
      rows.forEach(r => {
        let cells = ''; let tot = 0;
        PRODS.forEach((p,i) => {
          const val = r.key ? (arWarrantyData[r.key]?.[i] ?? 0)
                            : ((arWarrantyData.withW[i]||0)+(arWarrantyData.partialW[i]||0)+(arWarrantyData.withoutW[i]||0));
          tot += val;
          if (r.key) {
            cells += `<td class="text-center px-2 py-1"><input class="shl-input-sm ar-war-inp" data-key="${r.key}" data-idx="${i}" value="${val}" style="width:58px;text-align:center;"/></td>`;
          } else {
            cells += `<td class="text-center px-2 py-1 ar-war-total" data-idx="${i}">${fmt(val)}</td>`;
          }
        });
        tbody.append(`<tr>
          <td class="px-4 py-1.5 text-sm">${r.label}</td>
          ${cells}
          <td class="text-center px-3 py-1 font-semibold">${fmt(tot)}</td>
        </tr>`);
      });
    }

    function buildAgingTable() {
      const tbody = $('#arAgingBody'); tbody.empty();
      let totIH = 0, totCW = 0;
      const allIH = arAgingData.reduce((s,r) => s+r.ih, 0);
      const allCW = arAgingData.reduce((s,r) => s+r.cw, 0);
      arAgingData.forEach((r,i) => {
        totIH += r.ih; totCW += r.cw;
        tbody.append(`<tr>
          <td class="px-4 py-1.5 text-sm">${r.label}</td>
          <td class="text-center px-3 py-1">
            <input class="shl-input-sm ar-aging-inp" data-i="${i}" data-f="ih" value="${r.ih}" style="width:70px;text-align:center;"/>
          </td>
          <td class="text-center px-3 py-1 ar-aging-ihpct" data-i="${i}">${pct(r.ih, allIH)}</td>
          <td class="text-center px-3 py-1">
            <input class="shl-input-sm ar-aging-inp" data-i="${i}" data-f="cw" value="${r.cw}" style="width:70px;text-align:center;"/>
          </td>
          <td class="text-center px-3 py-1 ar-aging-cwpct" data-i="${i}">${pct(r.cw, allCW)}</td>
        </tr>`);
      });
      tbody.append(`<tr class="font-semibold">
        <td class="px-4 py-2">Total</td>
        <td class="text-center px-3 py-2" id="arAgingTotIH">${fmt(totIH)}</td>
        <td class="text-center px-3 py-2">100%</td>
        <td class="text-center px-3 py-2" id="arAgingTotCW">${fmt(totCW)}</td>
        <td class="text-center px-3 py-2">100%</td>
      </tr>`);
    }

    function buildReplacedTable() {
      const rows = [{label:'Units Replaced',key:'units'},{label:'Parts Replaced',key:'parts'}];
      const tbody = $('#arReplacedBody'); tbody.empty();
      rows.forEach((r,ri) => {
        let cells = ''; let tot = 0;
        PRODS.forEach((p,i) => {
          const val = arReplacedData[r.key]?.[i] ?? 0; tot += val;
          cells += `<td class="text-center px-2 py-1"><input class="shl-input-sm ar-rep-inp" data-key="${r.key}" data-idx="${i}" value="${val}" style="width:58px;text-align:center;"/></td>`;
        });
        tbody.append(`<tr>
          <td class="text-center px-3 py-1.5">${ri+1}</td>
          <td class="px-4 py-1.5 text-sm">${r.label}</td>
          ${cells}
          <td class="text-center px-3 py-1 font-semibold">${fmt(tot)}</td>
        </tr>`);
      });
    }

    function buildRevenueTable() {
      const tbody = $('#arRevenueBody'); tbody.empty();
      arRevenueData.forEach((r,i) => {
        const variance = r.cur - r.prev;
        const varPct = r.prev ? ((variance / r.prev)*100).toFixed(1)+'%' : '-';
        tbody.append(`<tr>
          <td class="px-4 py-1.5 text-sm">${r.label}</td>
          <td class="text-center px-3 py-1"><input class="shl-input-sm ar-rev-inp" data-i="${i}" data-f="cur" value="${r.cur}" style="width:90px;text-align:center;"/></td>
          <td class="text-center px-3 py-1"><input class="shl-input-sm ar-rev-inp" data-i="${i}" data-f="prev" value="${r.prev}" style="width:90px;text-align:center;"/></td>
          <td class="text-center px-3 py-1 ar-rev-var" data-i="${i}" style="color:${variance<0?'#f87171':'#86efac'}">${fmt(variance)}</td>
          <td class="text-center px-3 py-1 ar-rev-pct" data-i="${i}" style="color:${variance<0?'#f87171':'#86efac'}">${varPct}</td>
        </tr>`);
      });
    }

    function rebuildAllAnalysis() {
      buildNotifTable(); buildWarrantyTable(); buildAgingTable(); buildReplacedTable(); buildRevenueTable();
    }

    /* ── observations ─────────────────────────────────────────── */
    function buildObsCard(obs) {
      const riskColor = {High:'#f87171',Medium:'#fbbf24',Low:'#86efac'}[obs.risk] || '#94a3b8';
      return `
        <div class="ar-obs-card" id="obscard-${obs.id}">
          <div class="ar-obs-head" data-obsid="${obs.id}">
            <input type="checkbox" class="ar-check ar-obs-enabled" data-obsid="${obs.id}" ${obs.enabled?'checked':''} title="Include in report"/>
            <div class="ar-obs-title" contenteditable="true" data-obsid="${obs.id}" spellcheck="false">${obs.title}</div>
            <span class="text-xs px-2 py-0.5 rounded-full font-semibold" style="color:${riskColor};border:1px solid ${riskColor}40">${obs.risk}</span>
            <svg class="w-4 h-4 text-blue-100/50 ar-obs-chevron" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
          <div class="ar-obs-body" id="obsbody-${obs.id}">
            <div class="grid sm:grid-cols-2 gap-3">
              <div class="sm:col-span-2">
                <label class="shl-label">Observation</label>
                <textarea class="ar-textarea ar-obs-field" data-obsid="${obs.id}" data-field="observation">${obs.observation}</textarea>
              </div>
              <div class="sm:col-span-2">
                <label class="shl-label">Implication</label>
                <textarea class="ar-textarea ar-obs-field" data-obsid="${obs.id}" data-field="implication" style="min-height:50px">${obs.implication}</textarea>
              </div>
              <div>
                <label class="shl-label">Risk Rating</label>
                <select class="ar-select ar-obs-field" data-obsid="${obs.id}" data-field="risk" style="width:100%">
                  <option ${obs.risk==='High'?'selected':''}>High</option>
                  <option ${obs.risk==='Medium'?'selected':''}>Medium</option>
                  <option ${obs.risk==='Low'?'selected':''}>Low</option>
                </select>
              </div>
              <div>
                <label class="shl-label">Follow-up Status</label>
                <input class="shl-input ar-obs-field" data-obsid="${obs.id}" data-field="followup" value="${obs.followup}" placeholder="Open / In Process / Closed"/>
              </div>
              <div class="sm:col-span-2">
                <label class="shl-label">Recommendation</label>
                <textarea class="ar-textarea ar-obs-field" data-obsid="${obs.id}" data-field="recommendation">${obs.recommendation}</textarea>
              </div>
              <div>
                <label class="shl-label">Responsibility — Primary</label>
                <input class="shl-input ar-obs-field" data-obsid="${obs.id}" data-field="responsibility_primary" value="${obs.responsibility_primary}"/>
              </div>
              <div>
                <label class="shl-label">Responsibility — Secondary</label>
                <input class="shl-input ar-obs-field" data-obsid="${obs.id}" data-field="responsibility_secondary" value="${obs.responsibility_secondary}"/>
              </div>
              <div>
                <label class="shl-label">Target Date</label>
                <input class="shl-input ar-obs-field" data-obsid="${obs.id}" data-field="target_date" value="${obs.target_date}" placeholder="e.g. 30.06.2026"/>
              </div>
              <div class="flex items-end">
                <button class="btn-ghost text-xs py-2 px-4 w-full ar-del-obs" data-obsid="${obs.id}" style="border-color:rgba(248,113,113,.4);color:#f87171">Remove</button>
              </div>
            </div>
          </div>
        </div>`;
    }

    function renderObsList() {
      const $list = $('#arObsList'); $list.empty();
      arObservations.forEach(obs => $list.append(buildObsCard(obs)));
    }

    function getObs(id) { return arObservations.find(o => o.id === id); }

    /* ── conclusion query rows ─────────────────────────────────── */
    let arQueries = [
      {title:'Notifications Related Discrepancies', status:'Closed'},
      {title:'CS Invoices/Collection Not Cleared', status:'In Process'},
      {title:'A/B/C-pair Stock Difference', status:'Closed'},
      {title:'C Pair Not Uploaded', status:'Closed'},
      {title:'Pending Notifications', status:'In Process'},
      {title:'Physical Cash Count', status:'Closed'},
      {title:'Expenses Analysis', status:'In Process'},
      {title:'Pending MIGO', status:'Closed'},
    ];
    function renderQueryRows() {
      const $c = $('#arQueriesContainer'); $c.empty();
      arQueries.forEach((q,i) => {
        $c.append(`<div class="ar-query-row">
          <input class="shl-input ar-qr-title" data-qi="${i}" value="${q.title}" placeholder="Query title"/>
          <select class="ar-select ar-qr-status" data-qi="${i}" style="width:140px">
            <option ${q.status==='Open'?'selected':''}>Open</option>
            <option ${q.status==='In Process'?'selected':''}>In Process</option>
            <option ${q.status==='Closed'?'selected':''}>Closed</option>
          </select>
          <button class="btn-ghost text-xs py-2 px-3 ar-del-query" data-qi="${i}" style="border-color:rgba(248,113,113,.3);color:#f87171">✕</button>
        </div>`);
      });
    }

    /* ── Excel auto-extraction ─────────────────────────────────── */
    function extractFromExcel(workbook) {
      let extracted = [];

      // Try Notification Analysis sheet
      const nSheet = workbook.Sheets['Notification Analysis'] || workbook.Sheets['DataBase'];
      if (nSheet) {
        const data = XLSX.utils.sheet_to_json(nSheet, {header:1, defval:''});
        // Look for rows containing notification counts by product
        // (flexible - try to find header row with AC, REF, etc.)
        let hRow = -1;
        for (let r = 0; r < Math.min(20, data.length); r++) {
          const row = data[r].map(c => String(c||'').trim().toUpperCase());
          if (row.includes('AC') || row.includes('REF')) { hRow = r; break; }
        }
        if (hRow >= 0) {
          const headers = data[hRow].map(c => String(c||'').trim().toUpperCase());
          const colIdx = {};
          ['AC','REF','WD','WM','OVEN','LED'].forEach(p => {
            const ci = headers.indexOf(p);
            if (ci >= 0) colIdx[p] = ci;
          });
          if (Object.keys(colIdx).length >= 4) {
            // Scan next rows for totals, cancelled, resolved
            for (let r = hRow+1; r < Math.min(hRow+20, data.length); r++) {
              const rowLabel = String(data[r][0]||data[r][1]||'').toLowerCase();
              const vals = PRODS.map(p => parseInt(colIdx[p] !== undefined ? data[r][colIdx[p]] : 0) || 0);
              if (rowLabel.includes('total') || rowLabel.includes('opened')) arNotifData.total = vals;
              if (rowLabel.includes('cancel')) arNotifData.cancelled = vals;
              if (rowLabel.includes('resolv') || rowLabel.includes('closed')) arNotifData.resolved = vals;
            }
            extracted.push('Notification Analysis');
          }
        }
      }

      // Try Warranty Analysis sheet
      const wSheet = workbook.Sheets['Warranty Analysis'];
      if (wSheet) {
        const data = XLSX.utils.sheet_to_json(wSheet, {header:1, defval:''});
        let hRow = -1;
        for (let r = 0; r < Math.min(15, data.length); r++) {
          const row = data[r].map(c => String(c||'').trim().toUpperCase());
          if (row.includes('AC') || row.includes('REF')) { hRow = r; break; }
        }
        if (hRow >= 0) {
          const headers = data[hRow].map(c => String(c||'').trim().toUpperCase());
          const colIdx = {};
          PRODS.forEach(p => { const ci = headers.indexOf(p); if (ci >= 0) colIdx[p] = ci; });
          if (Object.keys(colIdx).length >= 4) {
            for (let r = hRow+1; r < Math.min(hRow+10, data.length); r++) {
              const rowLabel = String(data[r][0]||data[r][1]||'').toLowerCase();
              const vals = PRODS.map(p => parseInt(colIdx[p] !== undefined ? data[r][colIdx[p]] : 0) || 0);
              if (rowLabel.includes('with warrant') && !rowLabel.includes('partial')) arWarrantyData.withW = vals;
              if (rowLabel.includes('partial')) arWarrantyData.partialW = vals;
              if (rowLabel.includes('without')) arWarrantyData.withoutW = vals;
            }
            extracted.push('Warranty Analysis');
          }
        }
      }

      // Try Revenue sheet
      const revSheet = workbook.Sheets['Revenue'] || workbook.Sheets['Sales Analysis'];
      if (revSheet) {
        const data = XLSX.utils.sheet_to_json(revSheet, {header:1, defval:''});
        const newRev = [];
        for (let r = 0; r < Math.min(30, data.length); r++) {
          const label = String(data[r][0]||data[r][1]||'').trim();
          if (!label) continue;
          const cur = parseFloat(data[r][2]) || parseFloat(data[r][3]) || 0;
          const prev = parseFloat(data[r][3]) || parseFloat(data[r][4]) || 0;
          if ((label.toLowerCase().includes('revenue') || label.toLowerCase().includes('total')) && (cur || prev)) {
            newRev.push({label, cur, prev});
          }
        }
        if (newRev.length) { arRevenueData = newRev; extracted.push('Revenue'); }
      }

      // Try Notifi Aging sheet
      const agSheet = workbook.Sheets['Notifi Aging'] || workbook.Sheets['Aging'];
      if (agSheet) {
        const data = XLSX.utils.sheet_to_json(agSheet, {header:1, defval:''});
        const newAging = [];
        const labels = ['0 – 3 Days','4 – 7 Days','8 – 10 Days','Above 10 Days'];
        for (let r = 0; r < Math.min(30, data.length); r++) {
          const rowStr = data[r].map(c => String(c||'')).join('|');
          if (/0.*3|days/i.test(rowStr) || /4.*7/i.test(rowStr) || /8.*10/i.test(rowStr) || /above.*10|10.*above/i.test(rowStr)) {
            const nums = data[r].filter(c => parseFloat(c) > 0);
            if (nums.length >= 2) {
              newAging.push({label: labels[newAging.length] || rowStr.split('|')[0], ih: parseFloat(nums[0])||0, cw: parseFloat(nums[1])||0});
            }
          }
        }
        if (newAging.length >= 3) { arAgingData = newAging.slice(0,4); extracted.push('Aging'); }
      }

      return extracted;
    }

    /* ── Excel upload handler ──────────────────────────────────── */
    $('#arExcelInput').on('change', function(e) {
      const file = e.target.files[0]; if (!file) return;
      const reader = new FileReader();
      reader.onload = function(ev) {
        try {
          const wb = XLSX.read(ev.target.result, {type:'array'});
          const extracted = extractFromExcel(wb);
          rebuildAllAnalysis();
          const msg = extracted.length
            ? `Extracted: ${extracted.join(', ')}`
            : 'File loaded — no matching sheets found; check Analysis tab.';
          $('#arExcelBadge').text(file.name + ' — ' + msg).css('color','#86efac');
        } catch(err) {
          $('#arExcelBadge').text('Read error: '+err.message).css('color','#f87171');
        }
      };
      reader.readAsArrayBuffer(file);
    });

    /* ── live update handlers ──────────────────────────────────── */
    $(document).on('input change', '#page-audit-report', function(e) {
      const $t = $(e.target);

      if ($t.hasClass('ar-notif-inp')) {
        const key = $t.data('key'), idx = parseInt($t.data('idx'));
        arNotifData[key][idx] = parseInt($t.val()) || 0;
        // Update pending cells
        PRODS.forEach((_,i) => {
          const pending = arNotifData.total[i] - arNotifData.resolved[i] - arNotifData.cancelled[i];
          $(`.ar-notif-pending[data-idx="${i}"]`).text(pending);
        });
        return;
      }
      if ($t.hasClass('ar-war-inp')) {
        const key = $t.data('key'), idx = parseInt($t.data('idx'));
        arWarrantyData[key][idx] = parseInt($t.val()) || 0;
        PRODS.forEach((_,i) => {
          const tot = (arWarrantyData.withW[i]||0)+(arWarrantyData.partialW[i]||0)+(arWarrantyData.withoutW[i]||0);
          $(`.ar-war-total[data-idx="${i}"]`).text(fmt(tot));
        });
        return;
      }
      if ($t.hasClass('ar-aging-inp')) {
        const i = parseInt($t.data('i')), f = $t.data('f');
        arAgingData[i][f] = parseInt($t.val()) || 0;
        const allIH = arAgingData.reduce((s,r)=>s+r.ih,0);
        const allCW = arAgingData.reduce((s,r)=>s+r.cw,0);
        $(`.ar-aging-ihpct[data-i="${i}"]`).text(pct(arAgingData[i].ih, allIH));
        $(`.ar-aging-cwpct[data-i="${i}"]`).text(pct(arAgingData[i].cw, allCW));
        $('#arAgingTotIH').text(fmt(allIH));
        $('#arAgingTotCW').text(fmt(allCW));
        return;
      }
      if ($t.hasClass('ar-rev-inp')) {
        const i = parseInt($t.data('i')), f = $t.data('f');
        arRevenueData[i][f] = parseFloat($t.val()) || 0;
        const variance = arRevenueData[i].cur - arRevenueData[i].prev;
        const varPct = arRevenueData[i].prev ? ((variance/arRevenueData[i].prev)*100).toFixed(1)+'%' : '-';
        const color = variance < 0 ? '#f87171' : '#86efac';
        $(`.ar-rev-var[data-i="${i}"]`).text(fmt(variance)).css('color',color);
        $(`.ar-rev-pct[data-i="${i}"]`).text(varPct).css('color',color);
        return;
      }
      if ($t.hasClass('ar-obs-field')) {
        const obs = getObs($t.data('obsid'));
        if (obs) obs[$t.data('field')] = $t.val();
        return;
      }
      if ($t.hasClass('ar-qr-title')) {
        const i = parseInt($t.data('qi')); if (arQueries[i]) arQueries[i].title = $t.val();
        return;
      }
      if ($t.hasClass('ar-qr-status')) {
        const i = parseInt($t.data('qi')); if (arQueries[i]) arQueries[i].status = $t.val();
        return;
      }
    });

    // Observation title (contenteditable)
    $(document).on('input', '.ar-obs-title[contenteditable]', function() {
      const id = $(this).data('obsid'), obs = getObs(id);
      if (obs) obs.title = $(this).text();
    });

    // Observation enabled toggle
    $(document).on('change', '.ar-obs-enabled', function() {
      const obs = getObs($(this).data('obsid'));
      if (obs) obs.enabled = $(this).prop('checked');
    });

    // Expand/collapse observation
    $(document).on('click', '.ar-obs-head', function(e) {
      if ($(e.target).hasClass('ar-obs-enabled') || $(e.target).is('[contenteditable]')) return;
      const id = $(this).data('obsid');
      $('#obsbody-'+id).toggleClass('open');
      $(this).find('.ar-obs-chevron').toggleClass('rotate-180');
    });

    // Remove observation
    $(document).on('click', '.ar-del-obs', function(e) {
      e.stopPropagation();
      const id = $(this).data('obsid');
      arObservations = arObservations.filter(o => o.id !== id);
      $('#obscard-'+id).remove();
    });

    // Add observation
    $('#arAddObsBtn').on('click', function() {
      arObsCounter++;
      const newObs = {
        id:'o'+arObsCounter, title:'New Observation '+arObsCounter, enabled:true,
        observation:'', implication:'', risk:'Medium', recommendation:'',
        responsibility_primary:'Service Center In-Charge', responsibility_secondary:'',
        target_date:'', followup:'',
      };
      arObservations.push(newObs);
      $('#arObsList').append(buildObsCard(newObs));
      $('#obsbody-o'+arObsCounter).addClass('open');
    });

    // Add query row
    $('#arAddQueryBtn').on('click', function() {
      arQueries.push({title:'', status:'Open'});
      renderQueryRows();
    });

    // Delete query row
    $(document).on('click', '.ar-del-query', function() {
      const i = parseInt($(this).data('qi'));
      arQueries.splice(i,1);
      renderQueryRows();
    });

    /* ── tabs ─────────────────────────────────────────────── */
    $(document).on('click', '[data-ar-tab]', function() {
      const target = $(this).data('ar-tab');
      $('[data-ar-tab]').removeClass('active');
      $(this).addClass('active');
      $('.ar-pane').addClass('hidden');
      $('#'+target).removeClass('hidden');
    });

    /* ── collect checklist remarks ─────────────────────────────── */
    function getChecklistRemarks() {
      const remarks = [];
      $('.ar-cl-remark').each(function(i) {
        remarks.push($(this).val() || CHECKLIST[i][1]);
      });
      return remarks;
    }

    /* ── generate Word document ────────────────────────────────── */
    function generateReport() {
      if (typeof htmlDocx === 'undefined') {
        alert('html-docx-js library not loaded. Please ensure you are connected to the internet.');
        return;
      }
      const branch = v('ar_branch') || 'Service Center';
      const category = v('ar_category') || 'Service Center';
      const curFrom = v('ar_cur_from');
      const curTo = v('ar_cur_to');
      const prevFrom = v('ar_prev_from');
      const prevTo = v('ar_prev_to');
      const cutoff = v('ar_cutoff');
      const preparedBy = v('ar_prepared_by');
      const reviewedBy = v('ar_reviewed_by');
      const scIncharge = v('ar_sc_incharge');
      const scEmail = v('ar_sc_email');
      const scMobile = v('ar_sc_mobile');
      const technicians = v('ar_technicians');
      const reportDate = v('ar_report_date') || new Date().toLocaleDateString('en-PK');
      const days = n('ar_days') || 120;
      const clRemarks = getChecklistRemarks();

      // Collect current analysis data from inputs
      function notifRow(key) {
        return PRODS.map((_,i) => {
          if (key === 'pending') return arNotifData.total[i] - arNotifData.resolved[i] - arNotifData.cancelled[i];
          return arNotifData[key][i];
        });
      }
      function notifTotal(row) { return row.reduce((s,v)=>s+v,0); }

      const notifTotal_ = notifRow('total');
      const notifCancelled_ = notifRow('cancelled');
      const notifResolved_ = notifRow('resolved');
      const notifPending_ = notifRow('pending');

      const ihCases = n('ar_ih_total');
      const cwCases = n('ar_cw_total');
      const avgAgeIH = n('ar_avg_age_ih');
      const avgAgeCW = n('ar_avg_age_cw');

      // Build analysis tables HTML
      function mkProdTable(title, rows) {
        const prodHdrs = PRODS.map(p => `<th>${p}</th>`).join('');
        const rowsHtml = rows.map(r => {
          const cells = r.vals.map(v => `<td>${fmt(v)}</td>`).join('');
          const total = r.vals.reduce((s,x)=>s+x,0);
          return `<tr><td>${r.label}</td>${cells}<td><b>${fmt(total)}</b></td></tr>`;
        }).join('');
        return `<table><thead><tr><th>${title}</th>${prodHdrs}<th>Total</th></tr></thead><tbody>${rowsHtml}</tbody></table>`;
      }

      const notifTableHtml = mkProdTable('Particulars', [
        {label:'Total Notifications', vals: notifTotal_},
        {label:'Cancelled',           vals: notifCancelled_},
        {label:'Resolved',            vals: notifResolved_},
        {label:'Pending',             vals: notifPending_},
      ]);

      const warrantyTableHtml = mkProdTable('Cases vs. Warranty', [
        {label:'With Warranty',    vals: arWarrantyData.withW},
        {label:'Partial Warranty', vals: arWarrantyData.partialW},
        {label:'Without Warranty', vals: arWarrantyData.withoutW},
      ]);

      const allIH = arAgingData.reduce((s,r)=>s+r.ih,0);
      const allCW = arAgingData.reduce((s,r)=>s+r.cw,0);
      const agingRowsHtml = arAgingData.map(r =>
        `<tr><td>${r.label}</td><td>${fmt(r.ih)}</td><td>${pct(r.ih,allIH)}</td><td>${fmt(r.cw)}</td><td>${pct(r.cw,allCW)}</td></tr>`
      ).join('') + `<tr><td><b>Total</b></td><td><b>${fmt(allIH)}</b></td><td><b>100%</b></td><td><b>${fmt(allCW)}</b></td><td><b>100%</b></td></tr>`;

      const replacedTableHtml = mkProdTable('Replacement', [
        {label:'Units Replaced', vals: arReplacedData.units},
        {label:'Parts Replaced', vals: arReplacedData.parts},
      ]);

      const revenueRowsHtml = arRevenueData.map(r => {
        const variance = r.cur - r.prev;
        const varPct = r.prev ? ((variance/r.prev)*100).toFixed(1)+'%' : '-';
        return `<tr><td>${r.label}</td><td>${fmt(r.cur)}</td><td>${fmt(r.prev)}</td><td style="color:${variance<0?'red':'green'}">${fmt(variance)}</td><td style="color:${variance<0?'red':'green'}">${varPct}</td></tr>`;
      }).join('');

      // Build observations HTML
      const obsHtml = arObservations.filter(o => o.enabled).map((obs, i) => {
        const num = i+1;
        const riskColor = {High:'red',Medium:'darkorange',Low:'green'}[obs.risk] || '#333';
        return `
          <h2>${num < 10 ? '2.'+num : num}. ${obs.title}</h2>
          <table>
            <tr><td style="width:180px;font-weight:bold;background:#f0f4f8">Observation</td><td>${obs.observation.replace(/\n/g,'<br/>')}</td></tr>
            <tr><td style="font-weight:bold;background:#f0f4f8">Implication</td><td>${obs.implication}</td></tr>
            <tr><td style="font-weight:bold;background:#f0f4f8">Risk Rating</td><td style="color:${riskColor};font-weight:bold">${obs.risk}</td></tr>
            <tr><td style="font-weight:bold;background:#f0f4f8">Recommendation</td><td>${obs.recommendation.replace(/\n/g,'<br/>')}</td></tr>
            <tr><td style="font-weight:bold;background:#f0f4f8">Responsibility</td><td>
              <b>Primary:</b> ${obs.responsibility_primary || '—'}<br/>
              <b>Secondary:</b> ${obs.responsibility_secondary || '—'}<br/>
              <b>Target Date:</b> ${obs.target_date || '—'}
            </td></tr>
            <tr><td style="font-weight:bold;background:#f0f4f8">Follow-up Status</td><td>${obs.followup || '—'}</td></tr>
          </table>`;
      }).join('<br/>');

      // Build checklist HTML
      const clRowsHtml = CHECKLIST.map((row, i) =>
        `<tr><td style="text-align:center">${i+1}</td><td>${row[0]}</td><td style="text-align:center">${clRemarks[i] || row[1]}</td></tr>`
      ).join('');

      // Build queries HTML
      const queryRowsHtml = arQueries.map((q,i) => {
        const color = q.status==='Open'?'red':q.status==='In Process'?'darkorange':'green';
        return `<tr><td style="text-align:center">${i+1}</td><td>${q.title}</td><td style="text-align:center;color:${color};font-weight:bold">${q.status}</td></tr>`;
      }).join('');

      const html = `<!DOCTYPE html><html><head><meta charset="utf-8"/>
<style>
  body { font-family: Arial, sans-serif; font-size: 11pt; margin: 0; color: #1a1a1a; }
  h1 { font-size: 20pt; color: #1F3864; margin: 16pt 0 6pt; }
  h2 { font-size: 13pt; color: #1F3864; margin: 14pt 0 5pt; page-break-before: avoid; }
  h3 { font-size: 11pt; color: #2E5D9E; margin: 10pt 0 4pt; }
  p  { margin: 5pt 0; line-height: 1.5; }
  table { border-collapse: collapse; width: 100%; margin: 6pt 0; }
  th { background: #1F3864; color: #fff; padding: 5pt 8pt; font-size: 10pt; text-align: center; border: 1pt solid #1F3864; }
  td { border: 1pt solid #c0c0c0; padding: 4pt 7pt; font-size: 10pt; vertical-align: top; }
  tr:nth-child(even) td { background: #f8f9fc; }
  .cover-table { border: none; }
  .cover-table td { border: none; padding: 3pt 7pt; }
  .cover-title { font-size: 28pt; font-weight: bold; color: #1F3864; text-align: center; }
  .cover-sub { font-size: 14pt; color: #2E5D9E; text-align: center; }
  .section-header { background: #1F3864; color: #fff; font-size: 12pt; font-weight: bold; padding: 6pt 10pt; margin: 16pt 0 0; }
  .obs-label { font-weight: bold; background: #EDF2F7; }
  .risk-high { color: red; font-weight: bold; }
  .risk-med { color: darkorange; font-weight: bold; }
  .risk-low { color: green; font-weight: bold; }
  .page-break { page-break-before: always; }
  hr { border: none; border-top: 2pt solid #1F3864; margin: 10pt 0; }
</style>
</head><body>

<!-- COVER PAGE -->
<div style="text-align:center;padding-top:80pt">
  <p style="font-size:11pt;color:#555">Orient Energy Systems (Pvt.) Ltd.</p>
  <p style="font-size:11pt;color:#555;margin-top:0">Internal Audit Department</p>
  <br/><br/>
  <div class="cover-title">INTERNAL AUDIT REPORT</div>
  <div class="cover-sub">Service Center — ${branch}</div>
  <br/>
  <table class="cover-table" style="width:400pt;margin:20pt auto;">
    <tr><td style="font-weight:bold;width:160pt">Branch:</td><td>${branch}</td></tr>
    <tr><td style="font-weight:bold">Category:</td><td>${category}</td></tr>
    <tr><td style="font-weight:bold">Audit Period:</td><td>${curFrom} – ${curTo}</td></tr>
    <tr><td style="font-weight:bold">Prepared By:</td><td>${preparedBy}</td></tr>
    <tr><td style="font-weight:bold">Reviewed By:</td><td>${reviewedBy}</td></tr>
    <tr><td style="font-weight:bold">Report Date:</td><td>${reportDate}</td></tr>
  </table>
  <br/><br/>
  <p style="font-size:9pt;color:#888">CONFIDENTIAL — FOR MANAGEMENT USE ONLY</p>
</div>

<!-- TOC -->
<div class="page-break"></div>
<h1>Table of Contents</h1>
<table style="width:100%;border:none">
  <tr><td style="border:none">1. Analysis Section</td><td style="border:none;text-align:right">3</td></tr>
  <tr><td style="border:none;padding-left:20pt">1.1 CS Notification Analysis</td><td style="border:none;text-align:right">3</td></tr>
  <tr><td style="border:none;padding-left:20pt">1.2 Cases vs. Warranty Analysis</td><td style="border:none;text-align:right">3</td></tr>
  <tr><td style="border:none;padding-left:20pt">1.3 Cases Aging Analysis</td><td style="border:none;text-align:right">4</td></tr>
  <tr><td style="border:none;padding-left:20pt">1.4 Division-wise Parts and Units Replacement</td><td style="border:none;text-align:right">4</td></tr>
  <tr><td style="border:none;padding-left:20pt">1.5 Revenue for the Period</td><td style="border:none;text-align:right">4</td></tr>
  <tr><td style="border:none">2. Observations Section</td><td style="border:none;text-align:right">5</td></tr>
  <tr><td style="border:none">3. Conclusion</td><td style="border:none;text-align:right">9</td></tr>
</table>

<!-- METHODOLOGY -->
<div class="page-break"></div>
<h1>Methodology / Scope</h1>
<p>The Internal Audit Department of Orient Energy Systems (Pvt.) Ltd. conducted an audit of the ${branch} Service Center for the period <b>${curFrom}</b> to <b>${curTo}</b> (${days} days). The cutoff date for data collection was <b>${cutoff}</b>.</p>
<p>The audit was conducted in accordance with the Internal Audit Charter and the approved Annual Audit Plan. The scope included:</p>
<ul>
  <li>Review of customer service notification management and resolution efficiency</li>
  <li>Verification of warranty-related cases and compliance with warranty policies</li>
  <li>Physical stock count and reconciliation with SAP records</li>
  <li>Cash count and reconciliation with SAP petty cash balance</li>
  <li>Review of outstanding CS invoices and collection status</li>
  <li>Revenue analysis for the current and previous periods</li>
  <li>Expense analysis and comparison with prior period</li>
  <li>MIGO transaction completeness and accuracy</li>
</ul>
<p>The audit was performed by reviewing documentation, conducting physical verification, and obtaining management representations. Findings were discussed with the Service Center In-Charge before finalization.</p>

<!-- AUDIT CHECKLIST -->
<div class="page-break"></div>
<h1>Audit Checklist</h1>
<p><i>Audit period: ${curFrom} to ${curTo} | Cutoff: ${cutoff}</i></p>
<table>
  <thead><tr><th style="width:40pt">Sr.</th><th>Particulars</th><th style="width:160pt">Remarks</th></tr></thead>
  <tbody>${clRowsHtml}</tbody>
</table>

<!-- ANALYSIS SECTION -->
<div class="page-break"></div>
<div class="section-header">ANALYSIS SECTION</div>

<h2>1.1 CS Notification Analysis</h2>
<p>The following table summarizes CS notifications for the audit period. Total ${ihCases.toLocaleString()} In-House cases (avg age ${avgAgeIH} days) and ${cwCases.toLocaleString()} Contract Workshop cases (avg age ${avgAgeCW} days) were handled by <b>${technicians} technicians</b> at an average of <b>${days > 0 ? Math.round((ihCases+cwCases)/days) : '-'} cases/day</b>.</p>
${notifTableHtml}

<h2>1.2 Cases vs. Warranty Analysis</h2>
${warrantyTableHtml}

<h2>1.3 Cases Aging Analysis</h2>
<table>
  <thead><tr><th>Particulars</th><th>In-House Cases</th><th>In-House %</th><th>Contract Cases</th><th>Contract %</th></tr></thead>
  <tbody>${agingRowsHtml}</tbody>
</table>

<h2>1.4 Division-wise Parts and Units Replacement</h2>
${replacedTableHtml}

<h2>1.5 Revenue for the Period</h2>
<p>Comparison of revenue for current period (<b>${curFrom} – ${curTo}</b>) vs. previous period (<b>${prevFrom} – ${prevTo}</b>).</p>
<table>
  <thead><tr><th>Particulars</th><th>Current Period</th><th>Previous Period</th><th>Variance</th><th>Variance %</th></tr></thead>
  <tbody>${revenueRowsHtml}</tbody>
</table>

<!-- OBSERVATIONS SECTION -->
<div class="page-break"></div>
<div class="section-header">OBSERVATIONS SECTION</div>
${obsHtml}

<!-- CONCLUSION -->
<div class="page-break"></div>
<h1>Conclusion</h1>
<p>The Internal Audit of ${branch} Service Center for the period <b>${curFrom} – ${curTo}</b> has been completed. The following table summarizes the key metrics and the status of audit queries raised during the audit.</p>
<table>
  <tr><td style="font-weight:bold">Branch / Service Center</td><td>${branch}</td><td style="font-weight:bold">Category</td><td>${category}</td></tr>
  <tr><td style="font-weight:bold">Audit Period</td><td>${curFrom} – ${curTo}</td><td style="font-weight:bold">SC In-Charge</td><td>${scIncharge || '—'}</td></tr>
  <tr><td style="font-weight:bold">SC In-Charge Email</td><td>${scEmail || '—'}</td><td style="font-weight:bold">SC Mobile</td><td>${scMobile || '—'}</td></tr>
  <tr><td style="font-weight:bold">Total Complaints</td><td>${v('ar_total_complaints') || '—'}</td><td style="font-weight:bold">Cancelled</td><td>${v('ar_cancelled') || '—'}</td></tr>
  <tr><td style="font-weight:bold">Units Replaced</td><td>${v('ar_units_replaced') || '—'}</td><td style="font-weight:bold">Pending Notifications</td><td>${v('ar_pending') || '—'}</td></tr>
  <tr><td style="font-weight:bold">Revenue Target</td><td>${v('ar_rev_target') || 'N/A'}</td><td style="font-weight:bold">Target Achieved (Rs.)</td><td>${v('ar_target_achieved') || '—'}</td></tr>
  <tr><td style="font-weight:bold">Invoices Cleared as at</td><td>${v('ar_inv_cleared_date') || '—'}</td><td style="font-weight:bold">Amount (Rs.)</td><td>${v('ar_inv_cleared') || '—'}</td></tr>
  <tr><td style="font-weight:bold">Prepared By</td><td>${preparedBy}</td><td style="font-weight:bold">Reviewed By</td><td>${reviewedBy}</td></tr>
</table>

<h2>Audit Query Status Summary</h2>
<table>
  <thead><tr><th style="width:50pt">Sr.</th><th>Audit Query / Observation</th><th style="width:120pt">Status</th></tr></thead>
  <tbody>${queryRowsHtml}</tbody>
</table>

<br/>
<table style="width:100%;border:none">
  <tr>
    <td style="border:none;text-align:center;width:50%">
      <p style="margin-top:50pt">____________________________</p>
      <p><b>${preparedBy}</b></p>
      <p>Prepared By</p>
    </td>
    <td style="border:none;text-align:center;width:50%">
      <p style="margin-top:50pt">____________________________</p>
      <p><b>${reviewedBy}</b></p>
      <p>Reviewed By</p>
    </td>
  </tr>
</table>

</body></html>`;

      try {
        const blob = htmlDocx.asBlob(html, {orientation:'portrait', margins:{top:864,right:864,bottom:864,left:864}});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Audit_Report_${branch.replace(/\s+/g,'_')}_${curTo.replace(/\s+/g,'_')}.docx`;
        document.body.appendChild(a); a.click(); document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(url), 5000);
      } catch(err) {
        alert('Error generating report: '+err.message+'\n\nPlease ensure internet connection for html-docx-js.');
        console.error(err);
      }
    }

    $('#arGenBtn').on('click', generateReport);

    /* ── date defaults ─────────────────────────────────────────── */
    function initAuditReport() {
      // Set today's date as report date default
      const today = new Date();
      const dd = String(today.getDate()).padStart(2,'0');
      const mm = String(today.getMonth()+1).padStart(2,'0');
      const yyyy = today.getFullYear();
      if (!$('#ar_report_date').val()) {
        $('#ar_report_date').val(`${dd}.${mm}.${yyyy}`);
      }
      buildChecklist();
      rebuildAllAnalysis();
      renderObsList();
      renderQueryRows();
    }

    // Init on first navigation to the page
    let arInitialized = false;
    $(window).on('hashchange', function() {
      if (location.hash === '#/audit-report' && !arInitialized) {
        arInitialized = true;
        setTimeout(initAuditReport, 50);
      }
    });
    if (location.hash === '#/audit-report' && !arInitialized) {
      arInitialized = true;
      setTimeout(initAuditReport, 50);
    }

  })(); // end AUDIT REPORT IIFE
"""

with open('InterAudit-P1.html', encoding='utf-8') as f:
    content = f.read()

# Insert JS before the closing </script> tag of the main script block
# Find the last </script> in the file
last_script_close = content.rfind('</script>')
if last_script_close == -1:
    print('ERROR: </script> not found')
else:
    content = content[:last_script_close] + JS + '\n' + content[last_script_close:]
    with open('InterAudit-P1.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('JS injection done. Total size:', len(content))
