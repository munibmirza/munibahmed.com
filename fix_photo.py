import re

with open('InterAudit-P1.html', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Remove leftover comment
content = content.replace('  <!-- end page-audit-report -->\n', '')

# Fix 2: Remove the photo column div (md:sticky md:top-4 containing the photo)
idx = content.find('founderPhoto')
# Walk back to find the outermost sticky div
outer_start = content.rfind('<div', 0, idx)
# keep walking back until we find the "md:sticky" wrapper
for _ in range(10):
    test = content.rfind('<div', 0, outer_start)
    if 'md:sticky' in content[test:outer_start+50]:
        outer_start = test
        break
    if 'md:top' in content[test:outer_start+50]:
        outer_start = test
        break
    outer_start = test

print('Removing photo column from:', outer_start, repr(content[outer_start:outer_start+60]))

# Count nested divs to find closing tag
depth, i = 0, outer_start
while i < len(content):
    if content[i:i+4] == '<div': depth += 1; i += 4
    elif content[i:i+6] == '</div>':
        depth -= 1
        if depth == 0: i += 6; break
        else: i += 6
    else: i += 1

# Also remove the template#photoPlaceholder that follows
template_start = content.find('<template id="photoPlaceholder">', outer_start, outer_start + 2000)
if template_start != -1:
    template_end = content.find('</template>', template_start) + len('</template>')
    content = content[:outer_start] + content[template_end:]
    print('Removed photo column + placeholder template')
else:
    content = content[:outer_start] + content[i:]
    print('Removed photo column')

# Fix the grid: change md:grid-cols-[300px_1fr] → no left column
content = content.replace('md:grid-cols-[300px_1fr]', 'max-w-3xl mx-auto')

# Fix 3: Remove photo-frame CSS block
css_start = content.find('\n  .photo-frame {')
if css_start != -1:
    css_end = content.find('\n  .', css_start + 5)
    # find the end of the photo-frame block
    brace = 0
    for j in range(css_start, css_start+600):
        if content[j] == '{': brace += 1
        elif content[j] == '}':
            brace -= 1
            if brace == 0:
                content = content[:css_start] + content[j+1:]
                print('Removed .photo-frame CSS')
                break

# Also remove .photo-tag and .photo-frame::after CSS
for css_sel in ['\n  .photo-frame::after {', '\n  .photo-tag {']:
    idx2 = content.find(css_sel)
    if idx2 != -1:
        brace = 0
        for j in range(idx2, idx2+400):
            if content[j] == '{': brace += 1
            elif content[j] == '}':
                brace -= 1
                if brace == 0:
                    content = content[:idx2] + content[j+1:]
                    print('Removed', css_sel.strip()[:20])
                    break

with open('InterAudit-P1.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done. Size:', len(content))
