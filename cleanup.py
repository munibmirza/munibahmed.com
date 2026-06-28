import re, shutil

with open('InterAudit-P1.html', encoding='utf-8') as f:
    content = f.read()

shutil.copy('InterAudit-P1.html', 'InterAudit-P1.html.bak5')

# ══════════════════════════════════════════════════════════════════════════════
# 1. Remove Report tile (href="#/shl-report-db")
# ══════════════════════════════════════════════════════════════════════════════
tile_shl_start = content.find('<!-- ============ Tile — Report ============ -->')
if tile_shl_start == -1:
    tile_shl_start = content.find('<!-- ============ Tile - Report ============ -->')
tile_shl_end = content.find('<!-- ============ Tile', tile_shl_start + 10)
if tile_shl_start != -1 and tile_shl_end != -1:
    content = content[:tile_shl_start] + content[tile_shl_end:]
    print('Removed Report tile')
else:
    print('WARNING: Report tile not found')

# ══════════════════════════════════════════════════════════════════════════════
# 2. Remove Audit Report Generator tile
# ══════════════════════════════════════════════════════════════════════════════
tile_ar_start = content.find('<!-- ============ Tile — Audit Report Generator ============ -->')
if tile_ar_start == -1:
    tile_ar_start = content.find('href="#/audit-report"')
    if tile_ar_start != -1:
        tile_ar_start = content.rfind('<!-- ============', 0, tile_ar_start)
tile_ar_end = content.find('<!-- ============ Tile', tile_ar_start + 10) if tile_ar_start != -1 else -1
if tile_ar_start != -1 and tile_ar_end != -1:
    content = content[:tile_ar_start] + content[tile_ar_end:]
    print('Removed Audit Report tile')
else:
    # Try to remove just the <a> block
    a_start = content.find('<a href="#/audit-report"')
    if a_start != -1:
        # find the closing </a>
        depth = 0
        i = a_start
        while i < len(content):
            if content[i:i+2] == '<a': depth += 1; i += 2
            elif content[i:i+4] == '</a>': depth -= 1; i += 4
            if depth == 0: break
            else: i += 1
        content = content[:a_start] + content[i:]
        print('Removed Audit Report tile (fallback)')
    else:
        print('WARNING: Audit Report tile not found')

# ══════════════════════════════════════════════════════════════════════════════
# 3. Remove page-shl-db (Report workflow page)
# ══════════════════════════════════════════════════════════════════════════════
shl_page_start = content.find('<div id="page-shl-db"')
if shl_page_start != -1:
    depth, i = 0, shl_page_start
    while i < len(content):
        if content[i:i+4] == '<div': depth += 1; i += 4
        elif content[i:i+6] == '</div>': depth -= 1
        if depth == 0: i += 6; break
        elif content[i:i+6] != '</div>': i += 1
        else: i += 6
    content = content[:shl_page_start] + content[i:]
    print('Removed page-shl-db')
else:
    print('WARNING: page-shl-db not found')

# ══════════════════════════════════════════════════════════════════════════════
# 4. Remove page-audit-report
# ══════════════════════════════════════════════════════════════════════════════
ar_page_start = content.find('<div id="page-audit-report"')
if ar_page_start != -1:
    depth, i = 0, ar_page_start
    while i < len(content):
        if content[i:i+4] == '<div': depth += 1; i += 4
        elif content[i:i+6] == '</div>': depth -= 1
        if depth == 0: i += 6; break
        elif content[i:i+6] != '</div>': i += 1
        else: i += 6
    content = content[:ar_page_start] + content[i:]
    print('Removed page-audit-report')
else:
    print('WARNING: page-audit-report not found')

# ══════════════════════════════════════════════════════════════════════════════
# 5. Remove REPORT IIFE JS block
# ══════════════════════════════════════════════════════════════════════════════
js_report_start = content.find('// REPORT -- CS Audit Working Paper')
if js_report_start == -1:
    js_report_start = content.find('// REPORT — CS Audit Working Paper')
if js_report_start != -1:
    # Walk back to find the comment block start
    cb_start = content.rfind('//', 0, js_report_start)
    cb_start = content.rfind('\n', 0, cb_start) + 1
    # find closing })();
    m = re.search(r'\}\)\(\);', content[js_report_start:js_report_start+30000])
    if m:
        js_report_end = js_report_start + m.end()
        content = content[:cb_start] + content[js_report_end:]
        print('Removed REPORT IIFE JS')
    else:
        print('WARNING: REPORT IIFE end not found')
else:
    print('WARNING: REPORT IIFE start not found')

# ══════════════════════════════════════════════════════════════════════════════
# 6. Remove AUDIT REPORT GENERATOR IIFE JS block
# ══════════════════════════════════════════════════════════════════════════════
js_ar_start = content.find('// AUDIT REPORT GENERATOR')
if js_ar_start != -1:
    cb_start = content.rfind('\n', 0, js_ar_start) + 1
    m = re.search(r'\}\)\(\);.*?// end AUDIT REPORT IIFE', content[js_ar_start:js_ar_start+50000], re.DOTALL)
    if m:
        js_ar_end = js_ar_start + m.end()
    else:
        # find last })(); in the block
        m2 = None
        for m2 in re.finditer(r'\}\)\(\);', content[js_ar_start:js_ar_start+50000]): pass
        js_ar_end = js_ar_start + m2.end() if m2 else -1
    if js_ar_end != -1:
        content = content[:cb_start] + content[js_ar_end:]
        print('Removed AUDIT REPORT GENERATOR IIFE JS')
    else:
        print('WARNING: Audit Report IIFE end not found')
else:
    print('WARNING: Audit Report IIFE not found')

# ══════════════════════════════════════════════════════════════════════════════
# 7. Update routes
# ══════════════════════════════════════════════════════════════════════════════
content = re.sub(r'\s*"/shl-report-db"\s*:\s*"page-shl-db",?\n?', '\n', content)
content = re.sub(r'\s*"/audit-report"\s*:\s*"page-audit-report",?\n?', '\n', content)
content = content.replace(', #page-shl-db', '').replace('#page-shl-db, ', '').replace('#page-shl-db', '')
content = content.replace(', #page-audit-report', '').replace('#page-audit-report, ', '').replace('#page-audit-report', '')
print('Updated routes')

# ══════════════════════════════════════════════════════════════════════════════
# 8. Remove hero cutout photo (the entire hero-figure div)
# ══════════════════════════════════════════════════════════════════════════════
cutout_start = content.find('<!-- floating 3D cutout figure -->')
if cutout_start == -1:
    cutout_start = content.find('founder_cutout.png')
    if cutout_start != -1:
        cutout_start = content.rfind('<div', 0, cutout_start)
if cutout_start != -1:
    depth, i = 0, cutout_start
    # skip the comment if present
    if content[cutout_start:cutout_start+4] == '<!--':
        i = content.find('-->', cutout_start) + 3
        cutout_start = i
        i = content.find('<div', i)
        cutout_start = i
    while i < len(content):
        if content[i:i+4] == '<div': depth += 1; i += 4
        elif content[i:i+6] == '</div>': depth -= 1
        if depth == 0: i += 6; break
        elif content[i:i+6] != '</div>': i += 1
        else: i += 6
    content = content[:cutout_start] + content[i:]
    print('Removed hero cutout photo')
else:
    print('WARNING: hero cutout not found')

# ══════════════════════════════════════════════════════════════════════════════
# 9. Remove founder photo column from intro modal
#    (the entire "LEFT - photo column" div inside the modal)
# ══════════════════════════════════════════════════════════════════════════════
photo_col_start = content.find('<!-- LEFT')
if photo_col_start == -1:
    photo_col_start = content.find('photo-frame floaty')
    if photo_col_start != -1:
        photo_col_start = content.rfind('<div', 0, photo_col_start)
if photo_col_start != -1:
    depth, i = 0, photo_col_start
    while i < len(content):
        if content[i:i+4] == '<div': depth += 1; i += 4
        elif content[i:i+6] == '</div>': depth -= 1
        if depth == 0: i += 6; break
        elif content[i:i+6] != '</div>': i += 1
        else: i += 6
    # also remove the comment line before it
    comment_before = content.rfind('<!--', 0, photo_col_start)
    if comment_before != -1 and content[comment_before:photo_col_start].strip() == content[comment_before:content.find('-->',comment_before)+3].strip():
        photo_col_start = comment_before
    content = content[:photo_col_start] + content[i:]
    # Fix the grid cols class since we removed the left column
    content = content.replace('md:grid-cols-[300px_1fr]', 'grid-cols-1')
    print('Removed photo column from intro modal')
else:
    print('WARNING: photo column not found')

with open('InterAudit-P1.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done. Final size:', len(content))
