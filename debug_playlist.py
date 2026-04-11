"""
Cria "Portfolio - Raia" playlist via ytcp-playlist-creation-dialog.
O dialog usa contenteditable divs, nao input elements.
"""

import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

subprocess.Popen(['taskkill', '/F', '/IM', 'chrome.exe'],
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.Popen(['taskkill', '/F', '/IM', 'chromedriver.exe'],
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)

data_dir = os.path.join(os.getcwd(), 'chrome_selenium_data')
for f in ['SingletonLock', 'SingletonSocket', 'SingletonCookie']:
    try:
        os.remove(os.path.join(data_dir, f))
    except Exception:
        pass

opts = Options()
opts.add_argument(f'--user-data-dir={data_dir}')
opts.add_argument('--remote-debugging-port=9555')
opts.add_argument('--no-first-run')
opts.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=opts)

driver.get('https://studio.youtube.com')
time.sleep(5)
if 'accounts.google' in driver.current_url:
    print('[LOGIN]')
    for _ in range(150):
        time.sleep(2)
        if 'studio.youtube.com' in driver.current_url and 'accounts.google' not in driver.current_url:
            break
    time.sleep(3)

vid = 'JmbMlwo53GM'
driver.get(f'https://studio.youtube.com/video/{vid}/edit')
time.sleep(8)

# Open playlist dialog
print('[1] Open playlist dialog')
driver.execute_script("""
    var comp = document.querySelector('ytcp-video-metadata-playlists');
    if (comp) {
        var trigger = comp.querySelector('ytcp-text-dropdown-trigger, [role="button"]');
        if (trigger) trigger.click();
    }
""")
time.sleep(3)

# Click dropdown
print('[2] Click dropdown')
driver.execute_script("""
    var dialog = document.querySelector('ytcp-playlist-dialog');
    var dropBtn = dialog.querySelector('.new-playlist-button button');
    if (dropBtn) dropBtn.click();
""")
time.sleep(2)

# Click menu item
print('[3] Click menu item "Nova playlist"')
driver.execute_script("""
    var item = document.querySelector('tp-yt-paper-item[test-id="new_playlist"]');
    if (item) item.click();
""")
time.sleep(4)

# Find the creation dialog and dump its contenteditable elements
print('[4] Find creation dialog structure')
structure = driver.execute_script("""
    var dialogs = document.querySelectorAll('tp-yt-paper-dialog');
    for (var d of dialogs) {
        if (d.offsetHeight > 500 && getComputedStyle(d).display !== 'none') {
            var result = 'Found creation dialog (h=' + d.offsetHeight + ')\\n';

            // Find contenteditable elements
            var editables = d.querySelectorAll('[contenteditable], [contenteditable="true"], [contenteditable="plaintext-only"]');
            result += 'Contenteditable elements: ' + editables.length + '\\n';
            for (var e of editables) {
                result += '  [' + e.tagName + ' id="' + (e.id||'') + '"] text="' + e.textContent.trim() + '" h=' + e.offsetHeight + '\\n';
            }

            // Find textbox roles
            var textboxes = d.querySelectorAll('[role="textbox"]');
            result += 'Textbox roles: ' + textboxes.length + '\\n';
            for (var t of textboxes) {
                result += '  [' + t.tagName + ' id="' + (t.id||'') + '"] text="' + t.textContent.trim() + '"\\n';
            }

            // Find ytcp-form-input-container
            var formInputs = d.querySelectorAll('ytcp-form-input-container');
            result += 'Form input containers: ' + formInputs.length + '\\n';
            for (var fi of formInputs) {
                result += '  [id="' + (fi.id||'') + '"] label="' + (fi.getAttribute('label')||'') + '"\\n';
                var inner = fi.querySelector('[contenteditable], [role="textbox"], input, textarea');
                if (inner) {
                    result += '    inner: [' + inner.tagName + ' id="' + (inner.id||'') + '"] role="' + (inner.getAttribute('role')||'') + '"\\n';
                }
            }

            // Find the title input specifically
            var titleContainer = d.querySelector('#title-input, [aria-label*="tulo"], [aria-label*="itle"]');
            result += '\\nTitle input by aria: ' + (titleContainer ? titleContainer.tagName + '#' + titleContainer.id : 'NOT FOUND') + '\\n';

            // Just dump ALL elements with role or aria
            result += '\\nElements with aria-label:\\n';
            var all = d.querySelectorAll('[aria-label]');
            for (var el of all) {
                var lbl = el.getAttribute('aria-label');
                if (lbl && el.offsetHeight > 0) {
                    result += '  [' + el.tagName + ' id="' + (el.id||'') + '"] aria="' + lbl + '"\\n';
                }
            }

            return result;
        }
    }
    return 'No creation dialog found';
""")
print(structure)

# Now try to type in the title field
print('\n[5] Typing playlist name')
typed = driver.execute_script("""
    var dialogs = document.querySelectorAll('tp-yt-paper-dialog');
    for (var d of dialogs) {
        if (d.offsetHeight > 500 && getComputedStyle(d).display !== 'none') {
            // Find the title textbox
            var textboxes = d.querySelectorAll('[contenteditable], [role="textbox"]');
            if (textboxes.length > 0) {
                var titleBox = textboxes[0]; // First one should be title
                titleBox.focus();
                titleBox.click();
                titleBox.textContent = '';
                return 'focused: ' + titleBox.tagName + '#' + titleBox.id;
            }

            // Try form input containers
            var containers = d.querySelectorAll('ytcp-form-input-container');
            for (var c of containers) {
                var lbl = (c.getAttribute('label') || '').toLowerCase();
                if (lbl.includes('tulo') || lbl.includes('itle') || lbl.includes('nome')) {
                    var inner = c.querySelector('[contenteditable], [role="textbox"], div[id="textbox"]');
                    if (inner) {
                        inner.focus();
                        inner.click();
                        return 'focused_container: ' + inner.tagName + '#' + inner.id;
                    }
                }
            }

            return 'no_textbox_found';
        }
    }
    return 'no_dialog';
""")
print(f'  {typed}')

if 'focused' in typed:
    time.sleep(0.5)
    active = driver.switch_to.active_element
    active.send_keys(Keys.CONTROL + "a")
    active.send_keys(Keys.DELETE)
    active.send_keys("Portfolio - Raia")
    print('  Typed: Portfolio - Raia')
    time.sleep(2)

    # Set visibility to Unlisted if possible
    print('\n[6] Setting visibility...')
    vis = driver.execute_script("""
        var dialogs = document.querySelectorAll('tp-yt-paper-dialog');
        for (var d of dialogs) {
            if (d.offsetHeight > 500 && getComputedStyle(d).display !== 'none') {
                // Look for visibility dropdown or options
                var dropdowns = d.querySelectorAll('ytcp-text-dropdown-trigger, [role="listbox"], [role="combobox"]');
                for (var dd of dropdowns) {
                    var txt = (dd.textContent || '').trim();
                    if (txt.includes('blica') || txt.includes('ublic') || txt.includes('rivad') || txt.includes('listado')) {
                        dd.click();
                        return 'clicked_visibility: ' + txt;
                    }
                }
                return 'no_visibility_dropdown';
            }
        }
        return 'no_dialog';
    """)
    print(f'  {vis}')

    time.sleep(2)

    # Click "Criar" button
    print('\n[7] Clicking Criar...')
    criar = driver.execute_script("""
        var dialogs = document.querySelectorAll('tp-yt-paper-dialog');
        for (var d of dialogs) {
            if (d.offsetHeight > 500 && getComputedStyle(d).display !== 'none') {
                var btns = d.querySelectorAll('ytcp-button, button');
                for (var b of btns) {
                    var txt = (b.textContent || '').trim().toLowerCase();
                    if (txt === 'criar' || txt === 'create') {
                        var disabled = b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true';
                        if (!disabled) {
                            b.click();
                            return 'clicked_criar';
                        }
                        return 'criar_disabled';
                    }
                }
                return 'no_criar';
            }
        }
        return 'no_dialog';
    """)
    print(f'  {criar}')
    time.sleep(5)

    # Check result
    print('\n[8] Checking result...')
    print(f'  URL: {driver.current_url}')

    # Check if we're back on the edit page and the playlist dialog shows the new playlist
    check = driver.execute_script("""
        var comp = document.querySelector('ytcp-video-metadata-playlists');
        if (comp) {
            return 'playlists component text: ' + (comp.textContent || '').trim().substring(0, 200);
        }
        return 'no component';
    """)
    print(f'  {check}')

time.sleep(3)
print('\nDone.')
driver.quit()
