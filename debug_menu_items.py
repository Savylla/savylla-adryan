"""Debug: go to a video edit page and inspect the kebab menu."""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9555")
driver = webdriver.Chrome(options=options)

# Go to a specific video edit page
vid = "DiF7N5qqByM"
print(f"[1] Navegando para edit page: {vid}")
driver.get(f"https://studio.youtube.com/video/{vid}/edit")
time.sleep(6)
driver.save_screenshot("debug_edit_page.png")
print("   Screenshot: debug_edit_page.png")

# Dump all visible buttons
print("\n[2] Botoes visiveis na pagina:")
btns = driver.execute_script(r"""
    var info = [];
    var btns = document.querySelectorAll("ytcp-button, ytcp-icon-button, button");
    for (var b of btns) {
        if (b.offsetParent === null) continue;
        var txt = (b.textContent || "").trim().replace(/\s+/g, " ").substring(0, 60);
        var aria = b.getAttribute("aria-label") || "";
        var id = b.id || "";
        info.push(b.tagName + " id=" + id + " aria='" + aria + "' text='" + txt + "'");
    }
    return info.join("\n");
""")
print(btns)

# Click the kebab/more menu
print("\n[3] Clicando no menu kebab...")
r = driver.execute_script(r"""
    // Try #more-actions
    var more = document.querySelector("#more-actions");
    if (more) { more.click(); return "clicked #more-actions"; }

    // Try icon buttons with more_vert
    var icons = document.querySelectorAll("ytcp-icon-button, ytcp-button");
    for (var b of icons) {
        if (b.offsetParent === null) continue;
        var aria = (b.getAttribute("aria-label") || "").toLowerCase();
        if (aria.includes("mais") || aria.includes("more") || aria.includes("opções")) {
            b.click();
            return "clicked aria: " + aria;
        }
    }

    // Try any 3-dot icon
    var allBtns = document.querySelectorAll("ytcp-icon-button, ytcp-button, button");
    for (var b of allBtns) {
        if (b.offsetParent === null) continue;
        var icon = b.querySelector("[icon='more_vert'], tp-yt-iron-icon[icon='more_vert']");
        if (icon) { b.click(); return "clicked more_vert icon button"; }
    }

    return "not found";
""")
print(f"   {r}")
time.sleep(3)

driver.save_screenshot("debug_kebab_menu.png")
print("   Screenshot: debug_kebab_menu.png")

# Dump menu items
print("\n[4] Items no menu:")
items = driver.execute_script(r"""
    var info = [];

    // Check tp-yt-paper-item (standard menu items)
    var paperItems = document.querySelectorAll("tp-yt-paper-item");
    info.push("tp-yt-paper-item: " + paperItems.length);
    for (var item of paperItems) {
        var vis = item.offsetParent !== null ? "V" : "H";
        var txt = (item.textContent || "").trim().replace(/\s+/g, " ").substring(0, 80);
        if (txt) info.push("  [" + vis + "] " + txt);
    }

    // Check paper-listbox items
    var listboxItems = document.querySelectorAll("tp-yt-paper-listbox tp-yt-paper-item");
    info.push("\nlistbox items: " + listboxItems.length);

    // Check dialogs
    var dialogs = document.querySelectorAll("tp-yt-paper-dialog");
    info.push("\nDialogs: " + dialogs.length);
    for (var d of dialogs) {
        var hidden = d.getAttribute("aria-hidden");
        if (hidden !== "true") {
            info.push("  OPEN dialog, innerHTML: " + d.innerHTML.substring(0, 500));
        }
    }

    // Check ytcp-text-menu dialog
    var textMenus = document.querySelectorAll("ytcp-text-menu");
    info.push("\nText menus: " + textMenus.length);
    for (var tm of textMenus) {
        var pd = tm.querySelector("tp-yt-paper-dialog");
        if (pd) {
            var hidden = pd.getAttribute("aria-hidden");
            info.push("  dialog hidden=" + hidden);
            if (hidden !== "true") {
                var items = pd.querySelectorAll("tp-yt-paper-item");
                info.push("  items in open dialog: " + items.length);
                for (var item of items) {
                    info.push("    - " + item.textContent.trim().substring(0, 60));
                }
            }
        }
    }

    // Check anything with "excluir" or "delete" regardless of visibility
    info.push("\nAll elements with excluir/delete:");
    var all = document.querySelectorAll("*");
    for (var el of all) {
        if (el.children.length > 2) continue;
        var txt = (el.textContent || "").trim().toLowerCase();
        if (txt.length < 80 && (txt.includes("excluir") || txt.includes("delete"))) {
            var vis = el.offsetParent !== null ? "V" : "H";
            info.push("  [" + vis + "] " + el.tagName + ": " + txt);
        }
    }

    return info.join("\n");
""")
print(items)
