c = open('InterAudit-P1.html', encoding='utf-8').read()
import re

# Find all JS references to statusBar
for m in re.finditer(r'statusBar|setStatus', c):
    print(m.start(), repr(c[m.start()-10:m.start()+120]))
