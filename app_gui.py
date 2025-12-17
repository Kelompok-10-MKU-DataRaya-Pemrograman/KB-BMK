import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import sqlite3
from datetime import datetime
import os

class KBBMKApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KB-BMK: Kalkulator Biaya Bongkar Muat")
        self.root.geometry("900x600")
        
        # Konfigurasi Database
        self.db_name = 'riwayat_biaya.db'
        self.setup_database()

        # --- UI COMPONENTS ---
        
        # 1. Header Frame
        header_frame = tk.Frame(root, bg="#2c3e50", pady=10)
        header_frame.pack(fill="x")
        
        lbl_title = tk.Label(header_frame, text="Sistem Manajemen KB-BMK", 
                             font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
        lbl_title.pack()
        lbl_subtitle = tk.Label(header_frame, text="Manajemen Pelabuhan dan Logistik Maritim", 
                                font=("Arial", 10), bg="#2c3e50", fg="#bdc3c7")
        lbl_subtitle.pack()

        # 2. Control Frame (Input & Buttons)
        control_frame = tk.Frame(root, pady=10, padx=10)
        control_frame.pack(fill="x")

        self.btn_browse = tk.Button(control_frame, text="📂 Pilih File CSV", command=self.load_csv, 
                                    bg="#3498db", fg="white", font=("Arial", 10, "bold"), padx=10)
        self.btn_browse.pack(side="left", padx=5)

        self.lbl_filename = tk.Label(control_frame, text="Belum ada file dipilih...", fg="gray")
        self.lbl_filename.pack(side="left", padx=5)

        self.btn_process = tk.Button(control_frame, text="⚙️ Hitung & Simpan", command=self.process_data, 
                                     bg="#27ae60", fg="white", font=("Arial", 10, "bold"), state="disabled", padx=10)
        self.btn_process.pack(side="right", padx=5)

        # 3. Info Frame (Tarif)
        info_frame = tk.LabelFrame(root, text="Informasi Tarif", padx=10, pady=5)
        info_frame.pack(fill="x", padx=10)
        tk.Label(info_frame, text="20 Feet: Rp 500,000 | 40 Feet: Rp 900,000").pack(anchor="w")

        # 4. Result Table (Treeview)
        table_frame = tk.Frame(root, pady=10, padx=10)
        table_frame.pack(fill="both", expand=True)

        columns = ("no", "pelabuhan", "jenis", "jumlah", "tarif", "total")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Definisi Kolom
        self.tree.heading("no", text="No")
        self.tree.heading("pelabuhan", text="Pelabuhan")
        self.tree.heading("jenis", text="Jenis Kontainer")
        self.tree.heading("jumlah", text="Jumlah")
        self.tree.heading("tarif", text="Tarif Satuan")
        self.tree.heading("total", text="Total Biaya")
        
        self.tree.column("no", width=40, anchor="center")
        self.tree.column("jumlah", width=80, anchor="center")
        self.tree.column("tarif", width=120, anchor="e")
        self.tree.column("total", width=150, anchor="e")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 5. Footer Stats
        self.lbl_stats = tk.Label(root, text="Total Record: 0 | Grand Total Biaya: Rp 0", 
                                  font=("Arial", 10, "bold"), bg="#ecf0f1", pady=10)
        self.lbl_stats.pack(fill="x")

        # Variables
        self.current_data = [] # Menyimpan data yang sedang dimuat
        self.csv_path = None

    def setup_database(self):
        """Setup SQLite database sesuai spesifikasi."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS perhitungan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                waktu_eksekusi TEXT,
                pelabuhan TEXT,
                jenis_kontainer TEXT,
                jumlah INTEGER,
                tarif_per_kontainer INTEGER,
                total_biaya INTEGER
            )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal inisialisasi database: {e}")

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        self.csv_path = file_path
        self.lbl_filename.config(text=os.path.basename(file_path), fg="black")
        
        # Reset Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.current_data = []

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                # Cek delimiter otomatis (karena kadang ; kadang ,)
                dialect = csv.Sniffer().sniff(file.read(1024))
                file.seek(0)
                csv_reader = csv.DictReader(file, delimiter=dialect.delimiter)
                
                # Normalisasi Nama Kolom (Agar support file manual & big data)
                headers = csv_reader.fieldnames
                col_pelabuhan = next((h for h in headers if 'Pelabuhan' in h), None)
                col_jenis = next((h for h in headers if 'Jenis' in h), None) # Bisa 'Jenis' atau 'Jenis Kontainer'
                col_jumlah = next((h for h in headers if 'Jumlah' in h), None)

                if not (col_pelabuhan and col_jenis and col_jumlah):
                    messagebox.showerror("Error CSV", "Format CSV tidak dikenali. Pastikan ada kolom Pelabuhan, Jenis, dan Jumlah.")
                    return

                count = 0
                for row in csv_reader:
                    count += 1
                    try:
                        p_pelabuhan = row[col_pelabuhan]
                        
                        # --- LOGIKA PEMBERSIHAN DATA JENIS ---
                        # Mengubah "20 feet" menjadi "20" agar perhitungan cocok
                        raw_jenis = row[col_jenis].lower().replace("feet", "").strip()
                        
                        p_jumlah = int(row[col_jumlah])
                        
                        # Hitung Biaya
                        tarif = 0
                        if raw_jenis == "20":
                            tarif = 500000
                        elif raw_jenis == "40":
                            tarif = 900000
                        
                        total = tarif * p_jumlah
                        
                        # Simpan ke memori sementara (tambah raw_jenis untuk display nanti)
                        # Format: [Pelabuhan, JenisDisplay, Jumlah, Tarif, Total]
                        data_row = (p_pelabuhan, f"{raw_jenis} feet", p_jumlah, tarif, total)
                        self.current_data.append(data_row)
                        
                        # Masukkan ke Tabel GUI
                        self.tree.insert("", "end", values=(count, p_pelabuhan, f"{raw_jenis} feet", p_jumlah, f"Rp {tarif:,}", f"Rp {total:,}"))
                        
                    except ValueError:
                        continue # Skip baris error

            self.update_stats()
            self.btn_process.config(state="normal") # Aktifkan tombol proses

        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca file: {e}")

    def update_stats(self):
        total_rec = len(self.current_data)
        grand_total = sum(item[4] for item in self.current_data)
        self.lbl_stats.config(text=f"Total Record: {total_rec} | Grand Total Biaya: Rp {grand_total:,}")

    def process_data(self):
        """Simpan ke Database dan Export CSV Output"""
        if not self.current_data:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Simpan Database
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            data_db = []
            for row in self.current_data:
                # row structure: (pelabuhan, jenis_display, jumlah, tarif, total)
                data_db.append((timestamp, row[0], row[1], row[2], row[3], row[4]))

            cursor.executemany('''
            INSERT INTO perhitungan (
                waktu_eksekusi, pelabuhan, jenis_kontainer, jumlah, tarif_per_kontainer, total_biaya
            ) VALUES (?, ?, ?, ?, ?, ?)
            ''', data_db)
            
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal menyimpan ke DB: {e}")
            return

        # 2. Export CSV
        output_filename = f"output_biaya_{timestamp}.csv"
        try:
            with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Pelabuhan', 'Jenis Kontainer', 'Jumlah', 'Tarif per Kontainer', 'Total Biaya'])
                writer.writerows(self.current_data)
            
            messagebox.showinfo("Sukses", f"Data berhasil diproses!\n\nDisimpan ke DB: {self.db_name}\nExport CSV: {output_filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Gagal membuat file output: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KBBMKApp(root)
    root.mainloop()