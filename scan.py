import os, time, subprocess, requests, platform, psutil, hashlib, json, threading

# --- KONFIGURASI ---
URL_HOSTING = "http://god-eye.my.id/index.php" 
AUTH_TOKEN = "DEWA_SIG_2026_XYZ"

FORBIDDEN_KEYWORDS = ["antena", "headshot", "aimlock", "regedit", "modmenu", "bypass", "injector", "ffh4x", "ruok", "cheat", "hack"]
BANNED_APPS = ["game guardian", "mt manager", "lucky patcher", "lulu box"]

def show_visual_warning(msg):
    # Memunculkan pesan melayang (Toast) di layar HP
    subprocess.run(["termux-toast", "-c", "red", "-g", "top", msg])

def play_audio_warning():
    # Download alarm jika belum ada
    if not os.path.exists("alarm.mp3"):
        url = "https://www.soundjay.com/buttons/beep-01a.mp3"
        try:
            r = requests.get(url); open("alarm.mp3", "wb").write(r.content)
        except: pass
    # Putar suara
    subprocess.run(["play-audio", "alarm.mp3"], capture_output=True)

def get_hwid():
    raw = f"{platform.machine()}{platform.processor()}{platform.node()}"
    return hashlib.md5(raw.encode()).hexdigest()[:8].upper()

def scan():
    score = 10
    det = []
    if os.path.exists("/data/adb/magisk") or os.path.exists("/system/bin/su"):
        return 100, ["DEVICE_ROOTED"]
    
    # Cek Folder Download
    path = "/sdcard/Download"
    if os.path.exists(path):
        for f in os.listdir(path):
            if any(k in f.lower() for k in FORBIDDEN_KEYWORDS):
                det.append(f"FILE:{f}")
                score += 50
                
    return min(score, 100), list(set(det))

def main():
    os.system('clear')
    print("\033[92m[+] GOD-EYE SYSTEM ACTIVE\033[0m")
    nick = input("Input Nickname: ")
    hwid = get_hwid()

    while True:
        score, findings = scan()
        details = ", ".join(findings) if findings else "CLEAN"
        
        # --- EFEK VISUAL & SUARA JIKA TERDETEKSI ---
        if score >= 90:
            msg = f"PERINGATAN: {nick} TERDETEKSI CHEAT! DATA DIKIRIM KE PANITIA!"
            # Jalankan di background agar tidak macet
            threading.Thread(target=show_visual_warning, args=(msg,)).start()
            threading.Thread(target=play_audio_warning).start()

        # Kirim ke Dashboard
        try:
            payload = {"auth_token": AUTH_TOKEN, "nickname": nick, "score": score, "details": details, "device": hwid}
            requests.post(URL_HOSTING, data=payload, timeout=10, verify=False)
            print(f"[*] Status: Synced | Score: {score}%")
            
            if score >= 101: # Ubah ke 90 jika ingin langsung kick pemain asli
                subprocess.run(["am", "force-stop", "com.dts.freefireth"], capture_output=True)
                os._exit(0)
        except:
            print("Sync Error...")
            
        time.sleep(10)

if __name__ == "__main__":
    main()
