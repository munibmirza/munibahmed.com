c = open('InterAudit-P1.html', encoding='utf-8').read()

# Status bar + > prompt
idx = c.find('Ready</footer>')
print('=== status bar ===')
print(repr(c[idx-150:idx+20]))

# find the > (prompt)
idx2 = c.find('statusBar')
chunk = c[idx2-10:idx2+300]
print('=== statusBar element ===')
print(repr(chunk))

# contact page
marker = 'id="page-contact"'
idx3 = c.find(marker)
print('=== contact page ===')
print(repr(c[idx3:idx3+2000]))
