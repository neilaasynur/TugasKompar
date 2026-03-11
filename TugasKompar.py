# =============================================================
# PARALLEL WORD COUNT — Komputasi Paralel dengan Multiprocessing
# =============================================================
# Anggota 1 (Fatin) → baca_file()
# Anggota 2         → data_splitter()
# Anggota 3         → count_words() + run_parallel()
# Anggota 4         → reducer() + tampilkan_output()
# =============================================================

import os
from multiprocessing import Process, Manager


# =============================================================
# ANGGOTA 1 — File Reader (Fatin)
# =============================================================

def baca_file(nama_file):
    try:
        with open(nama_file, 'r', encoding='latin-1') as file:
            baris = file.readlines()
        print(f"File '{nama_file}' berhasil dibaca!")
        print(f"Total baris: {len(baris)}")
        return baris

    except FileNotFoundError:
        print(f"File '{nama_file}' tidak ada!")
        return None

    except Exception as e:
        print(f"Terdapat kesalahan saat membaca file: {e}")
        return None


# =============================================================
# ANGGOTA 2 — Data Splitter
# =============================================================

def data_splitter(lines, num_chunks):
    """Membagi list lines menjadi num_chunks bagian"""

    if not lines:
        return [[] for _ in range(num_chunks)]

    chunks = []
    total = len(lines)
    ukuran_chunk = total // num_chunks
    sisa = total % num_chunks

    index = 0
    for i in range(num_chunks):
        ekstra = 1 if i < sisa else 0
        akhir = index + ukuran_chunk + ekstra
        chunks.append(lines[index:akhir])
        index = akhir

    return chunks


# =============================================================
# ANGGOTA 3 — Multiprocessing Counter
# =============================================================

def count_words(chunk, results, index):
    """
    Menghitung jumlah kata dalam satu chunk (bagian dari file).

    Parameter:
    - chunk   : list of string (baris-baris teks)
    - results : shared list untuk menyimpan hasil tiap proses
    - index   : posisi proses ini di dalam list results
    """
    word_count = 0
    for line in chunk:
        words = line.split()
        word_count += len(words)

    results[index] = word_count


def run_parallel(chunks):
    """
    Menjalankan count_words secara paralel untuk setiap chunk.

    Parameter:
    - chunks : list of list (hasil split dari Anggota 2)

    Return:
    - results : list berisi jumlah kata tiap chunk
    """
    num_processes = len(chunks)

    with Manager() as manager:
        results = manager.list([0] * num_processes)
        processes = []

        for i in range(num_processes):
            p = Process(
                target=count_words,
                args=(chunks[i], results, i)
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        return list(results)


# =============================================================
# ANGGOTA 4 — Reducer + Output
# =============================================================

def reducer(result): #list yang berisi jumlah kata dari setiap chunk
    total_words = sum(result) #jumahkan semua nilai yang ada didalam list result
    return total_words #mengembalikan total kata

def tampilkan_output(total_words, nama_file): #total kata dan nama file yang dihitung
    #Menampilkan hasil akhir ke layar.
    print("\n===== HASIL PERHITUNGAN =====")
    print(f"Nama file yang telah di hitung            : {nama_file}")  # menampilkan nama file
    print(f"Total jumlah kata dari file tersebut      : {total_words}") # menampilkan total kata
    print("=============================")


# =============================================================
# ALUR UTAMA — sambungkan semua modul
# =============================================================

if __name__ == "__main__":
    nama_file  = "brokenstring.txt"   # nama file buku / teks besar

    lines = baca_file(nama_file)      # Anggota 1 → membaca file

    if lines is not None:             # memastikan file berhasil dibaca
        num_chunks = os.cpu_count()   # Anggota 2 → menentukan jumlah core CPU

        chunks = data_splitter(lines, num_chunks)  # Anggota 2 → membagi data menjadi beberapa bagian

        results = run_parallel(chunks)             # Anggota 3 → menjalankan proses paralel untuk menghitung kata

        total_words = reducer(results)             # Anggota 4 → gabungkan hasil semua proses

        tampilkan_output(total_words, nama_file)   # Anggota 4 → menampilkan hasil akhir