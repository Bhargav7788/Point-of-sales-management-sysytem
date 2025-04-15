import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from order import setup_order_tab
from payment import setup_payment_tab


class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Point of Sales Management System")
        self.root.geometry("900x700")

        # Database Connection
        self.conn = sqlite3.connect("pos_system.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Notebook for Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.user_tab = ttk.Frame(self.notebook)
        self.product_tab = ttk.Frame(self.notebook)
        self.order_tab = ttk.Frame(self.notebook)
        self.payment_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.user_tab, text="Users")
        self.notebook.add(self.product_tab, text="Products")
        self.notebook.add(self.order_tab, text="Orders")
        self.notebook.add(self.payment_tab, text="Payments")

        # Tab Setup
        self.setup_user_tab()
        self.setup_product_tab()
        setup_order_tab(self)
        setup_payment_tab(self)

    def create_tables(self):
        """Create the required database tables if they don't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    """)
        self.conn.commit()

    def setup_user_tab(self):
        """Setup the User Management tab."""
        tk.Label(self.user_tab, text="User Management", font=("Arial", 16, "bold")).pack(pady=10)
        frame = tk.Frame(self.user_tab)
        frame.pack(pady=10)

        tk.Label(frame, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.user_name = tk.Entry(frame)
        self.user_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Role:").grid(row=1, column=0, padx=10, pady=5)
        self.user_role = ttk.Combobox(frame, values=["Admin", "Staff"])
        self.user_role.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Password:").grid(row=2, column=0, padx=10, pady=5)
        self.user_password = tk.Entry(frame, show="*")
        self.user_password.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(frame, text="Add User", command=self.add_user).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Delete User", command=self.delete_user).grid(row=3, column=1, pady=10)

        self.user_list = tk.Listbox(self.user_tab, width=50)
        self.user_list.pack(pady=10)
        self.load_users()

    def add_user(self):
        """Add a new user to the database."""
        name = self.user_name.get()
        role = self.user_role.get()
        password = self.user_password.get()

        if not name or not role or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        self.cursor.execute("INSERT INTO users (name, role, password) VALUES (?, ?, ?)", (name, role, password))
        self.conn.commit()
        self.load_users()

    def delete_user(self):
        """Delete the selected user."""
        selection = self.user_list.curselection()
        if not selection:
            messagebox.showerror("Error", "No user selected.")
            return

        user = self.user_list.get(selection[0])
        user_id = user.split(":")[0]  # Extract the ID
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        self.load_users()

    def load_users(self):
        """Load users into the Listbox."""
        self.user_list.delete(0, tk.END)
        self.cursor.execute("SELECT id, name, role FROM users")
        for user in self.cursor.fetchall():
            self.user_list.insert(tk.END, f"{user[0]}: {user[1]} ({user[2]})")

    def setup_product_tab(self):
        """Setup the Product Management tab."""
        tk.Label(self.product_tab, text="Product Management", font=("Arial", 16, "bold")).pack(pady=10)
        frame = tk.Frame(self.product_tab)
        frame.pack(pady=10)

        tk.Label(frame, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.product_name = tk.Entry(frame)
        self.product_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Price:").grid(row=1, column=0, padx=10, pady=5)
        self.product_price = tk.Entry(frame)
        self.product_price.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Stock:").grid(row=2, column=0, padx=10, pady=5)
        self.product_stock = tk.Entry(frame)
        self.product_stock.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(frame, text="Add Product", command=self.add_product).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Delete Product", command=self.delete_product).grid(row=3, column=1, pady=10)

        self.product_list = tk.Listbox(self.product_tab, width=50)
        self.product_list.pack(pady=10)
        self.load_products()

    def add_product(self):
        """Add a new product to the database."""
        name = self.product_name.get()
        try:
            price = float(self.product_price.get())
            stock = int(self.product_stock.get())
        except ValueError:
            messagebox.showerror("Error", "Price and Stock must be numbers.")
            return

        if not name or price < 0 or stock < 0:
            messagebox.showerror("Error", "All fields are required and must be valid.")
            return

        self.cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        self.conn.commit()
        self.load_products()

    def delete_product(self):
        """Delete the selected product."""
        selection = self.product_list.curselection()
        if not selection:
            messagebox.showerror("Error", "No product selected.")
            return

        product = self.product_list.get(selection[0])
        product_id = product.split(":")[0]  # Extract the ID
        self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.conn.commit()
        self.load_products()

    def load_products(self):
        """Load products into the Listbox."""
        self.product_list.delete(0, tk.END)
        self.cursor.execute("SELECT id, name, price, stock FROM products")
        for product in self.cursor.fetchall():
            self.product_list.insert(tk.END, f"{product[0]}: {product[1]} - ${product[2]:.2f} (Stock: {product[3]})")

    def add_order(self):
        """Add a new order to the temporary order list."""
        user = self.order_user.get()
        product = self.order_product.get()
        quantity = self.order_quantity.get()

        if not user or not product or not quantity:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return

        self.order_list.insert(tk.END, f"User: {user}, Product: {product}, Quantity: {quantity}")

    def place_order(self):
        """Place the order into the database."""
        for order in self.order_list.get(0, tk.END):
            try:
                user_id, product_id, quantity = self.parse_order(order)
                self.cursor.execute(
                    "INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)",
                    (user_id, product_id, quantity),
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to place order: {str(e)}")
                return

        self.conn.commit()
        messagebox.showinfo("Success", "Order placed successfully!")
        self.order_list.delete(0, tk.END)

    def parse_order(self, order):
        """Helper to parse an order string from the listbox."""
        user_info = order.split(",")[0].split(":")[1].strip()
        product_info = order.split(",")[1].split(":")[1].strip()
        quantity = order.split(",")[2].split(":")[1].strip()
        user_id = int(user_info.split(" ")[0])  # Extract the user ID
        product_id = int(product_info.split(" ")[0])  # Extract the product ID
        return user_id, product_id, int(quantity)
    
    def record_payment(self):
        """Record a payment."""
        try:
            order_id = int(self.payment_order.get())
            amount = float(self.payment_amount.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Order ID must be an integer and Amount must be a number.")
            return

        if not order_id or not amount:
            tk.messagebox.showerror("Error", "All fields are required.")
            return

        # Check if the order exists
        self.cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = self.cursor.fetchone()
        if not order:
            tk.messagebox.showerror("Error", "Order ID does not exist.")
            return

        # Record the payment
        self.cursor.execute("INSERT INTO payments (order_id, amount) VALUES (?, ?)", (order_id, amount))
        self.conn.commit()
        tk.messagebox.showinfo("Success", "Payment recorded successfully!")

        # Refresh the payments display
        self.refresh_payments()

    def refresh_payments(self):
        """Refresh the payment list display."""
        self.payment_list.delete(0, tk.END)
        self.cursor.execute("SELECT id, order_id, amount FROM payments")
        for payment in self.cursor.fetchall():
            self.payment_list.insert(tk.END, f"Payment ID: {payment[0]}, Order ID: {payment[1]}, Amount: ${payment[2]:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()