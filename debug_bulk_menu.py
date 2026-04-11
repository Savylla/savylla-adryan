"""Debug: see what bulk action menu items appear after selecting shorts."""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9555")
driver = webdriver.Chrome(options=options)

# Navigate to shorts page
driver.get("https://studio.youtube.com/channel/UCaLWwZY1Yn_8svQQevLbMoA/videos/short")
time.sleep(6)

# Click the first checkbox (select all header)
r1 = driver.execute_script(r"""
    var allCB = document.querySelectorAll("ytcp-checkbox-lit");
    if (allCB.length > 0) {
        allCB[0].click();
        return "Clicked first checkbox. Total checkboxes: " + allCB.length;
    }
    return "No checkboxes found";
""")
print("[STEP 1]", r1)
time.sleep(3)

# Screenshot after selecting
driver.save_screenshot("debug_after_select.png")
print("[SCREENSHOT] debug_after_select.png")

# Dump all visible buttons and their text
r2 = driver.execute_script(r"""
    var info = [];
    var btns = document.querySelectorAll("ytcp-button, button, ytcp-icon-button, ytcp-dropdown-trigger");
    for (var i = 0; i < btns.length; i++) {
        var b = btns[i];
        if (b.offsetParent === null) continue;
        var txt = (b.textContent || "").trim().replace(/\s+/g, " ").substring(0, 80);
        var aria = b.getAttribute("aria-label") || "";
        var id = b.id || "";
        var tag = b.tagName;
        info.push(tag + " | id=" + id + " | aria=" + aria.substring(0,50) + " | text=" + txt);
    }
    return info.join("\n");
""")
print("\n[VISIBLE BUTTONS]")
print(r2)

# Now click the "Mais acoes" / overflow button
r3 = driver.execute_script(r"""
    var btns = document.querySelectorAll("ytcp-button, ytcp-icon-button, button");
    for (var b of btns) {
        if (b.offsetParent === null) continue;
        var aria = (b.getAttribute("aria-label") || "").toLowerCase();
        var txt = (b.textContent || "").trim().toLowerCase();
        if (aria.includes("mais") || aria.includes("more") ||
            aria.includes("other") || aria.includes("outro") ||
            txt.includes("mais a")) {
            b.click();
            return "Clicked: aria=" + aria + " txt=" + txt.substring(0, 40);
        }
    }
    // Try overflow icon
    var icons = document.querySelectorAll("tp-yt-iron-icon, iron-icon");
    for (var ic of icons) {
        var iconName = ic.getAttribute("icon") || "";
        if (iconName === "more_vert" || iconName === "more_horiz") {
            var parent = ic.closest("ytcp-button, ytcp-icon-button, button");
            if (parent && parent.offsetParent !== null) {
                parent.click();
                return "Clicked icon parent: " + iconName;
            }
        }
    }
    return "No more-actions button found";
""")
print("\n[STEP 2 - CLICK MORE]", r3)
time.sleep(3)

# Screenshot after clicking more
driver.save_screenshot("debug_after_more.png")
print("[SCREENSHOT] debug_after_more.png")

# Dump menu items
r4 = driver.execute_script(r"""
    var info = [];
    // All tp-yt-paper-item
    var items = document.querySelectorAll("tp-yt-paper-item");
    info.push("tp-yt-paper-item count: " + items.length);
    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        var visible = item.offsetParent !== null ? "visible" : "hidden";
        var txt = (item.textContent || "").trim().replace(/\s+/g, " ").substring(0, 80);
        info.push("  [" + i + "] " + visible + " | " + txt);
    }

    // All role=menuitem
    var menuItems = document.querySelectorAll("[role=menuitem], [role=option]");
    info.push("\nrole=menuitem count: " + menuItems.length);
    for (var i = 0; i < menuItems.length; i++) {
        var item = menuItems[i];
        var visible = item.offsetParent !== null ? "visible" : "hidden";
        var txt = (item.textContent || "").trim().replace(/\s+/g, " ").substring(0, 80);
        info.push("  [" + i + "] " + visible + " | " + txt);
    }

    // ytcp-ve items
    var veItems = document.querySelectorAll("ytcp-ve");
    info.push("\nytcp-ve count: " + veItems.length);
    for (var i = 0; i < veItems.length; i++) {
        var item = veItems[i];
        var visible = item.offsetParent !== null ? "visible" : "hidden";
        var txt = (item.textContent || "").trim().replace(/\s+/g, " ").substring(0, 80);
        if (txt && visible === "visible") {
            info.push("  [" + i + "] " + visible + " | " + txt);
        }
    }

    return info.join("\n");
""")
print("\n[MENU ITEMS]")
print(r4)

# Also check any popup/dropdown that appeared
r5 = driver.execute_script(r"""
    var info = [];
    var popups = document.querySelectorAll("tp-yt-iron-dropdown, ytcp-text-menu, tp-yt-paper-menu-button, [aria-expanded=true]");
    info.push("Popups/dropdowns: " + popups.length);
    for (var p of popups) {
        var vis = p.offsetParent !== null || getComputedStyle(p).display !== "none";
        info.push("  " + p.tagName + " visible=" + vis + " children=" + p.children.length);
        if (vis) {
            var html = p.innerHTML.substring(0, 500);
            info.push("  HTML: " + html);
        }
    }
    return info.join("\n");
""")
print("\n[POPUPS]")
print(r5)

print("\nDone. Check screenshots for visual state.")
