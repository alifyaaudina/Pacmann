#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tabulate import tabulate
from sqlalchemy import create_engine
from sqlalchemy import text


class transaction:
    def __init__(self):
        self.items = {}

    def add_item(self, nama_item, qty_item, harga_item):
        self.items[nama_item] = [qty_item, harga_item]
        print(f"Item {nama_item} berhasil ditambahkan.")

    def update_item_name(self, nama_item, nama_item_baru):
        if nama_item in self.items:
            self.items[nama_item_baru] = self.items.get(nama_item)
            self.items.pop(nama_item)
            print(f"Nama item {nama_item} berhasil diubah")
        else:
            print(f"Item {nama_item} tidak ditemukan.")

    def update_item_qty(self, nama_item, qty_item_baru):
        if nama_item in self.items:
            self.items[nama_item][0] = qty_item_baru
            print(f"Jumlah item {nama_item} berhasil diubah.")
        else:
            print(f"Item {nama_item} tidak ditemukan.")
             
    def update_item_price(self, nama_item, harga_item_baru):
        if nama_item in self.items:
            self.items[nama_item][1] = harga_item_baru
            print(f"Harga item {nama_item} berhasil diubah.")
        else:
            print(f"Item {nama_item} tidak ditemukan.")
            
    def delete_item(self, nama_item):
        if nama_item in self.items:
            self.items.pop(nama_item)
            print(f"Item {nama_item} telah dihapus.")
        else:
            print(f"Item {nama_item} tidak ditemukan.")

    def reset_transaction(self):
        self.items.clear()
        print("Semua item berhasil dihapus!")

    def check_order(self):
        errors = 0
        table = []
        for item in self.items.values():
            try:
                assert isinstance(item[0], int)
                assert isinstance(item[1], int)
            except AssertionError:
                errors += 1
        if errors > 0:
            print("Terdapat kesalahan input data.")
        else:
            print("Pemesanan sudah benar.")
    
            for i, (nama_item, qty_harga) in enumerate(self.items.items(), start=1):
                qty_item, harga_item = qty_harga
                total_harga = qty_item * harga_item
                table.append([i, nama_item, qty_item, harga_item, total_harga])
            print(tabulate(table, headers=['No', 'Nama Item', 'Jumlah Item', 'Harga/Item', 'Total Harga'], tablefmt='fancy_grid'))
            return self.items

    def check_out(self):
        diskon = 0
        total_belanja = 0
        items_for_upload = []
        for nama_item, qty_harga in self.items.items():
            qty_item, harga_item = qty_harga
            total_harga = qty_item * harga_item
            total_belanja += total_harga
            if total_harga > 500000:
                diskon = 7
            elif total_harga > 300000:
                diskon = 6
            elif total_harga > 200000:
                diskon = 5

            if diskon > 0:
                harga_diskon = total_harga - total_harga * diskon / 100
            else:
                harga_diskon = total_harga
                
            items_for_upload.append({
            'nama_item': nama_item,
            'jumlah_item': qty_item,
            'harga': harga_item,
            'total_harga': total_harga,
            'diskon': diskon,
            'harga_diskon': harga_diskon
            })

            
            
        print(f"Item yang dibeli adalah: {self.items}. Total belanja adalah: {total_belanja}")
        self.insert_to_table(items_for_upload)
        
    def insert_to_table(self, items_for_upload):
        # Membuat engine
        # Konfigurasi koneksi ke database sqlite
        engine = create_engine('sqlite:///example.db')

        # Buat koneksi
        conn = engine.connect()

        # Buat Query SQL dalam modul text
        query = text("""
        CREATE TABLE IF NOT EXISTS transactions(
            no_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_item TEXT,
            jumlah_item INT,
            harga INT,
            total_harga INT,
            diskon INT,
            harga_diskon INT
        )
        """)

        # Mengeksekusi Query
        conn.execute(query)

        # Loop through the items and insert them into the transactions table
        for item in items_for_upload:
            query = text("""
                INSERT INTO transactions (nama_item, jumlah_item, harga, total_harga, diskon, harga_diskon)
                VALUES (:nama_item, :jumlah_item, :harga, :total_harga, :diskon, :harga_diskon)
            """)

            conn.execute(query,
                         nama_item=item['nama_item'],
                         jumlah_item=item['jumlah_item'],
                         harga=item['harga'],
                         total_harga=item['total_harga'],
                         diskon=item['diskon'],
                         harga_diskon=item['harga_diskon'])

        # Menutup koneksi ke database
        conn.close()


    

