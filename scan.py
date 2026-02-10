import os, time, subprocess, requests, platform

# KONFIGURASI SINKRONISASI
URL_HOSTING = "http://god-eye.my.id/index.php" # Pastikan URL ini benar
AUTH_TOKEN = "DEWA_SIG_2026_XYZ"

def capture(name):
    # Nama file unik
    filename = f"evidence_{int(time.time())}.png"
    try:
        # Coba cara 1: Termux-API (Harus install pkg install termux-api)
        subprocess.run(["termux-screenshot", filename], capture_output=True)
        
        # C_oba cara 2: Jika cara 1 gagal
        if not os.path.exists(filename):
            subprocess.run(["screencap", "-p", filename])
            
        if os.path.exists(filename):
            return filename
    except:
        return None
    return None

def main():
    print(" === DEWA ANTI-CHEAT SCANNER v2.6 === ")
    nickname = input(" Masukkan Nickname: ")
    
    # Simulasi Scan (Ganti dengan logika scan kamu)
    print(" Sedang memindai file...")
    time.sleep(2)
    score = 80 # Contoh skor deteksi
    
    # Ambil Bukti jika skor tinggi
    file_bukti = None
    if score > 30:
        print(" [!] Aktivitas mencurigakan! Mengambil bukti...")
        file_bukti = capture(nickname)
    
    # Kirim Data ke Website
    data = {
        "auth_token": AUTH_TOKEN,
        "nickname": nickname,
        "score": score,
        "device": platform.machine()
    }
    
    files = {}
    if file_bukti and os.path.exists(file_bukti):
        files = {"evidence": open(file_bukti, "rb")}
        
    try:
        response = requests.post(URL_HOSTING, data=data, files=files)
        if response.text == "OK":
            print(" [+] Data & Bukti Berhasil Dikirim!")
        else:
            print(f" [-] Server merespon: {response.text}")
    except Exception as e:
        print(f" [!] Gagal terhubung ke server: {e}")

    # Hapus file sampah di HP setelah dikirim
    if file_bukti and os.path.exists(file_bukti):
        os.remove(file_bukti)

if __name__ == "__main__":
    main()
