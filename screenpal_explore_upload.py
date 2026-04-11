"""Explore the ScreenPal upload page selectors."""
import json, os, sys, time, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver():
    debug_port = 9556
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")
    return webdriver.Chrome(options=options)

def capture(driver, label):
    print(f"\n[CAPTURANDO] {label}")
    print(f"  URL: {driver.current_url}")
    print(f"  Title: {driver.title}")
    data = driver.execute_script("""
        var r = {buttons:[], inputs:[], fileInputs:[], links:[], dropZones:[], forms:[], all_tags:{}};

        // ALL visible elements summary
        document.querySelectorAll('*').forEach(function(el) {
            if (el.offsetParent !== null || el.offsetHeight > 0) {
                var tag = el.tagName;
                r.all_tags[tag] = (r.all_tags[tag] || 0) + 1;
            }
        });

        // Buttons
        document.querySelectorAll('button, [role="button"], input[type="submit"], input[type="button"], .btn').forEach(function(el) {
            if (el.offsetParent !== null || el.offsetHeight > 0) {
                r.buttons.push({
                    tag: el.tagName, text: (el.textContent||'').trim().substring(0,80),
                    id: el.id||'', cls: (el.className||'').toString().substring(0,120),
                    aria: el.getAttribute('aria-label')||'', type: el.type||''
                });
            }
        });

        // ALL inputs (visible and hidden)
        document.querySelectorAll('input, textarea, select').forEach(function(el) {
            r.inputs.push({
                tag: el.tagName, type: el.type||'', name: el.name||'', id: el.id||'',
                placeholder: el.placeholder||'', accept: el.accept||'',
                cls: (el.className||'').toString().substring(0,100),
                visible: el.offsetParent !== null, multiple: el.multiple||false,
                value: (el.type === 'hidden') ? '' : (el.value||'').substring(0,50)
            });
        });

        // File inputs
        document.querySelectorAll('input[type="file"]').forEach(function(el) {
            r.fileInputs.push({
                name: el.name||'', id: el.id||'', accept: el.accept||'',
                multiple: el.multiple, cls: (el.className||'').toString().substring(0,100),
                parentCls: (el.parentElement && el.parentElement.className||'').toString().substring(0,100)
            });
        });

        // Forms
        document.querySelectorAll('form').forEach(function(el) {
            r.forms.push({
                action: el.action||'', method: el.method||'', id: el.id||'',
                cls: (el.className||'').toString().substring(0,100),
                enctype: el.enctype||''
            });
        });

        // Links with relevant text
        document.querySelectorAll('a[href]').forEach(function(el) {
            if (el.offsetParent !== null) {
                r.links.push({
                    text: (el.textContent||'').trim().substring(0,80),
                    href: (el.href||'').substring(0,150),
                    id: el.id||''
                });
            }
        });

        // Drop zones / upload areas
        document.querySelectorAll('[class*="drop"], [class*="upload"], [class*="drag"], [class*="file"]').forEach(function(el) {
            if (el.offsetParent !== null || el.tagName === 'INPUT') {
                r.dropZones.push({
                    tag: el.tagName, id: el.id||'',
                    cls: (el.className||'').toString().substring(0,150),
                    text: (el.textContent||'').trim().substring(0,150)
                });
            }
        });

        return r;
    """)

    for key, items in data.items():
        if items:
            if isinstance(items, dict):
                print(f"\n  --- {key.upper()} ---")
                for tag, count in sorted(items.items(), key=lambda x: -x[1])[:20]:
                    print(f"    {tag}: {count}")
            else:
                print(f"\n  --- {key.upper()} ({len(items)}) ---")
                for item in items[:20]:
                    print(f"    {json.dumps(item, ensure_ascii=False)}")
    return data

driver = create_driver()

# Navigate to upload page
print("=" * 60)
print("  EXPLORANDO PAGINA DE UPLOAD")
print("=" * 60)

driver.get("https://screenpal.com/content/upload")
time.sleep(8)
capture(driver, "Upload Page")

# Check if there's a progress/status area after the page loads
print("\n\n[VERIFICANDO] Elementos de progresso e status...")
progress_data = driver.execute_script("""
    var r = [];
    document.querySelectorAll('[class*="progress"], [class*="status"], [class*="percent"], [role="progressbar"]').forEach(function(el) {
        r.push({
            tag: el.tagName, cls: (el.className||'').toString().substring(0,150),
            text: (el.textContent||'').trim().substring(0,100),
            role: el.getAttribute('role')||'',
            ariaValue: el.getAttribute('aria-valuenow')||''
        });
    });
    return r;
""")
if progress_data:
    print("  Elementos de progresso:")
    for item in progress_data:
        print(f"    {json.dumps(item, ensure_ascii=False)}")
else:
    print("  Nenhum elemento de progresso encontrado (normal antes do upload)")

# Check page structure (is it an iframe?)
print("\n[VERIFICANDO] Iframes na pagina...")
iframes = driver.execute_script("""
    var r = [];
    document.querySelectorAll('iframe').forEach(function(el) {
        r.push({ src: el.src||'', id: el.id||'', cls: (el.className||'').toString().substring(0,100) });
    });
    return r;
""")
for item in iframes:
    print(f"  {json.dumps(item, ensure_ascii=False)}")

print("\n\n[COMPLETO] Dados capturados!")
