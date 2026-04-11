import os, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9555")
driver = webdriver.Chrome(options=options)

# Navigate to content page (general)
driver.get("https://studio.youtube.com/channel/UC/content")
time.sleep(10)

driver.save_screenshot("debug_content_page.png")
print(f"[URL] {driver.current_url}")

# Dump tabs and content structure
info = driver.execute_script("""
    var info = [];

    // Check for filter chips/tabs at the top
    var chips = document.querySelectorAll('ytcp-chip-bar ytcp-chip, [role="tab"], tp-yt-paper-tab, .tab');
    info.push('=== CHIPS/TABS (' + chips.length + ') ===');
    for (var c of chips) {
        var txt = (c.textContent || '').trim().replace(/\\s+/g, ' ').substring(0, 60);
        info.push('  tag=' + c.tagName + ' text="' + txt + '"');
    }

    // Check navigation items on the left
    var navItems = document.querySelectorAll('tp-yt-app-drawer a, .navigation-item, ytcp-ve a');
    info.push('\\n=== NAV ITEMS (' + navItems.length + ') ===');
    for (var n of navItems) {
        var txt = (n.textContent || '').trim().replace(/\\s+/g, ' ').substring(0, 60);
        var href = n.getAttribute('href') || '';
        if (txt && (txt.toLowerCase().includes('short') || txt.toLowerCase().includes('cont') || txt.toLowerCase().includes('video'))) {
            info.push('  text="' + txt + '" href=' + href);
        }
    }

    // Video count
    var rows = document.querySelectorAll('ytcp-video-row');
    info.push('\\n=== VIDEO ROWS: ' + rows.length + ' ===');

    // Check for "Shorts" filter/tab anywhere
    var all = document.querySelectorAll('*');
    var shortElements = [];
    for (var el of all) {
        if (el.children.length > 3) continue;
        var txt = (el.textContent || '').trim();
        if (txt.toLowerCase() === 'shorts' || txt.toLowerCase() === 'short') {
            shortElements.push('tag=' + el.tagName + ' class=' + (el.className||'').substring(0,40) + ' text="' + txt + '"');
        }
    }
    info.push('\\n=== ELEMENTS WITH "Shorts" TEXT (' + shortElements.length + ') ===');
    for (var s of shortElements) info.push('  ' + s);

    // Any visible video links
    var links = document.querySelectorAll('a[href*="/video/"]');
    info.push('\\n=== VIDEO LINKS: ' + links.length + ' ===');
    for (var i = 0; i < Math.min(links.length, 5); i++) {
        info.push('  ' + links[i].getAttribute('href'));
    }

    return info.join('\\n');
""")
print(info)
