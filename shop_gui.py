import tkinter as tk
from tkinter import messagebox
import os
import json
import xlsxwriter
from datetime import datetime

class Shop:
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(__file__), 'shop_data.json')
        self.user_data_file = os.path.join(os.path.dirname(__file__), 'user_data.json')
        self.load_data()
        self.load_user_data()
        
        self.window = tk.Tk()
        self.window.title("Shop")

        self.login_frame = tk.Frame(self.window)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)

        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)

        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.show_registration)
        self.register_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.exit_button = tk.Button(self.login_frame, text="Exit", command=self.window.quit)
        self.exit_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.registration_frame = None
        self.shop_frame = None
        self.admin_frame = None

    def load_user_data(self):
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'r') as file:
                self.user_data = json.load(file)
        else:
            self.user_data = {}

    def save_user_data(self):
        with open(self.user_data_file, 'w') as file:
            json.dump(self.user_data, file)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "1234":
            self.login_frame.pack_forget()
            self.create_admin_ui()
        elif username in self.user_data and self.user_data[username] == password:
            self.login_frame.pack_forget()
            self.create_shop_ui()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")    

    def register(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        if username in self.user_data:
            messagebox.showerror("Registration Failed", "Username already exists")
        else:
            self.user_data[username] = password
            self.save_user_data()
            messagebox.showinfo("Registration Successful", "User registered successfully")
            self.registration_frame.pack_forget()
            self.login_frame.pack(fill=tk.BOTH, expand=True)

    def show_registration(self):
        if self.registration_frame:
            self.registration_frame.pack_forget()
        else:
            self.registration_frame = tk.Frame(self.window)
            self.registration_frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(self.registration_frame, text="New Username:").grid(row=0, column=0, padx=5, pady=5)
            self.register_username_entry = tk.Entry(self.registration_frame)
            self.register_username_entry.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(self.registration_frame, text="New Password:").grid(row=1, column=0, padx=5, pady=5)
            self.register_password_entry = tk.Entry(self.registration_frame, show="*")
            self.register_password_entry.grid(row=1, column=1, padx=5, pady=5)

            tk.Button(self.registration_frame, text="Register", command=self.register).grid(row=2, column=0, columnspan=2, pady=10)
            tk.Button(self.registration_frame, text="Back to Login", command=self.show_login).grid(row=3, column=0, columnspan=2, pady=10)

    def show_login(self):
        self.registration_frame.pack_forget()
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def create_shop_ui(self):
        self.shop_frame = tk.Frame(self.window)
        self.shop_frame.pack(fill=tk.BOTH, expand=True)

        self.inventory_frame = tk.Frame(self.shop_frame)
        self.inventory_frame.pack(fill=tk.X, padx=10, pady=10)

        self.cart_frame = tk.Frame(self.shop_frame)
        self.cart_frame.pack(fill=tk.X, padx=10, pady=10)

        self.checkout_frame = tk.Frame(self.shop_frame)
        self.checkout_frame.pack(fill=tk.X, padx=10, pady=10)

        self.import_frame = tk.Frame(self.shop_frame)
        self.import_frame.pack(fill=tk.X, padx=10, pady=10)

        self.cart_management_frame = tk.Frame(self.shop_frame)
        self.cart_management_frame.pack(fill=tk.X, padx=10, pady=10)

        self.import_label = tk.Label(self.import_frame, text="Import item (format: item,price,stock):")
        self.import_label.grid(row=0, column=0, padx=5, pady=5)

        self.import_entry = tk.Entry(self.import_frame, width=40)
        self.import_entry.grid(row=0, column=1, padx=5, pady=5)

        self.import_button = tk.Button(self.import_frame, text="Import", command=self.import_item)
        self.import_button.grid(row=0, column=2, padx=5, pady=5)

        self.remove_label = tk.Label(self.import_frame, text="Remove item (name only):")
        self.remove_label.grid(row=1, column=0, padx=5, pady=5)

        self.remove_entry = tk.Entry(self.import_frame, width=40)
        self.remove_entry.grid(row=1, column=1, padx=5, pady=5)

        self.remove_button = tk.Button(self.import_frame, text="Remove", command=self.remove_item)
        self.remove_button.grid(row=1, column=2, padx=5, pady=5)

        self.inventory_frame_header = tk.Label(self.inventory_frame, text="Inventory", font=("Arial", 14, "bold"))
        self.inventory_frame_header.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        self.cart_label = tk.Label(self.cart_frame, text="Cart:", font=("Arial", 12, "bold"))
        self.cart_label.grid(row=0, column=0, padx=5, pady=5)

        self.cart_text = tk.Text(self.cart_frame, height=10, width=50)
        self.cart_text.grid(row=1, column=0, padx=5, pady=5, rowspan=2)
        
        self.checkout_button = tk.Button(self.checkout_frame, text="Checkout", command=self.checkout)
        self.checkout_button.grid(row=0, column=0, padx=5, pady=5)

        self.print_receipt_button = tk.Button(self.checkout_frame, text="Print Receipt", command=self.print_receipt)
        self.print_receipt_button.grid(row=0, column=1, padx=5, pady=5)

        self.logout_button = tk.Button(self.checkout_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=1, column=0, padx=5, pady=5)

        self.exit_button = tk.Button(self.checkout_frame, text="Exit", command=self.window.quit)
        self.exit_button.grid(row=1, column=1, padx=5, pady=5)

        self.load_inventory()
        self.update_cart_text()

    def create_admin_ui(self):
        self.admin_frame = tk.Frame(self.window)
        self.admin_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.admin_frame, text="Admin Panel", font=("Arial", 16, "bold")).pack(pady=10)

        self.user_management_frame = tk.Frame(self.admin_frame)
        self.user_management_frame.pack(fill=tk.BOTH, expand=True)

        self.user_listbox = tk.Listbox(self.user_management_frame, height=10)
        self.user_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.user_listbox_scrollbar = tk.Scrollbar(self.user_management_frame, orient=tk.VERTICAL, command=self.user_listbox.yview)
        self.user_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.user_listbox.config(yscrollcommand=self.user_listbox_scrollbar.set)

        self.update_user_listbox()

        self.export_button = tk.Button(self.admin_frame, text="Export Data", command=self.export_data)
        self.export_button.pack(pady=10)

        self.logout_button = tk.Button(self.admin_frame, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

    def import_item(self):
        item_data = self.import_entry.get()
        if item_data:
            item_details = item_data.split(',')
            if len(item_details) == 3:
                item_name, item_price, item_stock = item_details
                try:
                    item_price = float(item_price)
                    item_stock = int(item_stock)
                except ValueError:
                    messagebox.showerror("Import Error", "Invalid price or stock value")
                    return

                self.inventory[item_name] = {'price': item_price, 'stock': item_stock}
                self.save_data()
                self.load_inventory()
            else:
                messagebox.showerror("Import Error", "Invalid format. Use: item,price,stock")
        else:
            messagebox.showerror("Import Error", "Input field is empty")

    def remove_item(self):
        item_name = self.remove_entry.get()
        if item_name:
            if item_name in self.inventory:
                del self.inventory[item_name]
                self.save_data()
                self.load_inventory()
                messagebox.showinfo("Remove Successful", f"Item '{item_name}' removed from inventory.")
            else:
                messagebox.showerror("Item Not Found", f"Item '{item_name}' not found in the inventory.")
        else:
            messagebox.showerror("Remove Error", "Input field is empty")

    def add_to_cart(self, item):
        if self.inventory[item]['stock'] > 0:
            self.inventory[item]['stock'] -= 1
            if item in self.cart:
                self.cart[item] += 1
            else:
                self.cart[item] = 1
            self.save_data()
            self.load_inventory()
            self.update_cart_text()
        else:
            messagebox.showinfo("Out of Stock", f"{item} is out of stock.")

    def remove_from_cart(self, item):
        if item in self.cart and self.cart[item] > 0:
            self.cart[item] -= 1
            self.inventory[item]['stock'] += 1
            if self.cart[item] == 0:
                del self.cart[item]
            self.save_data()
            self.load_inventory()
            self.update_cart_text()

    def load_inventory(self):
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()

        for idx, (item, details) in enumerate(self.inventory.items(), start=1):
            price = details.get('price', 'N/A')
            stock = details.get('stock', 'N/A')
        
            item_label = tk.Label(self.inventory_frame, text=f"{item} - Price: ${price} - Stock: {stock}")
            item_label.grid(row=idx, column=0, padx=5, pady=5)

            add_button = tk.Button(self.inventory_frame, text="Add to Cart", command=lambda i=item: self.add_to_cart(i))
            add_button.grid(row=idx, column=1, padx=5, pady=5)

            remove_button = tk.Button(self.inventory_frame, text="Remove from Cart", command=lambda i=item: self.remove_from_cart(i))
            remove_button.grid(row=idx, column=2, padx=5, pady=5)

    def update_cart_text(self):
        self.cart_text.delete(1.0, tk.END)
        for item, quantity in self.cart.items():
            self.cart_text.insert(tk.END, f"{item} - Quantity: {quantity}\n")

    def checkout(self):
        total_cost = sum(self.inventory[item]['price'] * quantity for item, quantity in self.cart.items())
        if self.cart:
            receipt_text = "\n".join([f"{item} - Quantity: {quantity} - Cost: ${self.inventory[item]['price'] * quantity}" for item, quantity in self.cart.items()])
            receipt_text += f"\n\nTotal Cost: ${total_cost:.2f}"
            messagebox.showinfo("Checkout", receipt_text)
            self.cart = {}
            self.update_cart_text()
        else:
            messagebox.showinfo("Checkout", "Your cart is empty.")

    def print_receipt(self):
        total_cost = sum(self.inventory[item]['price'] * quantity for item, quantity in self.cart.items())
    
        if self.cart:
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(os.path.dirname(__file__), f'data_{current_time}.xlsx')

            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet()

            worksheet.write('A1', 'Item')
            worksheet.write('B1', 'Quantity')
            worksheet.write('C1', 'Price per Item')
            worksheet.write('D1', 'Total Cost')

            row = 1
            for item, quantity in self.cart.items():
                worksheet.write(row, 0, item)
                worksheet.write(row, 1, quantity)
                worksheet.write(row, 2, self.inventory[item]['price'])
                worksheet.write(row, 3, self.inventory[item]['price'] * quantity)
                row += 1

            worksheet.write(row, 2, 'Total Cost')
            worksheet.write(row, 3, total_cost)
            workbook.close()

            messagebox.showinfo("Receipt", f"Receipt has been printed to '{file_path}'.")
        else:
            messagebox.showinfo("Receipt", "Your cart is empty.")

    def logout(self):
        if self.shop_frame:
            self.shop_frame.pack_forget()
            self.shop_frame = None
        if self.admin_frame:
            self.admin_frame.pack_forget()
            self.admin_frame = None
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.inventory, file)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.inventory = json.load(file)
        else:
            self.inventory = {}
        self.cart = {}

    def update_user_listbox(self):
        self.user_listbox.delete(0, tk.END)
        for username in self.user_data:
            self.user_listbox.insert(tk.END, username)

    def export_data(self):
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(os.path.dirname(__file__), f'data_{current_time}.xlsx')

        workbook = xlsxwriter.Workbook(file_path)

        user_worksheet = workbook.add_worksheet("User Data")
        user_worksheet.write('A1', 'Username')
        user_worksheet.write('B1', 'Password')

        for idx, (username, password) in enumerate(self.user_data.items(), start=1):
            user_worksheet.write(idx, 0, username)
            user_worksheet.write(idx, 1, password)

        orders_worksheet = workbook.add_worksheet("Orders Data")
        orders_worksheet.write('A1', 'Item')
        orders_worksheet.write('B1', 'Quantity')
        orders_worksheet.write('C1', 'Price per Item')
        orders_worksheet.write('D1', 'Total Cost')

        row = 1
        for item, quantity in self.cart.items():
            orders_worksheet.write(row, 0, item)
            orders_worksheet.write(row, 1, quantity)
            orders_worksheet.write(row, 2, self.inventory[item]['price'])
            orders_worksheet.write(row, 3, self.inventory[item]['price'] * quantity)
            row += 1

        orders_worksheet.write(row, 2, 'Total Cost')
        orders_worksheet.write(row, 3, sum(self.inventory[item]['price'] * quantity for item, quantity in self.cart.items()))

        workbook.close()
        messagebox.showinfo("Export Successful", f"Data exported to '{file_path}'.")

if __name__ == "__main__":
    app = Shop()
    app.window.mainloop()