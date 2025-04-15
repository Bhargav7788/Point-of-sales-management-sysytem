import tkinter as tk
from tkinter import ttk, messagebox

def setup_order_tab(app):
    """Setup the Order Management tab."""
    tk.Label(app.order_tab, text="Order Management", font=("Arial", 16, "bold")).pack(pady=10)

    # Input frame
    frame = tk.Frame(app.order_tab)
    frame.pack(pady=10)

    # User dropdown
    tk.Label(frame, text="User:").grid(row=0, column=0, padx=10, pady=5)
    app.order_user = ttk.Combobox(frame, state="readonly")
    app.order_user.grid(row=0, column=1, padx=10, pady=5)

    # Product dropdown
    tk.Label(frame, text="Product:").grid(row=1, column=0, padx=10, pady=5)
    app.order_product = ttk.Combobox(frame, state="readonly")
    app.order_product.grid(row=1, column=1, padx=10, pady=5)

    # Quantity entry
    tk.Label(frame, text="Quantity:").grid(row=2, column=0, padx=10, pady=5)
    app.order_quantity = tk.Entry(frame)
    app.order_quantity.grid(row=2, column=1, padx=10, pady=5)

    # Buttons
    tk.Button(frame, text="Add to Order", command=lambda: add_order(app)).grid(row=3, column=0, pady=10)
    tk.Button(frame, text="Place Order", command=lambda: place_order(app)).grid(row=3, column=1, pady=10)

    # Order list
    app.order_list = tk.Listbox(app.order_tab, width=60)
    app.order_list.pack(pady=10)

    # Load users and products
    load_users_for_orders(app)
    load_products_for_orders(app)

def load_users_for_orders(app):
    """Load users into the order dropdown."""
    app.order_user['values'] = [
        f"{user[0]}: {user[1]}" for user in app.cursor.execute("SELECT id, name FROM users").fetchall()
    ]

def load_products_for_orders(app):
    """Load products into the order dropdown."""
    app.order_product['values'] = [
        f"{product[0]}: {product[1]}" for product in app.cursor.execute("SELECT id, name FROM products").fetchall()
    ]

def add_order(app):
    """Add an order to the list."""
    try:
        user_id = int(app.order_user.get().split(":")[0])  # Extract user ID
        product_id = int(app.order_product.get().split(":")[0])  # Extract product ID
        quantity = int(app.order_quantity.get())
    except ValueError:
        messagebox.showerror("Error", "Please select valid User, Product, and Quantity.")
        return

    app.order_list.insert(tk.END, f"User: {user_id}, Product: {product_id}, Quantity: {quantity}")

def place_order(app):
    """Place the order and save it to the database."""
    try:
        for order in app.order_list.get(0, tk.END):
            user_id, product_id, quantity = [
                int(value.split(":")[1]) for value in order.split(", ")
            ]
            app.cursor.execute(
                "INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)",
                (user_id, product_id, quantity),
            )
        app.conn.commit()
        messagebox.showinfo("Success", "Order(s) placed successfully!")
        app.order_list.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to place order: {e}")