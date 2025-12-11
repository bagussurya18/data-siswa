

import os
from typing import Dict, List, Tuple, Any

DB_FILENAME = "database_siswa.txt"



def load_data_from_file(filename: str) -> Dict[str, Dict[str, Any]]:

    data: Dict[str, Dict[str, Any]] = {}
    if not os.path.exists(filename):
        return data

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
         
            parts = line.split(",", 2)
           
            if len(parts) < 2:
                continue
            nis = parts[0].strip()
            nama = parts[1].strip()
            nilai_list: List[int] = []
            if len(parts) == 3 and parts[2].strip():
                raw_vals = parts[2].strip()
            
                try:
                    nilai_tokens = [x.strip() for x in raw_vals.split(";") if x.strip()]
                    for t in nilai_tokens:
                     
                        try:
                            nilai_list.append(int(t))
                        except ValueError:
                          
                            continue
                except Exception:
                    nilai_list = []

            data[nis] = {"nama": nama, "nilai": nilai_list}
    return data


def save_data_to_file(filename: str, data: Dict[str, Dict[str, Any]]) -> None:

    lines: List[str] = []
    for nis, info in data.items():
        nama = info.get("nama", "").strip()
        nilai_list = info.get("nilai", [])
       
        nilai_str = ";".join(str(int(v)) for v in nilai_list) if nilai_list else ""
        line = f"{nis},{nama},{nilai_str}"
        lines.append(line)

    with open(filename, "w", encoding="utf-8") as f:
        for ln in lines:
            f.write(ln + "\n")


def compute_stats(nilai_list: List[int]) -> Tuple[float, int, int, str]:

    if not nilai_list:
        avg = 0.0
        mx = 0
        mn = 0
    else:
        mx = max(nilai_list)
        mn = min(nilai_list)
        avg = sum(nilai_list) / len(nilai_list)

    grade = determine_grade(avg)
    return (avg, mx, mn, grade)


def determine_grade(average: float) -> str:
    
    if average >= 85:
        return "A"
    elif average >= 75:
        return "B"
    elif average >= 65:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "E"




def lihat_daftar_siswa(data_siswa: Dict[str, Dict[str, Any]]) -> None:
   
    if not data_siswa:
        print("Belum ada data siswa.")
        return

    print("Daftar Siswa:")
    for nis in sorted(data_siswa.keys(), key=lambda x: x):
        nama = data_siswa[nis].get("nama", "")
        print(f"{nis}: {nama}")


def lihat_detail_siswa(data_siswa: Dict[str, Dict[str, Any]]) -> None:
  
    nis = input("Masukkan NIS yang ingin dilihat: ").strip()
    if nis == "":
        print("NIS tidak boleh kosong.")
        return

    if nis not in data_siswa:
        print(f"Error: NIS {nis} tidak ditemukan.")
        return

    info = data_siswa[nis]
    nama = info.get("nama", "")
    nilai_list = info.get("nilai", [])

    avg, mx, mn, grade = compute_stats(nilai_list)

    print("----- Detail Siswa -----")
    print(f"NIS   : {nis}")
    print(f"Nama  : {nama}")
    print("Nilai :", end=" ")
    if nilai_list:
        print(", ".join(str(int(v)) for v in nilai_list))
    else:
        print("(Belum ada nilai)")

    print(f"Rata-rata : {avg:.2f}")
    print(f"Nilai Tertinggi : {mx}")
    print(f"Nilai Terendah   : {mn}")
    print(f"Grade Akhir      : {grade}")
    print("------------------------")


def tambah_siswa_baru(data_siswa: Dict[str, Dict[str, Any]]) -> Tuple[bool, str]:

    nis = input("Masukkan NIS baru: ").strip()
    if nis == "":
        return (False, "NIS tidak boleh kosong.")
    if nis in data_siswa:
        return (False, f"NIS {nis} sudah ada. Tambah siswa dibatalkan.")

    nama = input("Masukkan Nama Lengkap: ").strip()
    if nama == "":
        return (False, "Nama tidak boleh kosong.")

    data_siswa[nis] = {"nama": nama, "nilai": []}
    return (True, f"Siswa dengan NIS {nis} berhasil ditambahkan.")


def tambah_nilai_siswa(data_siswa: Dict[str, Dict[str, Any]]) -> Tuple[bool, str]:

    nis = input("Masukkan NIS siswa: ").strip()
    if nis == "":
        return (False, "NIS tidak boleh kosong.")
    if nis not in data_siswa:
        return (False, f"Error: NIS {nis} tidak ditemukan."
                      f" Penambahan nilai dibatalkan.")

    nilai_str = input("Masukkan nilai baru (angka 0-100): ").strip()
    try:
        nilai = int(nilai_str)
    except ValueError:
        return (False, "Input tidak valid. Harap masukkan angka bulat untuk nilai.")

    if nilai < 0 or nilai > 100:
        return (False, "Nilai harus berada di rentang 0 hingga 100.")

    data_siswa[nis]["nilai"].append(nilai)
    return (True, f"Nilai {nilai} berhasil ditambahkan untuk NIS {nis}.")


def simpan_dan_keluar(data_siswa: Dict[str, Dict[str, Any]]) -> None:
 
    save_data_to_file(DB_FILENAME, data_siswa)
    print("Data berhasil disimpan. Program berakhir.")




def main() -> None:
    print("--- Sistem Informasi Siswa ---")

   
    data_semua_siswa = load_data_from_file(DB_FILENAME)
    if data_semua_siswa:
        print(f"Memuat {len(data_semua_siswa)} siswa dari '{DB_FILENAME}'.")
    else:
        if os.path.exists(DB_FILENAME):
            print(f"File '{DB_FILENAME}' ditemukan namun tidak ada data valid di dalamnya atau kosong.")
        else:
            print(f"File '{DB_FILENAME}' tidak ditemukan. Memulai dengan data kosong.")

    while True:
        print("\n--- Menu Utama ---")
        print("1. Lihat Daftar Siswa")
        print("2. Lihat Detail Siswa")
        print("3. Tambah Siswa Baru")
        print("4. Tambah Nilai Siswa")
        print("5. Simpan & Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            lihat_daftar_siswa(data_semua_siswa)
        elif pilihan == "2":
            lihat_detail_siswa(data_semua_siswa)
        elif pilihan == "3":
            status, pesan = tambah_siswa_baru(data_semua_siswa)
            print(pesan)
        elif pilihan == "4":
            status, pesan = tambah_nilai_siswa(data_semua_siswa)
            print(pesan)
        elif pilihan == "5":
            simpan_dan_keluar(data_semua_siswa)
            break
        else:
            print("Pilihan tidak dikenali. Silakan masukkan angka 1-5.")


if __name__ == "__main__":
    main()