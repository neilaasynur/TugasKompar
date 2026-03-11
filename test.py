# data splitter untuk membagi data menjadi beberapa bagian sesuai jumlah core CPU
import os #mengimport modul os untuk mendapatkan jumlah core CPU

def data_splitter(lines, num_chunks):
    """Membagi list lines menjadi num_chunks bagian"""

    if not lines:  # jika list kosong, kembalikan list kosong
        return [[] for _ in range(num_chunks)]

    chunks = [] # list untuk menyimpan hasil pembagian
    total = len(lines) # total baris yang akan dibagi
    ukuran_chunk = total // num_chunks  # bulat ke bawah
    sisa = total % num_chunks           # sisa baris yang tidak terbagi rata

    index = 0  # titik awal
    for i in range(num_chunks):
        ekstra = 1 if i < sisa else 0 # tambahkan 1 baris ekstra untuk sisa yang belum terbagi
        akhir = index + ukuran_chunk + ekstra # titik akhir untuk chunk ini
        chunks.append(lines[index:akhir]) # tambahkan chunk ke hasil
        index = akhir # update titik awal untuk chunk berikutnya

    return chunks


# hanya jalan kalau file ini dijalankan langsung
if __name__ == "__main__":
    num_chunks = os.cpu_count()  # otomatis baca core CPU device
    print(f"Jumlah core CPU  : {num_chunks}")

    contoh = [f"baris{i}" for i in range(1, 11)]  # simulasi 10 baris
    hasil = data_splitter(contoh, num_chunks) # panggil fungsi pembagi data

    for i, chunk in enumerate(hasil): # tampilkan hasil pembagian
        print(f"Chunk {i+1}: {chunk}") # tampilkan setiap chunk dengan nomor urutnya