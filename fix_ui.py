import re, shutil

with open('InterAudit-P1.html', encoding='utf-8') as f:
    content = f.read()

shutil.copy('InterAudit-P1.html', 'InterAudit-P1.html.bak6')

# ══════════════════════════════════════════════════════════════════════════════
# 1. Remove the footer status bar element
# ══════════════════════════════════════════════════════════════════════════════
content = re.sub(
    r'\s*<!-- STATUS BAR -->\s*\n<footer id="statusBar"[^>]*>.*?</footer>',
    '', content, flags=re.DOTALL
)
# Also try without the comment
content = re.sub(
    r'\n<footer id="statusBar"[^>]*>.*?</footer>',
    '', content, flags=re.DOTALL
)
print('Status bar footer removed:', 'statusBar' not in content.split('<script')[0])

# ══════════════════════════════════════════════════════════════════════════════
# 2. Remove #statusBar CSS blocks
#    There are several theme-variant overrides — remove them all
# ══════════════════════════════════════════════════════════════════════════════
# Remove the first full #statusBar block (the general one in CSS)
content = re.sub(
    r'/\* status bar \*/\s*\n\s*#statusBar \{[^}]*\}',
    '', content
)
# Remove any remaining #statusBar { ... } overrides in theme <style> blocks
content = re.sub(
    r'\s*#statusBar \{[^}]*\}',
    '', content
)
print('StatusBar CSS blocks removed')

# ══════════════════════════════════════════════════════════════════════════════
# 3. Remove setStatus JS function and its callers
# ══════════════════════════════════════════════════════════════════════════════
content = re.sub(
    r'\nfunction setStatus\(msg\) \{[^\}]+\}\n',
    '\nfunction setStatus(msg) {}\n',   # stub it silently so callers don't error
    content
)
print('setStatus stubbed')

# ══════════════════════════════════════════════════════════════════════════════
# 4. Add profile picture to contact section
#    Insert a centered photo card right before the "LET'S TALK." heading section
# ══════════════════════════════════════════════════════════════════════════════
CONTACT_PHOTO = '''    <section class="pt-4 flex flex-col sm:flex-row items-center gap-8">
      <!-- Profile photo -->
      <div class="flex-shrink-0">
        <div class="relative w-44 h-44 rounded-2xl overflow-hidden ring-2 ring-yellow-300/30 shadow-2xl">
          <img src="assets/founder.jpg" alt="Munib Ahmed"
               onerror="this.style.display='none';document.getElementById('contactPhotoPh').style.display='flex';"
               class="w-full h-full object-cover object-top"/>
          <div id="contactPhotoPh" class="hidden w-full h-full items-center justify-center"
               style="background:linear-gradient(160deg,#1a2a40,#0f1a2c)">
            <svg class="w-20 h-20 opacity-30" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
          </div>
          <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent pointer-events-none"></div>
        </div>
        <p class="text-center text-xs mt-2 text-blue-100/60 tracking-widest uppercase">Munib Ahmed</p>
        <p class="text-center text-[10px] text-yellow-300/70 tracking-wider">Internal Audit Trainee</p>
      </div>
      <!-- Heading -->
      <div class="flex-1">
        <div class="flex items-center gap-3 mb-6">
          <div class="gold-bar w-10"></div>
          <span class="text-[11px] uppercase tracking-[0.3em] text-yellow-300/90">Get in touch</span>
        </div>
        <h1 class="h-serif leading-[0.92]" style="font-size:clamp(2.4rem,6vw,4.8rem); color:var(--ink);">
          <span class="clip"><span style="--d:.05s">LET\'S TALK.</span></span>
        </h1>
        <p class="reveal max-w-xl mt-5 text-base" style="--d:.4s; color:var(--ink);">
          Open to audit-technology, internal-audit and finance-automation conversations.
        </p>
      </div>
    </section>

'''

# Find the original contact heading section and replace it
old_contact_header = '''    <section class="pt-4">
      <div class="flex items-center gap-3 mb-6">
        <div class="gold-bar w-10"></div>
        <span class="text-[11px] uppercase tracking-[0.3em] text-yellow-300/90">Get in touch</span>
      </div>
      <h1 class="h-serif leading-[0.92]" style="font-size:clamp(2.4rem,6vw,4.8rem); color:var(--ink);">
        <span class="clip"><span style="--d:.05s">LET\'S TALK.</span></span>
      </h1>
      <p class="reveal max-w-xl mt-7 text-base" style="--d:.4s; color:var(--ink);">
        Open to audit-technology, internal-audit and finance-automation conversations.
      </p>
    </section>'''

if old_contact_header in content:
    content = content.replace(old_contact_header, CONTACT_PHOTO.rstrip())
    print('Contact photo section added')
else:
    # Try a looser replacement
    idx = content.find('LET\'S TALK.')
    if idx != -1:
        sec_start = content.rfind('<section', 0, idx)
        sec_end = content.find('</section>', idx) + len('</section>')
        content = content[:sec_start] + CONTACT_PHOTO.rstrip() + content[sec_end:]
        print('Contact photo added (fallback)')
    else:
        print('WARNING: Contact heading not found')

with open('InterAudit-P1.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done. Size:', len(content))
