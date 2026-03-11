# bagian fatin
def baca_file(nama_file):
# mencoba untuk membuka dan membaca file
    try:
        # buka file dengan mode baca dan encoding latin-1(cara komputer membaca karakter khusus jika ada)
        with open(nama_file, 'r', encoding='latin-1') as file:
        #baca semua baris pada file
            baris = file.readlines()
        #menampilkan pesan jika file berhasil atau sukses fibaca
        print(f"File '{nama_file}' berhasil dibaca!")
        # dan program akan menghitung jumlah baris yang dibaca dan menampilkan hasilnya
        print(f"Total baris: {len(baris)}")
        # artinya mengembalikan data pada baris ke fungsi baris yang memanggilnya, sehingga data tersebut dapat digunakan untuk proses selanjutnya
        return baris
    
#Jika data tidak ditemukan maka 
    except FileNotFoundError:
    # maka file data tidak ada dan akan mengeluarkan pesan bahwa file tidak ditemukan
        print(f"File '{nama_file}' tidak ada!") 
        return None

    # misalnya terdaoat eror lain seperti harus ada akses atau selebihnya maka 
    except Exception as e:
        #akan mengeluarkan pesan bahwa file tak dapat dibaca
        print(f"Terdapat kesalahan saat membaca file: {e}")
        return None


# akan di run ketika file dapat atau berhasil dibuka langsung
if __name__ == "__main__":
    #membaca nama file yang akan dibaca
    nama_file = "brokenstring.txt"
    # memanggil fungsi pada baca_file yang sebelumnya sudah dibuat, dan hasilnya akann disimpan ke variabel
    data = baca_file(nama_file)
    # cek apakah file berhasil diproses atau tidak, jika gagal maka file tak akan ditampilkan
    if data is not None:
        print("Data berhasil diproses!")