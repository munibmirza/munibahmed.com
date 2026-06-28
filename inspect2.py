c = open('InterAudit-P1.html', encoding='utf-8').read()

# Find > prompt near end of body
body_end = c.rfind('</body>')
last_section = c[body_end-3000:body_end]
print('=== last 3000 chars before </body> ===')
print(repr(last_section[:2000]))
