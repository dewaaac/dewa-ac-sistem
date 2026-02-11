import os, time, subprocess, requests, platform, psutil, hashlib, json

# --- KONFIGURASI SINKRONISASI ---
# Gunakan http karena belum ada SSL
URL_HOSTING = "http://god-eye.my.id/index.php" 
AUTH_TOKEN = "DEWA_SIG_2026_XYZ"

FORBIDDEN_KEYWORDS = ["antena", "headshot", "aimlock", "regedit", "modmenu", "bypass", "injector", "ffh4x", "ruok", "cheat", "hack"]
BANNED_APPS = ["game guardian", "mt manager", "lucky patcher", "lulu box", "tiktok lite", "facebook lite"]

def capture():
    filename = f"evid_{int(time.time())}.png"
    try:
        # Cara 1: Termux-API
        subprocess.run(["termux-screenshot", filename], capture_output=True)
        if not os.path.exists(filename):
            # Cara 2: Generic Android
            subprocess.run(["screencap", "-p", filename], capture_output=True)
        
        if os.path.exists(filename):
            return filename
    except:
        return None
    return None

def get_hwid():
    raw = f"{platform.machine()}{platform.processor()}{platform.node()}"
    return hashlib.md5(raw.encode()).hexdigest()[:8].upper()

def check_history():
    traces = []
    paths = ["/sdcard/Download", "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Documents"]
    for p in paths:
        if os.path.exists(p):
            try:
                for f in os.listdir(p):
                    if any(k in f.lower() for k in FORBIDDEN_KEYWORDS):
                        traces.append(f"TRACE:{f}")
            except: continue
    return traces

def scan():
    score = 10
    det = []
    # 1. Root Check
    if os.path.exists("/data/adb/magisk") or os.path.exists("/system/bin/su"):
        return 100, ["DEVICE_ROOTED"]
    # 2. History Check
    tr = check_history()
    if tr: 
        score += 50
        det.extend(tr)
    # 3. Process Check
    for p in psutil.process_iter(['name']):
        try:
            if any(a in p.info['name'].lower() for a in BANNED_APPS):
                score += 45
                det.append(p.info['name'].upper())
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
        
        # Ambil Lokasi
        loc = "UNKNOWN"
        try:
            res = subprocess.run(["termux-location"], capture_output=True, text=True, timeout=5)
            ld = json.loads(res.stdout)
            loc = f"{ld['latitude']},{ld['longitude']}"
        except: pass

        # Ambil Bukti Screenshot jika terdeteksi
        file_bukti = None
        files = {}
        if score > 50:
            file_bukti = capture()
            if file_bukti:
                files = {"ss": open(file_bukti, "rb")}

        # Kirim ke Dashboard
        try:
            payload = {
                "auth_token": AUTH_TOKEN, 
                "nickname": nick, 
                "score": score, 
                "details": details, 
                "device": hwid, 
                "location": loc
            }
            # verify=False digunakan karena tidak ada SSL
            response = requests.post(URL_HOSTING, data=payload, files=files, timeout=15, verify=False)
            
            if response.status_code == 200:
                print(f"\033[94m[*] Synced | Score: {score}% | Status: OK\033[0m")
            else:
                print(f"\033[33m[!] Server Error: {response.status_code}\033[0m")
            
            # Tutup file agar bisa dihapus
            if files: files["ss"].close()
            if file_bukti: os.remove(file_bukti)

            # Eksekusi Hukuman
            if score >= 90:
                print(f"\033[91m[!] CHEAT DETECTED! KICKING...\033[0m")
                subprocess.run(["am", "force-stop", "com.dts.freefireth"], capture_output=True)
                os._exit(0)

        except Exception as e:
            print(f"\033[91m[!] Sync Error: {e}\033[0m")
            
        time.sleep(10)

if __name__ == "__main__":
    main()
