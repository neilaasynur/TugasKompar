from multiprocessing import Process, Manager

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
        words = line.split()        # pisah tiap kata berdasarkan spasi
        word_count += len(words)

    results[index] = word_count     # simpan hasil ke slot milik proses ini


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
        results = manager.list([0] * num_processes)  # shared list antar proses
        processes = []

        # buat dan jalankan semua proses sekaligus
        for i in range(num_processes):
            p = Process(
                target=count_words,
                args=(chunks[i], results, i)
            )
            processes.append(p)
            p.start()               # tiap proses jalan di core CPU sendiri

        # tunggu semua proses selesai
        for p in processes:
            p.join()

        return list(results)        # contoh hasil: [3200, 3150, 3300, 3100]