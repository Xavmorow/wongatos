from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
from datetime import datetime

# Data global
antrian = []  # Format: (id, nama, kendaraan, servis, tanggal, status)
stocks = {
    "Oli": 10,
    "Ban": 8,
    "Vanbelt": 5,
    "Kampas Rem": 7
}
layanan_servis = {
    "Ganti oli": 50000,
    "Servis berat": 250000,
    "Servis ringan": 150000,
    "Tambal ban": 20000,
}
opsi_servis = list(layanan_servis.keys())

class AdminMainMenu:
    def __init__(self, root, admin_instance):
        self.root = root
        self.admin_instance = admin_instance
        self.root.title("Admin Panel - Bengkel Proper")
        self.root.geometry("600x200")
        self.root.configure(bg="#6A9AB0")
        self.root.minsize(600, 200)  # Ukuran minimum agar tombol terlihat
        
        # Frame untuk tombol, diletakkan di tengah
        self.btn_frame = tk.Frame(self.root, bg="#6A9AB0")
        self.btn_frame.pack(expand=True, fill="both")
        
        # Frame dalam untuk tombol agar tetap dari kiri ke kanan
        self.inner_btn_frame = tk.Frame(self.btn_frame, bg="#6A9AB0")
        self.inner_btn_frame.pack(expand=True)
        
        # Tombol utama, diatur dari kiri ke kanan
        self.manage_pelanggan_btn = tk.Button(self.inner_btn_frame, text="Manage Pelanggan", font=("poppins", 11, "bold"),
                                             command=lambda: [self.btn_frame.pack_forget(), admin_instance.show_manage_pelanggan()])
        self.manage_pelanggan_btn.pack(side="left", padx=5, pady=5)
        self.manage_produk_btn = tk.Button(self.inner_btn_frame, text="Manage Produk", font=("poppins", 11, "bold"),
                                          command=lambda: [self.btn_frame.pack_forget(), admin_instance.show_manage_barang()])
        self.manage_produk_btn.pack(side="left", padx=5, pady=5)
        self.manage_servis_btn = tk.Button(self.inner_btn_frame, text="Manage Servis", font=("poppins", 11, "bold"),
                                          command=lambda: [self.btn_frame.pack_forget(), admin_instance.show_manage_servis()])
        self.manage_servis_btn.pack(side="left", padx=5, pady=5)
        self.laporan_transaksi_btn = tk.Button(self.inner_btn_frame, text="Laporan Transaksi", font=("poppins", 11, "bold"),
                                              command=lambda: [self.btn_frame.pack_forget(), admin_instance.show_laporan_transaksi()])
        self.laporan_transaksi_btn.pack(side="left", padx=5, pady=5)
        self.logout_btn = tk.Button(self.inner_btn_frame, text="Logout", font=("poppins", 11, "bold"), width=15,
                                   bg="#FF5555", fg="#f5f5f5", command=admin_instance.logout)
        self.logout_btn.pack(side="left", padx=5, pady=5)

    def show(self):
        self.btn_frame.pack(expand=True, fill="both")



class AdminMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin Panel - Bengkel Proper")
        self.root.geometry("1000x700")
        self.root.configure(bg="#6A9AB0")
        self.root.minsize(1000, 700)

        # Judul
        title_label = tk.Label(self.root, text="Hallo, Admin!", font=("poppins", 20, "bold"),
                              bg="#6A9AB0", fg="white")
        title_label.pack(pady=20)

        # Frame untuk tombol utama
        self.admin_main_menu = AdminMainMenu(self.root, self)

        # Frame untuk konten
        self.content_frame = tk.Frame(self.root, bg="#6A9AB0")
        self.content_frame.pack(fill="both", expand=True)

        self.root.mainloop()

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        app = AplikasiLogin(root)
        root.mainloop()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_manage_pelanggan(self):
        self.clear_content_frame()
        self.content_frame.pack(fill="both", expand=True)

        tk.Label(self.content_frame, text="Manage Pelanggan", font=("poppins", 14, "bold"),
                 bg="#6A9AB0", fg="white").pack(pady=10)

        form_frame = tk.Frame(self.content_frame, bg="#6A9AB0")
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Nama:", font=("poppins", 12),
                 bg="#6A9AB0", fg="white").pack(side="left", padx=5)
        self.entry_nama = tk.Entry(form_frame, font=("poppins", 12), width=25)
        self.entry_nama.pack(side="left", padx=5)

        tk.Label(form_frame, text="Kendaraan:", font=("poppins", 12),
                 bg="#6A9AB0", fg="white").pack(side="left", padx=5)
        self.entry_kendaraan = tk.Entry(form_frame, font=("poppins", 12), width=25)
        self.entry_kendaraan.pack(side="left", padx=5)

        tk.Label(form_frame, text="Servis:", font=("poppins", 12),
                 bg="#6A9AB0", fg="white").pack(side="left", padx=5)
        servis_frame = tk.Frame(form_frame, bg="#6A9AB0")
        servis_frame.pack(side="left", padx=5)
        self.servis_vars = {}
        for i, servis in enumerate(opsi_servis):
            var = tk.BooleanVar()
            tk.Checkbutton(servis_frame, text=servis, variable=var,
                           bg="#6A9AB0", fg="white", font=("poppins", 10),
                           selectcolor="#6A9AB0",
                           activebackground="#6A9AB0", activeforeground="white",
                           indicatoron=1).pack(anchor="w")
            self.servis_vars[servis] = var

        tk.Button(form_frame, text="Tambah", font=("poppins", 11, "bold"),
                  command=self.tambah_pelanggan).pack(side="left", padx=5)

        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.tree = ttk.Treeview(tree_frame, columns=("Id", "Nama", "Kendaraan", "Servis", "Tanggal"),
                                 show="headings", height=12)
        self.tree.heading("Id", text="Id")
        self.tree.heading("Nama", text="Nama")
        self.tree.heading("Kendaraan", text="Kendaraan")
        self.tree.heading("Servis", text="Servis")
        self.tree.heading("Tanggal", text="Tanggal")
        self.tree.column("Id", width=50)
        self.tree.column("Nama", width=150)
        self.tree.column("Kendaraan", width=150)
        self.tree.column("Servis", width=200)
        self.tree.column("Tanggal", width=100)

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        for data in antrian:
            self.tree.insert("", "end", values=(data[0], data[1], data[2], data[3], data[4]))

        btn_frame = tk.Frame(self.content_frame, bg="#6A9AB0")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Edit Pelanggan", font=("poppins", 11, "bold"),
                  bg="#f5cb41", fg="white", command=self.buka_form_edit_pelanggan).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Hapus Pelanggan", font=("poppins", 11, "bold"),
                  bg="#FC6655", fg="white", command=self.hapus_pelanggan).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Kembali", font=("poppins", 11, "bold"),
                  command=self.kembali_ke_menu_utama).pack(side="left", padx=10)

    def tambah_pelanggan(self):
        nama = self.entry_nama.get().strip()
        kendaraan = self.entry_kendaraan.get().strip()
        servis_terpilih = [s for s, var in self.servis_vars.items() if var.get()]

        if not nama or not kendaraan or not servis_terpilih:
            messagebox.showerror("Error", "Semua kolom harus diisi dan minimal satu servis dipilih!")
            return

        if not all(s in opsi_servis for s in servis_terpilih):
            messagebox.showerror("Error", "Salah satu servis tidak valid!")
            return

        jumlah_data = len(antrian) + 1
        id_user = f"RS-{jumlah_data:03d}"
        tanggal = datetime.now().strftime("%Y-%m-%d")
        status = "Belum Dibayar"
        servis_text = ", ".join(servis_terpilih)
        data = (id_user, nama, kendaraan, servis_text, tanggal, status)
        antrian.append(data)
        self.tree.insert("", "end", values=(data[0], data[1], data[2], data[3], data[4]))

        self.entry_nama.delete(0, tk.END)
        self.entry_kendaraan.delete(0, tk.END)
        for var in self.servis_vars.values():
            var.set(False)
        messagebox.showinfo("Berhasil", "Pelanggan berhasil ditambahkan!")

    def buka_form_edit_pelanggan(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diedit terlebih dahulu.")
            return
        item_data = self.tree.item(selected_item)["values"]
        if not item_data:
            messagebox.showerror("Error", "Gagal mendapatkan data.")
            return
        full_data = next((d for d in antrian if d[0] == item_data[0]), None)
        if not full_data:
            messagebox.showerror("Error", "Data tidak ditemukan.")
            return
        self.root.withdraw()
        FormEditPelanggan(self.root, self.content_frame, self.update_pelanggan, selected_item, full_data)

    def update_pelanggan(self, item_id, nama, kendaraan, servis, tanggal, status):
        index = self.tree.index(item_id)
        antrian[index] = (antrian[index][0], nama, kendaraan, servis, tanggal, status)
        self.tree.item(item_id, values=(antrian[index][0], nama, kendaraan, servis, tanggal))
        self.root.deiconify()

    def hapus_pelanggan(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Pilih Data", "Pilih pelanggan yang ingin dihapus.")
            return
        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")
        if konfirmasi:
            index = self.tree.index(selected_item[0])
            self.tree.delete(selected_item)
            antrian.pop(index)
            messagebox.showinfo("Berhasil", "Data pelanggan berhasil dihapus.")
        else:
            messagebox.showinfo("Dibatalkan", "Penghapusan data dibatalkan.")

    def show_manage_barang(self):
        self.clear_content_frame()
        self.content_frame.pack(fill="both", expand=True)

        tk.Label(self.content_frame, text="Tambah Barang Baru", font=("poppins", 14, "bold"),
                 bg="#6A9AB0", fg="white").pack(pady=10)
        form_frame = tk.Frame(self.content_frame, bg="#6A9AB0")
        form_frame.pack(pady=5)
        tk.Label(form_frame, text="Nama Barang:", font=("poppins", 12),
                 bg="#6A9AB0", fg="white").pack(side="left", padx=5)
        self.entry_barang = tk.Entry(form_frame, font=("poppins", 12), width=25)
        self.entry_barang.pack(side="left", padx=5)
        tk.Button(form_frame, text="Tambah", font=("poppins", 11, "bold"),
                  command=self.tambah_barang).pack(side="left", padx=5)
        self.stock_frame = tk.LabelFrame(self.content_frame, text="Manage Stok Barang",
                                        font=("poppins", 13, "bold"), bg="#FFFFFF", fg="black",
                                        padx=20, pady=10, labelanchor="n")
        self.stock_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.stock_labels = {}
        self.refresh_stok()

        tk.Button(self.content_frame, text="Kembali", font=("poppins", 11, "bold"),
                  command=self.kembali_ke_menu_utama).pack(pady=10)

    def tambah_barang(self):
        nama = self.entry_barang.get().strip().title()
        if not nama:
            messagebox.showwarning("Input Kosong", "Nama barang tidak boleh kosong.")
            return
        if nama in stocks:
            messagebox.showinfo("Sudah Ada", f"Barang '{nama}' sudah ditambahkan.")
            return
        stocks[nama] = 0
        self.entry_barang.delete(0, tk.END)
        self.refresh_stok()

    def refresh_stok(self):
        for widget in self.stock_frame.winfo_children():
            widget.destroy()
        for i, (item, qty) in enumerate(stocks.items()):
            lbl_item = tk.Label(self.stock_frame, text=item, font=("poppins", 12, "bold"),
                                bg="#6A9AB0", fg="white")
            lbl_item.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            qty_var = tk.StringVar(value=str(qty))
            lbl_qty = tk.Label(self.stock_frame, textvariable=qty_var, font=("poppins", 12),
                               bg="white", width=8)
            lbl_qty.grid(row=i, column=1, padx=10)
            btn_minus = tk.Button(self.stock_frame, text="-", font=("poppins", 12, "bold"), width=3,
                                  command=lambda item=item, var=qty_var: self.kurangi_stok(item, var))
            btn_minus.grid(row=i, column=2, padx=5)
            btn_plus = tk.Button(self.stock_frame, text="+", font=("poppins", 12, "bold"), width=3,
                                 command=lambda item=item, var=qty_var: self.tambah_stok(item, var))
            btn_plus.grid(row=i, column=3, padx=5)
            self.stock_labels[item] = qty_var

    def tambah_stok(self, item, var):
        stocks[item] += 1
        var.set(str(stocks[item]))

    def kurangi_stok(self, item, var):
        if stocks[item] > 0:
            stocks[item] -= 1
            var.set(str(stocks[item]))
        else:
            messagebox.showwarning("Stok Habis", f"Stok {item} sudah 0!")

    def show_manage_servis(self):
        self.clear_content_frame()
        self.content_frame.pack(fill="both", expand=True)

        tk.Label(self.content_frame, text="Manage Servis", font=("poppins", 14, "bold"),
                 bg="#6A9AB0", fg="white").pack(pady=10)

        form_frame = tk.Frame(self.content_frame, bg="#6A9AB0")
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Nama Servis:", font=("poppins", 12),
                 bg="#6A9AB0", fg="white").pack(side="left", padx=5)
        self.entry_servis_nama = tk.Entry(form_frame, font=("poppins", 12), width=25)
        self.entry_servis_nama.pack(side="left", padx=5)

        tk.Label(form_frame, text="Harga (Rp):", font=("poppins", 12),
                 bg="#6A9AB0", fg="white").pack(side="left", padx=5)
        self.entry_servis_harga = tk.Entry(form_frame, font=("poppins", 12), width=15)
        self.entry_servis_harga.pack(side="left", padx=5)

        tk.Button(form_frame, text="Tambah", font=("poppins", 11, "bold"),
                  command=self.tambah_servis).pack(side="left", padx=5)

        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.tree_servis = ttk.Treeview(tree_frame, columns=("Nama", "Harga"),
                                       show="headings", height=12)
        self.tree_servis.heading("Nama", text="Nama Servis")
        self.tree_servis.heading("Harga", text="Harga (Rp)")
        self.tree_servis.column("Nama", width=200)
        self.tree_servis.column("Harga", width=100)

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_servis.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree_servis.xview)
        self.tree_servis.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.tree_servis.pack(side="left", fill="both", expand=True)

        for nama, harga in layanan_servis.items():
            self.tree_servis.insert("", "end", values=(nama, f"{harga:,}"))

        tk.Button(self.content_frame, text="Kembali", font=("poppins", 11, "bold"),
                  command=self.kembali_ke_menu_utama).pack(pady=10)

    def tambah_servis(self):
        nama = self.entry_servis_nama.get().strip()
        try:
            harga = int(self.entry_servis_harga.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Harga harus berupa angka!")
            return

        if not nama or harga < 0:
            messagebox.showerror("Error", "Nama servis dan harga harus valid!")
            return

        if nama in layanan_servis:
            messagebox.showinfo("Sudah Ada", f"Servis '{nama}' sudah ada!")
            return

        layanan_servis[nama] = harga
        opsi_servis.append(nama)
        self.tree_servis.insert("", "end", values=(nama, f"{harga:,}"))
        self.entry_servis_nama.delete(0, tk.END)
        self.entry_servis_harga.delete(0, tk.END)
        messagebox.showinfo("Berhasil", f"Servis '{nama}' dengan harga Rp{harga:,} berhasil ditambahkan!")
        self.refresh_servis_options()

    def refresh_servis_options(self):
        if hasattr(self, 'servis_vars'):
            current_servis = [s for s, var in self.servis_vars.items() if var.get()]
            for widget in self.content_frame.winfo_children():
                if isinstance(widget, tk.Frame) and widget.winfo_children():
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Checkbutton):
                            child.destroy()
            self.servis_vars.clear()
            for i, servis in enumerate(opsi_servis):
                var = tk.BooleanVar()
                tk.Checkbutton(widget, text=servis, variable=var,
                               bg="#6A9AB0", fg="white", font=("poppins", 10),
                               selectcolor="#808080",
                               activebackground="#6A9AB0", activeforeground="white",
                               indicatoron=1).pack(anchor="w")
                self.servis_vars[servis] = var
            for s in current_servis:
                if s in self.servis_vars:
                    self.servis_vars[s].set(True)

    def show_laporan_transaksi(self):
        self.clear_content_frame()
        self.content_frame.pack(fill="both", expand=True)

        tk.Label(self.content_frame, text="Laporan Transaksi (Lunas)", font=("poppins", 14, "bold"),
                 bg="#6A9AB0", fg="white").pack(pady=10)

        filter_frame = tk.Frame(self.content_frame, bg="#6A9AB0")
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Filter Tanggal:", font=("poppins", 12),
                 bg="#6A9AB0", fg="white").pack(side="left", padx=5)
        self.entry_tanggal = tk.Entry(filter_frame, font=("poppins", 12), width=12)
        self.entry_tanggal.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_tanggal.pack(side="left", padx=5)
        tk.Button(filter_frame, text="Filter", font=("poppins", 11, "bold"),
                  command=self.filter_laporan).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Tampilkan Semua", font=("poppins", 11, "bold"),
                  command=self.tampilkan_semua_laporan).pack(side="left", padx=5)

        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.tree_laporan = ttk.Treeview(tree_frame, columns=("Id", "Nama", "Kendaraan", "Servis", "Tanggal", "Total"),
                                         show="headings", height=12)
        self.tree_laporan.heading("Id", text="Id")
        self.tree_laporan.heading("Nama", text="Nama")
        self.tree_laporan.heading("Kendaraan", text="Kendaraan")
        self.tree_laporan.heading("Servis", text="Servis")
        self.tree_laporan.heading("Tanggal", text="Tanggal")
        self.tree_laporan.heading("Total", text="Total (Rp)")
        self.tree_laporan.column("Id", width=50)
        self.tree_laporan.column("Nama", width=150)
        self.tree_laporan.column("Kendaraan", width=150)
        self.tree_laporan.column("Servis", width=200)
        self.tree_laporan.column("Tanggal", width=100)
        self.tree_laporan.column("Total", width=100)

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_laporan.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree_laporan.xview)
        self.tree_laporan.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.tree_laporan.pack(side="left", fill="both", expand=True)

        self.label_total = tk.Label(self.content_frame, text="Total Pendapatan: Rp 0", font=("poppins", 12, "bold"),
                                    bg="#6A9AB0", fg="white")
        self.label_total.pack(pady=10)

        tk.Button(self.content_frame, text="Kembali", font=("poppins", 11, "bold"),
                  command=self.kembali_ke_menu_utama).pack(pady=10)

        self.tampilkan_semua_laporan()

    def filter_laporan(self):
        try:
            tanggal_filter = datetime.strptime(self.entry_tanggal.get(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Format tanggal harus YYYY-MM-DD!")
            return

        self.tree_laporan.delete(*self.tree_laporan.get_children())
        total_pendapatan = 0
        for data in antrian:
            if data[5] == "Lunas":
                tanggal_data = datetime.strptime(data[4], "%Y-%m-%d").date()
                if tanggal_data == tanggal_filter:
                    servis_list = [s.strip() for s in data[3].split(",")]
                    total = sum(layanan_servis.get(s, 100000) for s in servis_list)
                    total_pendapatan += total
                    self.tree_laporan.insert("", "end", values=(data[0], data[1], data[2], data[3], data[4], f"{total:,}"))
        self.label_total.config(text=f"Total Pendapatan: Rp {total_pendapatan:,}")

    def tampilkan_semua_laporan(self):
        self.tree_laporan.delete(*self.tree_laporan.get_children())
        total_pendapatan = 0
        for data in antrian:
            if data[5] == "Lunas":
                servis_list = [s.strip() for s in data[3].split(",")]
                total = sum(layanan_servis.get(s, 100000) for s in servis_list)
                total_pendapatan += total
                self.tree_laporan.insert("", "end", values=(data[0], data[1], data[2], data[3], data[4], f"{total:,}"))
        self.label_total.config(text=f"Total Pendapatan: Rp {total_pendapatan:,}")

    def kembali_ke_menu_utama(self):
        self.clear_content_frame()
        self.content_frame.pack_forget()
        self.admin_main_menu.show()


class FormEditPelanggan:
    def __init__(self, master, parent_frame, callback_update, item_id, data):
        self.master = master
        self.callback_update = callback_update
        self.item_id = item_id
        self.root = tk.Toplevel(master)
        self.root.title("Edit Pelanggan")
        self.root.geometry("500x400")
        self.root.configure(bg="#6A9AB0")
        self.root.resizable(False, False)
        
        tk.Label(self.root, text="Edit Pelanggan", bg="#6A9AB0", fg="white",
                 font=("poppins", 20, "bold")).pack(pady=(20, 10))
        form_frame = tk.Frame(self.root, bg="#6A9AB0")
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Nama:", bg="#6A9AB0", fg="white",
                 font=("poppins", 11, "bold"), anchor="w").grid(row=0, column=0, sticky="w", padx=20, pady=5)
        self.entry_nama = tk.Entry(form_frame, font=("poppins", 12), width=30)
        self.entry_nama.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Kendaraan:", bg="#6A9AB0", fg="white",
                 font=("poppins", 11, "bold"), anchor="w").grid(row=1, column=0, sticky="w", padx=20, pady=5)
        self.entry_kendaraan = tk.Entry(form_frame, font=("poppins", 12), width=30)
        self.entry_kendaraan.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Servis:", bg="#6A9AB0", fg="white",
                 font=("poppins", 11, "bold"), anchor="w").grid(row=2, column=0, sticky="w", padx=20, pady=5)
        servis_frame = tk.Frame(form_frame, bg="#6A9AB0")
        servis_frame.grid(row=2, column=1, padx=10, pady=5)
        self.servis_vars = {}
        selected_services = [s.strip() for s in data[3].split(",")]
        for i, servis in enumerate(opsi_servis):
            var = tk.BooleanVar()
            tk.Checkbutton(servis_frame, text=servis, variable=var,
                           bg="#6A9AB0", fg="white", font=("poppins", 10),
                           selectcolor="#808080",  # Warna abu-abu untuk tanda centang
                           activebackground="#6A9AB0", activeforeground="white",
                           indicatoron=1).pack(anchor="w")
            self.servis_vars[servis] = var
            if servis in selected_services:
                var.set(True)
        
        tk.Label(form_frame, text="Tanggal (YYYY-MM-DD):", bg="#6A9AB0", fg="white",
                 font=("poppins", 11, "bold"), anchor="w").grid(row=3, column=0, sticky="w", padx=20, pady=5)
        self.entry_tanggal = tk.Entry(form_frame, font=("poppins", 12), width=30)
        self.entry_tanggal.grid(row=3, column=1, padx=10, pady=5)
        
        self.entry_nama.insert(0, data[1])
        self.entry_kendaraan.insert(0, data[2])
        self.entry_tanggal.insert(0, data[4])
        
        tombol_frame = tk.Frame(self.root, bg="#6A9AB0")
        tombol_frame.pack(pady=20)
        tk.Button(tombol_frame, text="Kembali", font=("poppins", 10, "bold"),
                  command=self.kembali, bg="white", fg="#3A6D8C", width=10).pack(side="left", padx=10)
        tk.Button(tombol_frame, text="Simpan", font=("poppins", 10, "bold"),
                  command=self.simpan_data, bg="white", fg="#3A6D8C", width=10).pack(side="left", padx=10)

    def simpan_data(self):
        nama = self.entry_nama.get().strip()
        kendaraan = self.entry_kendaraan.get().strip()
        servis_terpilih = [s for s, var in self.servis_vars.items() if var.get()]
        tanggal = self.entry_tanggal.get().strip()
        
        if not nama or not kendaraan or not servis_terpilih or not tanggal:
            messagebox.showerror("Error", "Semua kolom harus diisi dan minimal satu servis dipilih!")
            return
        if not all(s in opsi_servis for s in servis_terpilih):
            messagebox.showerror("Error", "Salah satu servis tidak valid! Pilih dari daftar servis.")
            return
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Format tanggal harus YYYY-MM-DD!")
            return
        
        servis_text = ", ".join(servis_terpilih)
        self.callback_update(self.item_id, nama, kendaraan, servis_text, tanggal, antrian[self.tree.index(self.item_id)][5])
        self.root.destroy()

    def kembali(self):
        self.root.destroy()
        self.master.deiconify()

class AplikasiLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        width, height = 400, 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg="#6A9AB0")
        self.percobaan = 0
        self.buat_login_form()

    def buat_login_form(self):
        tk.Label(self.root, text="Login", bg="#6A9AB0", fg="white",
                 font=("Poppins", 24, "bold")).pack(pady=(40, 30))
        form_frame = tk.Frame(self.root, bg="#6A9AB0")
        form_frame.pack()
        tk.Label(form_frame, text="Username", bg="#6A9AB0", fg="white",
                 font=("Poppins", 12, "bold"), anchor="w").pack(fill="x", padx=40, pady=(0, 5))
        self.entry_user = tk.Entry(form_frame, font=("Poppins", 12), width=30, relief="flat", bg="white", bd=0)
        self.entry_user.pack(ipady=12, padx=40, pady=(0, 20))
        tk.Label(form_frame, text="Password", bg="#6A9AB0", fg="white",
                 font=("Poppins", 12, "bold"), anchor="w").pack(fill="x", padx=40, pady=(0, 5))
        self.entry_pw = tk.Entry(form_frame, show="*", font=("Poppins", 12), width=30, relief="flat", bg="white", bd=0)
        self.entry_pw.pack(ipady=12, padx=40, pady=(0, 30))
        login_button = tk.Button(self.root, text="Login", font=("Poppins", 12, "bold"),
                                bg="#2C5777", fg="white", width=30, bd=0, command=self.check_login)
        login_button.pack(pady=10)

    def check_login(self):
        user = self.entry_user.get().strip()
        pw = self.entry_pw.get().strip()
        user_akun = {"username": "111", "password": "111"}
        admin_akun = {"username": "admin", "password": "admin"}
        if user == "" or pw == "":
            messagebox.showerror("Login Gagal", "Username atau password tidak boleh kosong!")
            return
        self.percobaan += 1
        sisa = 3 - self.percobaan
        if user == user_akun["username"] and pw == user_akun["password"]:
            self.percobaan = 0
            self.root.destroy()
            MainMenu()
        elif user == admin_akun["username"] and pw == admin_akun["password"]:
            self.percobaan = 0
            self.root.destroy()
            AdminMenu()
        else:
            if sisa == 0:
                messagebox.showerror("Gagal Login", "Login gagal 3 kali. Aplikasi akan ditutup.")
                self.root.destroy()
                exit()
            else:
                messagebox.showerror("Login Gagal", f"Username atau password salah.\nSisa percobaan: {sisa}")
                self.entry_pw.delete(0, tk.END)

class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bengkel Proper")
        self.root.geometry("800x500")
        self.root.configure(bg="#6A9AB0")
        self.buat_main_menu()
        self.root.mainloop()

    def buat_main_menu(self):
        tk.Label(self.root, text="Bengkel Proper", font=("Poppins", 18, "bold"), fg="#f5f5f5", bg="#6A9AB0", pady=20).pack()
        daftar_frame = tk.LabelFrame(self.root, text="Daftar Masalah", font=("Poppins", 12, "bold"), fg="#f5f5f5", bg="#6A9AB0", padx=10, pady=10)
        daftar_frame.pack()
        
        tree_frame = tk.Frame(daftar_frame)
        tree_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(tree_frame, columns=("Id", "Nama", "Kendaraan", "Servis", "Tanggal", "Status"), show="headings", height=10)
        for col in ("Id", "Nama", "Kendaraan", "Servis", "Tanggal", "Status"):
            self.tree.heading(col, text=col)
        self.tree.column("Id", width=50)
        self.tree.column("Nama", width=150)
        self.tree.column("Kendaraan", width=150)
        self.tree.column("Servis", width=200)
        self.tree.column("Tanggal", width=100)
        self.tree.column("Status", width=100)
        
        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        for data in antrian:
            self.tree.insert("", "end", values=data)

        button_frame = tk.Frame(self.root, bg="#6A9AB0")
        button_frame.pack(pady=30, padx=20)
        tk.Button(button_frame, text="Reservasi", font=("Poppins", 11, "bold"), width=15, bg="#f5f5f5", fg="#3A6D8C", command=self.buka_form_reservasi).pack(side="left", padx=10)
        tk.Button(button_frame, text="Edit", font=("Poppins", 11, "bold"), width=12, bg="#f5cb41", fg="#f5f5f5", command=self.buka_form_edit).pack(side="left", padx=10)
        tk.Button(button_frame, text="Hapus", font=("Poppins", 11, "bold"), width=15, bg="#f24822", fg="#f5f5f5", command=self.hapus_data).pack(side="left", padx=10)
        tk.Button(button_frame, text="Tagihan", font=("Poppins", 11, "bold"), width=15, bg="#6DEB89", fg="#f5f5f5", command=self.buka_form_bayar).pack(side="left", padx=10)
        tk.Button(button_frame, text="Logout", font=("Poppins", 11, "bold"), width=15, bg="#FF5555", fg="#f5f5f5", command=self.logout).pack(side="left", padx=10)

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        app = AplikasiLogin(root)
        root.mainloop()

    def buka_form_reservasi(self):
        self.root.withdraw()
        FormReservasi(self.root, self.show_main_menu, self.tambah_data)

    def tambah_data(self, nama, kendaraan, servis):
        jumlah_data = len(antrian) + 1
        id_user = f"RS-{jumlah_data:03d}"
        tanggal = datetime.now().strftime("%Y-%m-%d")
        status = "Belum Dibayar"
        data = (id_user, nama, kendaraan, servis, tanggal, status)
        antrian.append(data)
        self.tree.insert("", "end", values=data)

    def buka_form_edit(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diedit terlebih dahulu.")
            return
        item_data = self.tree.item(selected_item)["values"]
        if not item_data:
            messagebox.showerror("Error", "Gagal mendapatkan data.")
            return
        self.root.withdraw()
        FormEdit(self.root, self.show_main_menu, self.update_data, selected_item, item_data)

    def update_data(self, item_id, nama, kendaraan, servis):
        selected_item = self.tree.selection()[0]
        index = self.tree.index(selected_item)
        antrian[index] = (antrian[index][0], nama, kendaraan, servis, antrian[index][4], antrian[index][5])
        self.tree.item(item_id, values=(antrian[index][0], nama, kendaraan, servis, antrian[index][4], antrian[index][5]))

    def hapus_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus terlebih dahulu.")
            return
        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?\nData akan dihapus secara permanen.")
        if konfirmasi:
            index = self.tree.index(selected_item[0])
            self.tree.delete(selected_item)
            antrian.pop(index)
            messagebox.showinfo("Berhasil", "Data berhasil dihapus.")
        else:
            messagebox.showinfo("Dibatalkan", "Penghapusan data dibatalkan.")

    def buka_form_bayar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dibayar terlebih dahulu.")
            return
        item_data = self.tree.item(selected_item)["values"]
        if not item_data:
            messagebox.showerror("Error", "Gagal mendapatkan data.")
            return
        if item_data[5] == "Lunas":
            messagebox.showwarning("Peringatan", "Transaksi ini sudah lunas!")
            return
        self.root.withdraw()
        FormBeli(self.root, item_data, self.show_main_menu, self.update_status_lunas)

    def update_status_lunas(self, data):
        for i, item in enumerate(antrian):
            if item[0] == data[0]:
                antrian[i] = (item[0], item[1], item[2], item[3], item[4], "Lunas")
                break
        for item in self.tree.get_children():
            if self.tree.item(item)["values"][0] == data[0]:
                self.tree.item(item, values=(data[0], data[1], data[2], data[3], data[4], "Lunas"))
                break

    def show_main_menu(self):
        self.root.deiconify()

class FormReservasi:
    def __init__(self, master, callback_kembali, callback_simpan):
        self.master = master
        self.callback_kembali = callback_kembali
        self.callback_simpan = callback_simpan

        self.root = tk.Toplevel(master)
        self.root.title("Reservasi")
        self.root.geometry("500x400")
        self.root.configure(bg="#6A9AB0")
        self.root.resizable(False, False)

        tk.Label(self.root, text="Reservasi", bg="#6A9AB0", fg="white", font=("Poppins", 20, "bold")).pack(pady=(20, 10))

        form_frame = tk.Frame(self.root, bg="#6A9AB0")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nama:", bg="#6A9AB0", fg="white", font=("Poppins", 11, "bold"), anchor="w").grid(row=0, column=0, sticky="w", padx=20, pady=5)
        self.entry_nama = tk.Entry(form_frame, font=("Poppins", 12), width=30)
        self.entry_nama.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Kendaraan:", bg="#6A9AB0", fg="white", font=("Poppins", 11, "bold"), anchor="w").grid(row=1, column=0, sticky="w", padx=20, pady=5)
        self.entry_kendaraan = tk.Entry(form_frame, font=("Poppins", 12), width=30)
        self.entry_kendaraan.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Servis:", bg="#6A9AB0", fg="white", font=("Poppins", 11, "bold"), anchor="nw").grid(row=2, column=0, sticky="nw", padx=20, pady=5)

        self.servis_vars = {}
        servis_options = opsi_servis

        servis_frame = tk.Frame(form_frame, bg="#6A9AB0")
        servis_frame.grid(row=2, column=1, sticky="w", padx=10)

        for option in servis_options:
            var = tk.BooleanVar()
            tk.Checkbutton(servis_frame, text=option, variable=var, bg="#6A9AB0", fg="white", font=("Poppins", 10), anchor="w",
                           selectcolor="#6A9AB0",  # Warna abu-abu untuk tanda centang
                           activebackground="#6A9AB0", activeforeground="white", indicatoron=1).pack(anchor="w")
            self.servis_vars[option] = var

        tombol_frame = tk.Frame(self.root, bg="#6A9AB0")
        tombol_frame.pack(pady=20)

        tk.Button(tombol_frame, text="Kembali", font=("Poppins", 10, "bold"), command=self.kembali, bg="white", fg="#3A6D8C", width=10).pack(side="left", padx=10)
        tk.Button(tombol_frame, text="Reservasi", font=("Poppins", 10, "bold"), command=self.simpan_data, bg="white", fg="#3A6D8C", width=10).pack(side="left", padx=10)

    def kembali(self):
        self.root.destroy()
        self.callback_kembali()

    def simpan_data(self):
        nama = self.entry_nama.get().strip()
        kendaraan = self.entry_kendaraan.get().strip()
        servis_terpilih = [nama for nama, var in self.servis_vars.items() if var.get()]

        if not nama or not kendaraan or not servis_terpilih:
            messagebox.showerror("Error", "Semua kolom harus diisi dan minimal satu servis dipilih!")
            return

        servis_text = ", ".join(servis_terpilih)
        self.callback_simpan(nama, kendaraan, servis_text)
        self.root.destroy()
        self.callback_kembali()

class FormEdit:
    def __init__(self, master, callback_kembali, callback_update, item_id, data):
        self.master = master
        self.callback_kembali = callback_kembali
        self.callback_update = callback_update
        self.item_id = item_id

        self.root = tk.Toplevel(master)
        self.root.title("Edit Reservasi")
        self.root.geometry("500x400")
        self.root.configure(bg="#6A9AB0")
        self.root.resizable(False, False)

        tk.Label(self.root, text="Edit Reservasi", bg="#6A9AB0", fg="white", font=("Poppins", 20, "bold")).pack(pady=(20, 10))

        form_frame = tk.Frame(self.root, bg="#6A9AB0")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Nama:", bg="#6A9AB0", fg="white", font=("Poppins", 11, "bold"), anchor="w").grid(row=0, column=0, sticky="w", padx=20, pady=5)
        self.entry_nama = tk.Entry(form_frame, font=("Poppins", 12), width=30)
        self.entry_nama.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Kendaraan:", bg="#6A9AB0", fg="white", font=("Poppins", 11, "bold"), anchor="w").grid(row=1, column=0, sticky="w", padx=20, pady=5)
        self.entry_kendaraan = tk.Entry(form_frame, font=("Poppins", 12), width=30)
        self.entry_kendaraan.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Servis:", bg="#6A9AB0", fg="white", font=("Poppins", 11, "bold"), anchor="nw").grid(row=2, column=0, sticky="nw", padx=20, pady=5)

        self.servis_vars = {}
        servis_options = opsi_servis

        servis_frame = tk.Frame(form_frame, bg="#6A9AB0")
        servis_frame.grid(row=2, column=1, sticky="w", padx=10)

        for option in servis_options:
            var = tk.BooleanVar()
            tk.Checkbutton(servis_frame, text=option, variable=var, bg="#6A9AB0", fg="white", font=("Poppins", 10), anchor="w",
                           selectcolor="#808080",  # Warna abu-abu untuk tanda centang
                           activebackground="#6A9AB0", activeforeground="white", indicatoron=1).pack(anchor="w")
            self.servis_vars[option] = var

        self.entry_nama.insert(0, data[1])
        self.entry_kendaraan.insert(0, data[2])
        selected_services = [s.strip() for s in data[3].split(",")]
        for s in selected_services:
            if s in self.servis_vars:
                self.servis_vars[s].set(True)

        tombol_frame = tk.Frame(self.root, bg="#6A9AB0")
        tombol_frame.pack(pady=20)

        tk.Button(tombol_frame, text="Kembali", font=("Poppins", 10, "bold"), command=self.kembali, bg="white", fg="#3A6D8C", width=10).pack(side="left", padx=10)
        tk.Button(tombol_frame, text="Simpan", font=("Poppins", 10, "bold"), command=self.simpan_data, bg="white", fg="#3A6D8C", width=10).pack(side="left", padx=10)

    def simpan_data(self):
        nama = self.entry_nama.get().strip()
        kendaraan = self.entry_kendaraan.get().strip()
        servis_terpilih = [s for s, var in self.servis_vars.items() if var.get()]

        if not nama or not kendaraan or not servis_terpilih:
            messagebox.showerror("Error", "Semua kolom harus diisi dan minimal satu servis dipilih!")
            return

        servis_text = ", ".join(servis_terpilih)
        self.callback_update(self.item_id, nama, kendaraan, servis_text)
        self.root.destroy()
        self.callback_kembali()

    def kembali(self):
        self.root.destroy()
        self.callback_kembali()

class FormBeli:
    def __init__(self, master, data, callback_kembali, callback_update):
        self.master = master
        self.callback_kembali = callback_kembali
        self.callback_update = callback_update
        self.data = data

        self.root = tk.Toplevel(master)
        self.root.title("Invoice Servis")
        self.root.geometry("600x700")
        self.root.configure(bg="#6A9AB0")
        self.root.resizable(False, False)

        tk.Label(self.root, text="Invoice Servis", font=("Poppins", 20, "bold"), bg="#6A9AB0", fg="white").pack(pady=10)

        frame_layanan = tk.LabelFrame(self.root, text="Detail Layanan", font=("Poppins", 12, "bold"), bg="#6A9AB0", fg="white", bd=2, relief="groove")
        frame_layanan.place(x=20, y=60, width=560, height=120)

        columns = ("no", "nama", "kendaraan", "servis")
        tree_layanan = ttk.Treeview(frame_layanan, columns=columns, show="headings", height=1)
        tree_layanan.heading("no", text="No")
        tree_layanan.heading("nama", text="Nama")
        tree_layanan.heading("kendaraan", text="Kendaraan")
        tree_layanan.heading("servis", text="Servis")

        tree_layanan.column("no", width=40, anchor="center")
        tree_layanan.column("nama", width=100)
        tree_layanan.column("kendaraan", width=160)
        tree_layanan.column("servis", width=220)

        tree_layanan.pack(fill="both", padx=10, pady=5)
        tree_layanan.insert("", "end", values=(1, data[1], data[2], data[3]))

        frame_tagihan = tk.LabelFrame(self.root, text="Detail Tagihan", font=("Poppins", 12, "bold"), bg="#6A9AB0", fg="white", bd=2, relief="groove")
        frame_tagihan.place(x=20, y=200, width=560, height=200)

        columns_tagihan = ("nama", "harga")
        tree_tagihan = ttk.Treeview(frame_tagihan, columns=columns_tagihan, show="headings", height=5)
        tree_tagihan.heading("nama", text="Nama")
        tree_tagihan.heading("harga", text="Harga")

        tree_tagihan.column("nama", width=180)
        tree_tagihan.column("harga", width=350)
        tree_tagihan.pack(fill="both", padx=10, pady=5)

        self.total_tagihan = 0
        for servis in data[3].split(","):
            servis = servis.strip()
            harga = layanan_servis.get(servis, 100000)
            self.total_tagihan += harga
            tree_tagihan.insert("", "end", values=(data[1], f"{servis} - Rp. {harga:,.0f},00"))

        label_total = tk.Label(frame_tagihan, font=("Poppins", 11, "bold"), bg="#6A9AB0", fg="white", anchor="e")
        label_total.pack(fill="x", padx=10, pady=(0, 5))
        label_total.config(text=f"Total Tagihan: Rp. {self.total_tagihan:,.0f},00")

        frame_bayar = tk.LabelFrame(self.root, text="Bayar", font=("Poppins", 12, "bold"), bg="#6A9AB0", fg="white", bd=2, relief="groove")
        frame_bayar.place(x=20, y=410, width=300, height=70)

        self.entry_bayar = tk.Entry(frame_bayar, font=("Poppins", 10))
        self.entry_bayar.place(width=280, x=8)

        tombol_frame = tk.Frame(self.root, bg="#6A9AB0")
        tombol_frame.place(x=10, y=500, width=560, height=50)

        tk.Button(tombol_frame, text="Kembali", font=("Poppins", 10, "bold"), command=self.kembali, bg="white", fg="#3A6D8C", width=15).pack(side="left", padx=10)
        tk.Button(tombol_frame, text="Bayar", font=("Poppins", 10, "bold"), command=self.nota, bg="#6DEB89", fg="#f5f5f5", width=15).pack(side="left", padx=10)

    def kembali(self):
        self.root.destroy()
        self.callback_kembali()

    def nota(self):
        jumlah_bayar_str = self.entry_bayar.get()
        try:
            jumlah_bayar = int(jumlah_bayar_str)
        except ValueError:
            messagebox.showerror("Error", "Masukkan jumlah bayar yang valid (angka)")
            return

        if jumlah_bayar < self.total_tagihan:
            messagebox.showwarning("Uang Kurang", f"Jumlah bayar kurang dari total tagihan.\n"
                                                f"Tagihan: Rp. {self.total_tagihan:,.0f},00\n"
                                                f"Dibayar: Rp. {jumlah_bayar:,.0f},00")
            return

        kembalian = jumlah_bayar - self.total_tagihan
        self.root.destroy()
        FormNotaPembayaran(self.master, self.data, self.total_tagihan, jumlah_bayar, kembalian, self.kembali_setelah_bayar)

    def kembali_setelah_bayar(self, data):
        self.callback_update(data)
        self.callback_kembali()

class FormNotaPembayaran:
    def __init__(self, master, data, total_tagihan, bayar, kembalian, callback_kembali):
        self.master = master
        self.callback_kembali = callback_kembali
        self.data = data

        self.root = tk.Toplevel(master)
        self.root.title("Nota Pembayaran")
        self.root.geometry("500x500")
        self.root.configure(bg="#6A9AB0")
        self.root.resizable(False, False)

        tk.Label(self.root, text="Nota Pembayaran", font=("Poppins", 20, "bold"), bg="#6A9AB0", fg="white").pack(pady=15)

        frame_tagihan = tk.Label(self.root, font=("Poppins", 12, "bold"), bg="white", fg="white", bd=2, relief="groove")
        frame_tagihan.place(x=20, y=60, width=460, height=200)

        columns = ("nama_servis", "harga")
        tree = ttk.Treeview(frame_tagihan, columns=columns, show="headings", height=7)
        tree.heading("nama_servis", text="Layanan Servis")
        tree.heading("harga", text="Harga (Rp)")

        tree.column("nama_servis", width=300)
        tree.column("harga", width=140)
        tree.pack(fill="both", padx=10, pady=10)

        for servis in data[3].split(","):
            servis = servis.strip()
            harga = layanan_servis.get(servis, 100000)
            tree.insert("", "end", values=(servis, f"{harga:,.0f}"))

        label_total = tk.Label(self.root, text=f"Total Tagihan: Rp. {total_tagihan:,.0f}", font=("Poppins", 12, "bold"), bg="#6A9AB0", fg="white", anchor="w")
        label_total.place(x=20, y=280, width=460, height=30)

        label_bayar = tk.Label(self.root, text=f"Total Bayar: Rp. {bayar:,.0f}", font=("Poppins", 12, "bold"), bg="#6A9AB0", fg="white", anchor="w")
        label_bayar.place(x=20, y=320, width=460, height=30)

        if kembalian > 0:
            label_kembali = tk.Label(self.root, text=f"Kembalian: Rp. {kembalian:,.0f}", font=("Poppins", 12, "bold"), bg="#6A9AB0", fg="#5AF34B", anchor="w")
            label_kembali.place(x=20, y=360, width=460, height=30)

        btn_kembali = tk.Button(self.root, text="Kembali", font=("Poppins", 12, "bold"), bg="white", fg="#3A6D8C", command=self.kembali)
        btn_kembali.place(x=200, y=420, width=100, height=30)

    def kembali(self):
        self.root.destroy()
        self.callback_kembali(self.data)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiLogin(root)
    root.mainloop()