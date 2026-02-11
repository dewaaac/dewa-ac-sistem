import os, time, subprocess, requests, platform, psutil, hashlib, json


URL_HOSTING = "https://website-kamu.com/index.php"
AUTH_TOKEN = "DEWA_SIG_2026_XYZ"

FORBIDDEN_KEYWORDS = ["antena", "headshot", "aimlock", "regedit", "modmenu", "bypass", "injector", "ffh4x", "ruok", "cheat", "hack"]
BANNED_APPS = ["game guardian", "mt manager", "lucky patcher", "lulu box", "tiktok lite", "facebook lite"]

def get_hwid():
    raw = f"{platform.machine()}{platform.processor()}{platform.node()}"
    return hashlib.md5(raw.encode()).hexdigest()[:8].upper()

def check_history():
    traces = []
    # Cek folder download & WA
    paths = ["/sdcard/Download", "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Documents"]
    for p in paths:
        if os.path.exists(p):
            for f in os.listdir(p):
                if any(k in f.lower() for k in FORBIDDEN_KEYWORDS):
                    traces.append(f"TRACE:{f}")
    return traces

def scan():
    score = 10
    det = []
    # 1. Root Check
    if os.path.exists("/data/adb/magisk") or os.path.exists("/system/bin/su"):
        return 100, ["DEVICE_ROOTED"]
    # 2. History Check
    tr = check_history()
    if tr: score += 50; det.extend(tr)
    # 3. Process Check
    for p in psutil.process_iter(['name']):
        try:
            if any(a in p.info['name'].lower() for a in BANNED_APPS):
                score += 45; det.append(p.info['name'].upper())
        except: continue
    return min(score, 100), list(set(det))

def main():
    os.system('clear')
    print("\033[92m[+] DEWA ANTI-CHEAT SYSTEM ACTIVE\033[0m")
    nick = input("Input Nickname: ")
    hwid = get_hwid()

    while True:
        score, findings = scan()
        details = ", ".join(findings) if findings else "CLEAN"
        
        # Ambil Lokasi (Termux-API harus terpasang)
        loc = "UNKNOWN"
        try:
            res = subprocess.run(["termux-location"], capture_output=True, text=True, timeout=5)
            ld = json.loads(res.stdout); loc = f"{ld['latitude']},{ld['longitude']}"
        except: pass

        # Kirim ke Dashboard
        try:
            payload = {"auth_token": AUTH_TOKEN, "nickname": nick, "score": score, "details": details, "device": hwid, "location": loc}
            requests.post(URL_HOSTING, data=payload, timeout=10)
            
            if score >= 90:
                print(f"\033[91m[!] CHEAT DETECTED: {details}. KICKING...\033[0m")
                subprocess.run(["am", "force-stop", "com.dts.freefireth"], capture_output=True)
                os._exit(0)
        except Exception as e:
            print("Sync Error...")
            
        time.sleep(10)

if __name__ == "__main__":
    main()
