"""
Fix: add single video Drogasil_020 to Portfolio - Drogasil playlist.
"""
import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

subprocess.Popen(['taskkill', '/F', '/IM', 'chrome.exe'],
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.Popen(['taskkill', '/F', '/IM', 'chromedriver.exe'],
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)

for f in ['SingletonLock', 'SingletonSocket', 'SingletonCookie']:
    p = os.path.join('chrome_selenium_data', f)
    try:
        os.remove(p)
    except Exception:
        pass

opts = Options()
data_dir = os.path.join(os.getcwd(), 'chrome_selenium_data')
opts.add_argument(f'--user-data-dir={data_dir}')
opts.add_argument('--remote-debugging-port=9555')
opts.add_argument('--no-first-run')
opts.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=opts)

driver.get('https://studio.youtube.com')
time.sleep(5)

if 'accounts.google' in driver.current_url:
    print('[LOGIN] Faca login no Chrome! (max 5 min)')
    for i in range(150):
        time.sleep(2)
        try:
            if 'studio.youtube.com' in driver.current_url and 'accounts.google' not in driver.current_url:
                print('[OK] Login detectado!')
                break
        except Exception:
            pass
    time.sleep(3)

vid = '4GacJQx5Bc8'
playlist_name = 'Portfolio - Drogasil'
print(f'\n[FIX] Video {vid} -> {playlist_name}')

driver.get(f'https://studio.youtube.com/video/{vid}/edit')
time.sleep(8)

# Click playlist trigger
driver.execute_script("""
    var comp = document.querySelector('ytcp-video-metadata-playlists');
    if (comp) {
        var trigger = comp.querySelector('ytcp-text-dropdown-trigger, [role="button"]');
        if (trigger) trigger.click();
        else comp.click();
    }
""")
time.sleep(4)

# Select playlist
selected = driver.execute_script("""
    var targetName = arguments[0];
    var dialog = document.querySelector('ytcp-playlist-dialog');
    if (!dialog) return 'no_dialog';
    var groups = dialog.querySelectorAll('ytcp-checkbox-group');
    for (var group of groups) {
        var nameSpan = group.querySelector('span.checkbox-label, span.label');
        var txt = nameSpan ? nameSpan.textContent.trim() : '';
        if (txt.includes(targetName)) {
            var cbDiv = group.querySelector('div[role="checkbox"]');
            var isChecked = cbDiv && cbDiv.getAttribute('aria-checked') === 'true';
            if (isChecked) return 'already_checked';
            var label = group.querySelector('label.ytcp-checkbox-label');
            if (label) { label.click(); return 'clicked'; }
        }
    }
    // Fallback
    var labels = dialog.querySelectorAll('label.ytcp-checkbox-label');
    for (var l of labels) {
        if ((l.textContent || '').trim().includes(targetName)) {
            l.click();
            return 'clicked_fallback';
        }
    }
    return 'not_found';
""", playlist_name)
print(f'  Select: {selected}')

time.sleep(1)

# Verify
verify = driver.execute_script("""
    var targetName = arguments[0];
    var dialog = document.querySelector('ytcp-playlist-dialog');
    if (!dialog) return 'no_dialog';
    var groups = dialog.querySelectorAll('ytcp-checkbox-group');
    for (var group of groups) {
        var nameSpan = group.querySelector('span.checkbox-label, span.label');
        var txt = nameSpan ? nameSpan.textContent.trim() : '';
        if (txt.includes(targetName)) {
            var cbDiv = group.querySelector('div[role="checkbox"]');
            return 'aria-checked=' + (cbDiv ? cbDiv.getAttribute('aria-checked') : 'no_div');
        }
    }
    return 'not_found';
""", playlist_name)
print(f'  Verify: {verify}')

# Click Concluir
driver.execute_script("""
    var dialog = document.querySelector('ytcp-playlist-dialog');
    if (!dialog) return;
    var allElements = dialog.querySelectorAll('ytcp-button, button, div');
    for (var el of allElements) {
        var txt = (el.textContent || '').trim().toLowerCase();
        if (txt === 'concluir' || txt === 'done') {
            el.click();
            return;
        }
    }
""")
time.sleep(2)

# Save
saved = driver.execute_script("""
    var saveBtn = document.querySelector('ytcp-button#save');
    if (!saveBtn) saveBtn = document.querySelector('#save');
    if (!saveBtn) {
        var btns = document.querySelectorAll('ytcp-button');
        for (var b of btns) {
            if ((b.textContent || '').trim().toLowerCase() === 'salvar') { saveBtn = b; break; }
        }
    }
    if (!saveBtn) return 'no_save_btn';
    var ariaDisabled = saveBtn.getAttribute('aria-disabled');
    if (ariaDisabled !== 'true') { saveBtn.click(); return 'saved'; }
    return 'disabled|aria=' + ariaDisabled;
""")
print(f'  Save: {saved}')
time.sleep(3)

print('\n[DONE]')
driver.quit()
