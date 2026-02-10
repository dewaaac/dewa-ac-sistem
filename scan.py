import os, hashlib, requests, subprocess, time, platform

# =========================================================
# KONFIGURASI DOMAIN RESMI DEWA AC
# =========================================================
URL = "http://god-eye.my.id/index.php"
TOKEN = "DEWA_SIG_2026_XYZ"
# =========================================================

def capture(name):
    # Buat nama file yang rapi
    filename = f"evidence_{int(time.time())}.png"
    
    # Lokasi penyimpanan sementara di dalam folder Termux saja (lebih aman)
    # Tidak perlu /sdcard/ agar tidak bentrok dengan izin Android yang ketat
    try:
        # Menjalankan perintah screenshot
        subprocess.run(["screencap", "-p", filename])
        
        # Cek apakah file benar-benar tercipta
        if os.path.exists(filename):
            return filename
        else:
            return None
    except Exception as e:
        print(f" Gagal mengambil gambar: {e}")
        return None

def check_illegal_files():
    # Daftar folder dan file yang paling sering digunakan cheater FF
    bad_files = [
        "/sdcard/Android/data/com.gameguardian",
        "/sdcard/Download/aimbot.lua",
        "/sdcard/Download/regedit.v1",
        "/sdcard/MT2",
        "/sdcard/Download/mod_menu.apk"
    ]
    found = []
    for p in bad_files:
        if os.path.exists(p):
            found.append(p.split('/')[-1])
    return found

print("\n" + "="*45)
print("       DEWA AC - GOD EYE ARMORED SYSTEM")
print("="*45)
print("     DOMAIN: god-eye.my.id | SECURE ON")
print("="*45)

name = input("[?] Masukkan Nickname Turnamen: ")
print("\n[*] Menjalankan Protokol Pemindaian...")
time.sleep(1.5)

# --- PROSES ANALISIS ---
threats = check_illegal_files()
score = 0

# Logika Skor Risiko
if len(threats) > 0: 
    score += 80  # Terdeteksi file ilegal (Critical)
if os.path.exists("/system/xbin/su") or os.path.exists("/system/app/Superuser.apk"):
    score += 20  # Terdeteksi Root

# --- PENGAMBILAN BUKTI ---
img_path = None
if score > 30:
    print("[!] RISIKO TINGGI TERDETEKSI! Memotret layar...")
    img_path = capture(name)

# --- PENGIRIMAN DATA KE SERVER ---
payload = {
    'auth_token': TOKEN,
    'nickname': name,
    'score': score,
    'device': platform.machine()
}

print("[*] Mengirim laporan forensic ke Dashboard Admin...")

try:
    if img_path:
        with open(img_path, 'rb') as f:
            files = {'evidence': f}
            r = requests.post(URL, data=payload, files=files, timeout=20)
        if os.path.exists(img_path):
            os.remove(img_path) # Bersihkan file di HP pemain
    else:
        r = requests.post(URL, data=payload, timeout=20)

    if r.status_code == 200:
        print("\n[+] VERIFIKASI SELESAI!")
        print("[+] Status: Data Terkirim.")
        print("[+] Anda diizinkan bermain jika tidak ada panggilan Admin.")
    else:
        print("\n[-] GAGAL: Server sibuk (Error 01)")
except Exception as e:
    print(f"\n[-] GAGAL: Tidak bisa menghubungi domain god-eye.my.id (Error 02)")

print("="*45)
