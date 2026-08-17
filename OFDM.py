import numpy as np
import matplotlib.pyplot as plt

# --- 1. ALT TAŞIYICI YERLEŞTİRME (Subcarrier Mapping) ---
N_fft = 64
subcarriers = np.zeros(N_fft, dtype=complex)

# Tabloya göre 1 ve -1'lerin (BPSK) yerleştirilmesi
# İlk 6 boşluk (0-5) varsayılan olarak 0 kalır.
subcarriers[6:11]  = [1, -1, 1, -1, 1]
subcarriers[11]    = 1  # 1. Pilot
subcarriers[12:25] = [-1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]
subcarriers[25]    = 1  # 2. Pilot
subcarriers[26:32] = [-1, 1, -1, 1, -1, 1]
subcarriers[32] = 0
# 32. indeks DC (Merkez) boşluğu, 0 olarak kalır.
subcarriers[33:39] = [-1, 1, -1, 1, -1, 1]
subcarriers[39]    = 1  # 3. Pilot
subcarriers[40:53] = [-1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]
subcarriers[53]    = -1 # 4. Pilot
subcarriers[54:59] = [-1, 1, -1, 1, -1]
# Son 5 boşluk (59-63) varsayılan olarak 0 kalır.

# --- 2. IFFT İŞLEMİ (Zaman Düzlemine Geçiş) ---
# Numpy'ın standart IFFT fonksiyonunu kullanıyoruz.
ifft_out = np.fft.ifft(subcarriers)

# --- 3. CYCLIC PREFIX (CP) EKLEME ---
CP_length = 16
# IFFT çıkışının son 16 elemanını kopyala
cp = ifft_out[-CP_length:] 
# Kopyalanan bu tamponu orijinal dalganın en başına ekle (Toplam 80 eleman)
ofdm_symbol = np.concatenate((cp, ifft_out))

# --- RAPORLAMA VE ÇIKTILAR (Hocaya Sunulacak Kısım) ---
print("--- VIVADO İLE KARŞILAŞTIRILACAK DEĞERLER ---")
for i in range(64):
    # Satırın son elemanıysa (5'in katı) VEYA listenin tam son elemanıysa (i == 63)
    if (i + 1) % 4 == 0 or i == 63:
        print(f"İndeks {i}: Real={ofdm_symbol[i].real:.4f}, Imag={ofdm_symbol[i].imag:.4f}\n")
        # Burada 'end' parametresi vermediğimiz için otomatik olarak | koymadan alt satıra geçer.
    else:
        # Satır ortası elemanları için yan yana yazıp | eklemeye devam et.
        print(f"İndeks {i}: Real={ofdm_symbol[i].real:.4f}, Imag={ofdm_symbol[i].imag:.4f}", end="    |    ")

# Zaman Dalgasının Çizdirilmesi (Hocanın raporunda çok şık duracaktır)
plt.figure(figsize=(10, 4))
plt.plot(ofdm_symbol.real, label="Gerçel (I)", marker='.', color='blue')
plt.plot(ofdm_symbol.imag, label="Sanal (Q)", marker='.', color='orange')
plt.axvline(x=15.5, color='red', linestyle='--', label='Cyclic Prefix Bitişi')
plt.title("Zaman Düzleminde OFDM Sembolü (80 Örnek)")
plt.xlabel("Örnek (Sample) İndeksi")
plt.ylabel("Genlik (Volt)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()