with open('InterAudit-P1.html', encoding='utf-8') as f:
    content = f.read()

# ── 1. Auto-days: add date change listener after the tabs listener ────────────
AUTO_DAYS = """
    // Auto-compute days from period dates
    function calcShlDays() {
      var fromStr = $('#shl_from').val();
      var toStr   = $('#shl_to').val();
      if (!fromStr || !toStr) return;
      var from = new Date(fromStr);
      var to   = new Date(toStr);
      if (isNaN(from.getTime()) || isNaN(to.getTime()) || to <= from) return;
      var diff = Math.round((to - from) / 86400000) + 1;
      $('#shl_days').val(diff);
      window.shlCompute();
    }
    $('#shl_from, #shl_to').on('input change', calcShlDays);
"""

# insert right before "// Init"
content = content.replace(
    "    // Init\n    function initShlDb()",
    AUTO_DAYS + "\n    // Init\n    function initShlDb()"
)

# ── 2. Dummy default data ─────────────────────────────────────────────────────
DUMMY_ROWS = """      // Default dummy data (Sahiwal SC sample)
      shlDb = [
        newRow('AC','IH','Resolved','With',2,1500,false,false),
        newRow('AC','IH','Resolved','With',1,0,false,false),
        newRow('AC','CWS','Resolved','Without',3,2200,false,true),
        newRow('AC','IH','Resolved','Partial',5,1800,false,false),
        newRow('AC','CWS','Resolved','With',2,0,false,false),
        newRow('AC','IH','Pending','With',12,0,false,false),
        newRow('AC','IH','Resolved','Without',4,3500,false,true),
        newRow('AC','CWS','Cancelled','With',0,0,false,false),
        newRow('AC','IH','Resolved','With',1,1200,false,false),
        newRow('AC','CWS','Resolved','With',3,0,false,false),
        newRow('REF','IH','Resolved','With',2,800,false,true),
        newRow('REF','IH','Resolved','Partial',6,1400,false,true),
        newRow('REF','CWS','Resolved','Without',4,2100,false,false),
        newRow('REF','IH','Pending','With',15,0,false,false),
        newRow('REF','CWS','Resolved','With',1,0,false,false),
        newRow('REF','IH','Resolved','With',3,900,false,false),
        newRow('REF','IH','Cancelled','With',0,0,false,false),
        newRow('WD','IH','Resolved','With',2,1100,false,true),
        newRow('WD','CWS','Resolved','Without',5,1700,false,false),
        newRow('WD','IH','Resolved','Partial',3,950,false,false),
        newRow('WM','IH','Resolved','With',1,700,false,true),
        newRow('WM','CWS','Resolved','With',4,1300,false,false),
        newRow('WM','IH','Pending','Without',11,0,false,false),
        newRow('WM','IH','Resolved','With',2,850,false,false),
        newRow('OVEN','IH','Resolved','With',1,600,false,false),
        newRow('OVEN','CWS','Resolved','Without',3,1000,false,true),
        newRow('LED','IH','Resolved','With',2,1600,false,false),
        newRow('LED','IH','Resolved','Partial',7,2400,false,true),
        newRow('LED','CWS','Resolved','With',1,0,false,false),
        newRow('LED','IH','Cancelled','With',0,0,false,false),
        newRow('AC','IH','Resolved','With',3,1800,false,false),
        newRow('AC','CWS','Resolved','With',2,0,false,false),
        newRow('REF','IH','Resolved','Without',8,2800,true,false),
        newRow('WM','CWS','Resolved','With',5,1500,false,false),
        newRow('AC','IH','Pending','With',9,0,false,false),
      ];"""

content = content.replace(
    "    function initShlDb(){ renderDb(); window.shlCompute(); }",
    "    function initShlDb() {\n" + DUMMY_ROWS + "\n      calcShlDays(); renderDb(); window.shlCompute();\n    }"
)

with open('InterAudit-P1.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done. Size:', len(content))
