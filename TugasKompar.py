# =============================================================
# PARALLEL WORD COUNT — Komputasi Paralel dengan Multiprocessing
# =============================================================
# Anggota 1 (Fatin) → baca_file()
# Anggota 2         → data_splitter()
# Anggota 3         → count_words() + run_parallel()
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
# ALUR UTAMA — sambungkan semua modul
# =============================================================

if __name__ == "__main__":
    nama_file   = "brokenstring.txt"        # nama file yang akan diproses
    num_chunks  = os.cpu_count()            # jumlah chunk = jumlah core CPU (dari Anggota 2)

    print(f"Jumlah core CPU : {num_chunks}")

    # Anggota 1 → baca file, hasilnya disimpan ke variabel 'baris'
    baris = baca_file(nama_file)

    if baris is not None:
        # Anggota 2 → terima 'baris' dari Anggota 1, bagi jadi beberapa chunk
        chunks = data_splitter(baris, num_chunks)

        # Anggota 3 → terima 'chunks' dari Anggota 2, proses secara paralel
        results = run_parallel(chunks)

        print(f"Data berhasil diproses!")
        print(f"Hasil tiap proses : {results}")
        print(f"Total kata        : {sum(results)}")