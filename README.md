# Super Cashier



## Background Problems
A supermarket owner is expanding the business by creating a self-service cashier system so that customers can add item's name, quantity, and price themselves to the system.

## Objectives
Create a program to do _Create, Read, Update, and Delete_(CRUD)
* Create: customers will be able to input item details manually, and the system will process the transaction and give the total price.
* Read: customers will be able to check if their order has been correctly inputted and will be presented a table containing their order. Customers also will be able to see the total price, and whether they get a discount on their purchase.
* Update: customers will be able to edit the details of the items that have been inputted to the system. System will automatically process the update and adjust the total price.
* Delete: customers will be able to delete items in the order basket one at a time or reset the whole order.

## Program Flow
* At the self-service cashier, customers will make a new transaction and the system will process the `transaction()` function.
* Customers can add one type of item at a time to the basket, by inputting the item name, quantity, and the price with `add_item()`. Customers will get a message to show that the item has been added: **"Item {nama_item} berhasil ditambahkan."**.
* Customers can edit the item details one by one (item name with `update_item_name()` , quantity with `update_item_qty()`, or price with `update_item_price()`) by inputting the item name and the new detail to be added, whether it's the new item name with , new item quantity, or new item price.
    * Customers will get a message to show that the item detail has been modified: **"Nama/Jumlah/Harga Item {nama_item} berhasil diubah."**
    * If the input was incorrect, there will be a message to show that the item was not found **"Item {nama_item} tidak ditemukan."**
* Customers can delete the items one by one by using `delete_item()` or reset the whole transaction with `reset_transaction()`.
    * By deleting one item, customers will get a message to show that the item has been deleted: **"Item {nama_item} berhasil dihapus."**
        * If the input was incorrect, there will be a message to show that the item was not found **"Item {nama_item} tidak ditemukan."**
    * By resetting the transaction, customers will get a message to shows that all the items have been deleted from the order: **"Semua item berhasil dihapus!"**
* When the customers have finished inputting the item details but are still unsure whether there was a mistake, customers can do `check_order()`.
    * If there was a wrong input, the system will print **"Terdapat kesalahan input data"**
    * If all the items have been correctly inputted, the system will print **"Pemesanan sudah benar"** and a table showing the order details, Item Number, Item Name, Item Quantity, Price per Item, and Total Price per Item Type.
* After the order got checked, customers can do a check out with `check_out()` to get the total price for all the items.
    * If the total price is above IDR 200.000, the customers will get a 5% discount.
    * If the total price is above IDR 300.000, the customers will get a 6% discount.
    * If the total price is above IDR 500.000, the customers will get a 7% discount.
* For each `check_out()` ran by the customers, transaction data consisting of transaction details will be inserted to sqlite to the transaction table using `insert_to_table()`  

## Module Syntax and Explanation

```
from tabulate import tabulate
from sqlalchemy import create_engine
from sqlalchemy import text
# Make sure to download everything before importing.
```
Importing tabulate to create table for check_order function and sqlalchemy to put the transaction details to the database.

```
class transaction:
    def __init__(self):
        self.items = {}
```

Creating a new class named transaction and use init to initialize the attributes of the class.

```def add_item(self, nama_item, qty_item, harga_item):
        self.items[nama_item] = [qty_item, harga_item]
        print(f"Item {nama_item} berhasil ditambahkan.")
        print(f"Item yang dibeli adalah{self.items}")
```
Adding a new item by inputting item name, quantity, and the price.
```def update_item_name(self, nama_item, nama_item_baru):
        if nama_item in self.items:
            self.items[nama_item_baru] = self.items.get(nama_item)
            self.items.pop(nama_item)
            print(f"Nama item {nama_item} berhasil diubah")
        else:
            print(f"Item {nama_item} tidak ditemukan.")
```
Updating item name by inputting item name and the new item name.
```def update_item_qty(self, nama_item, qty_item_baru):
        if nama_item in self.items:
            self.items[nama_item][0] = qty_item_baru
            print(f"Jumlah item {nama_item} berhasil diubah.")
        else:
            print(f"Item {nama_item} tidak ditemukan.")
```
Updating item quantity by inputting item name and the new item quantity.
```def update_item_price(self, nama_item, harga_item_baru):
        if nama_item in self.items:
            self.items[nama_item][1] = harga_item_baru
            print(f"Harga item {nama_item} berhasil diubah.")
        else:
            print(f"Item {nama_item} tidak ditemukan.")
```
Updating item price by inputting item name and the new item price.
```def delete_item(self, nama_item):
        if nama_item in self.items:
            self.items.pop(nama_item)
            print(f"Item {nama_item} telah dihapus.")
            print(self.items)
        else:
            print(f"Item {nama_item} tidak ditemukan.")
```
Deleting one item by inputting the item name.
```def reset_transaction(self):
        self.items.clear()
        print("Semua item berhasil dihapus!")
```
Resetting transaction and clearing the order list.
```def check_order(self):
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
```
Checking order if there was any incorrect input.
```def check_out(self):
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
```
Doing a check out and printing the order details and the total price for the customers.
```def insert_to_table(self, items_for_upload):
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
```
Creating a database table if it doesn't exist yet and inserting the values to the table.


## Trying Test Case
![image.png](attachment:image.png)
Importing module
![image-2.png](attachment:image-2.png)
Inserting the function to a variable
![image-11.png](attachment:image-11.png)
Adding items
![image-5.png](attachment:image-5.png)
Updating item name
![image-6.png](attachment:image-6.png)
Updating item quantity
![image-7.png](attachment:image-7.png)
Failed updating item quantity as the item name was incorrect
![image-8.png](attachment:image-8.png)
Updating item price
![image-9.png](attachment:image-9.png)
Deleting one item
![image-10.png](attachment:image-10.png)
Resetting transaction
![image-14.png](attachment:image-14.png)
Adding new items
![image-15.png](attachment:image-15.png)
Checking order, incorrect input
![image-17.png](attachment:image-17.png)
Updating incorrect input: Panci Air quantity
![image-19.png](attachment:image-19.png)
Checking order successfully
![image-20.png](attachment:image-20.png)
Checking out

## Conclusion
This module works but need to be upgraded at some points. If i had more time, i would make more annotations so that this would be easier to understand.
