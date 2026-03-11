# Program Parallel Word Count
# Menghitung jumlah kata di file teks besar menggunakan komputasi paralel

import os
from multiprocessing import Process, Manager


# =============================================================
# ANGGOTA 1 — Baca File (Fatin)
# =============================================================

def baca_file(nama_file):
    # fungsi ini bertugas membuka dan membaca isi file teks
    try:
        # buka file, encoding latin-1 dipakai supaya bisa baca karakter khusus
        with open(nama_file, 'r', encoding='latin-1') as file:
            baris = file.readlines()  # simpan semua baris ke dalam list

        print(f"File '{nama_file}' berhasil dibaca!")
        print(f"Total baris: {len(baris)}")

        return baris  # kirim data baris ke fungsi berikutnya

    except FileNotFoundError:
        # kalau file tidak ditemukan, tampilkan pesan error
        print(f"File '{nama_file}' tidak ada!")
        return None

    except Exception as e:
        # kalau ada error lain yang tidak terduga
        print(f"Terdapat kesalahan saat membaca file: {e}")
        return None


# =============================================================
# ANGGOTA 2 — Pembagi Data
# =============================================================

def data_splitter(lines, num_chunks):
    # fungsi ini membagi semua baris menjadi beberapa bagian (chunk)
    # tujuannya supaya tiap proses punya bagian data sendiri yang dikerjakan

    if not lines:
        # kalau datanya kosong, kembalikan chunk kosong sejumlah num_chunks
        return [[] for _ in range(num_chunks)]

    chunks = []                          # tempat menyimpan hasil pembagian
    total = len(lines)                   # hitung total baris
    ukuran_chunk = total // num_chunks   # ukuran dasar tiap chunk
    sisa = total % num_chunks            # sisa baris yang tidak habis dibagi

    index = 0
    for i in range(num_chunks):
        # kalau ada sisa, beberapa chunk pertama dapat 1 baris ekstra
        ekstra = 1 if i < sisa else 0
        akhir = index + ukuran_chunk + ekstra
        chunks.append(lines[index:akhir])  # potong dan simpan chunk
        index = akhir                      # geser titik awal ke chunk berikutnya

    return chunks  # kirim hasil pembagian ke fungsi berikutnya


# =============================================================
# ANGGOTA 3 — Penghitung Kata (Paralel)
# =============================================================

def count_words(chunk, results, index):
    # fungsi ini dijalankan oleh setiap proses secara bersamaan
    # tugasnya menghitung jumlah kata di bagian (chunk) yang diberikan

    word_count = 0
    for line in chunk:
        words = line.split()       # pisahkan setiap kata berdasarkan spasi
        word_count += len(words)   # tambahkan jumlah kata di baris ini

    # simpan hasil hitungan ke posisi milik proses ini
    results[index] = word_count


def run_parallel(chunks):
    # fungsi ini yang mengatur jalannya komputasi paralel
    # setiap chunk dikirim ke proses yang berbeda dan dijalankan bersamaan

    num_processes = len(chunks)

    with Manager() as manager:
        # buat shared list supaya semua proses bisa menyimpan hasil ke satu tempat
        results = manager.list([0] * num_processes)
        processes = []

        for i in range(num_processes):
            # buat proses baru untuk setiap chunk
            p = Process(
                target=count_words,          # fungsi yang akan dijalankan
                args=(chunks[i], results, i) # data yang dikirim ke fungsi tersebut
            )
            processes.append(p)
            p.start()  # mulai jalankan proses — di sinilah komputasi paralel terjadi

        for p in processes:
            p.join()  # tunggu semua proses selesai sebelum lanjut

        return list(results)  # kembalikan hasil hitungan semua proses


# =============================================================
# ALUR UTAMA — Sambungkan semua bagian
# =============================================================

if __name__ == "__main__":
    nama_file  = "brokenstring.txt"  # nama file yang akan diproses
    num_chunks = os.cpu_count()      # jumlah pembagian = jumlah core CPU di perangkat

    print(f"Jumlah core CPU : {num_chunks}")

    # langkah 1 — baca file (Anggota 1)
    baris = baca_file(nama_file)

    if baris is not None:
        # langkah 2 — bagi data menjadi beberapa bagian (Anggota 2)
        chunks = data_splitter(baris, num_chunks)

        # langkah 3 — hitung kata secara paralel (Anggota 3)
        results = run_parallel(chunks)

        # tampilkan hasil sementara sebelum Anggota 4 selesai
        print(f"Data berhasil diproses!")
        print(f"Hasil tiap proses : {results}")
        print(f"Total kata        : {sum(results)}")