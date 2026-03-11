#bagian output yang menggabungkan semua hasil perhitungan setiap proses yang telah dijalani

def reducer (result): #list yang berisi jumlah kata dari setiap chunk

    total_words = sum(result) #jumahkan semua nilai yang ada didalam list result
    return total_words #mengembalika total kata

def tampilkan_output(total_words, nama_file): #total kata dan nama file yang dihitung
    #Menampilkan hasil akhir ke layar.

    print("\n===== HASIL PERHITUNGAN =====")
    print(f"Nama file yang telah di hitung            : {nama_file}")  # menampilkan nama file
    print(f"Total jumlah kata dari file tersebut      : {total_words}") # menampilkan total kata
    print("=============================")


# program utama yang menggabungkan semua bagian
if __name__ == "__main__":

    import os

    # import fungsi 
    from baca_file import baca_file
    from data_splitter import data_splitter
    from word_counter import run_parallel

    nama_file = "brokenstring.txt"   # nama file buku / teks besar

    lines = baca_file(nama_file) # digunakan untuk membaca file

    if lines is not None:  # memastikan file berhasil dibaca
        num_chunks = os.cpu_count() # menentukan jumlah core CPU

        chunks = data_splitter(lines, num_chunks) #m embagi data menjadi beberapa bagian

        results = run_parallel(chunks) # menjalankan proses paralel untuk menghitung kata

        total_words = reducer(results)  # gabungkan hasil semua proses

        tampilkan_output(total_words, nama_file) # digunakna untuk menampilkan hasil akhir