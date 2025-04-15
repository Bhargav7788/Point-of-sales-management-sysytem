import tkinter as tk
from tkinter import ttk

def setup_payment_tab(app):
    """Setup the Payments tab."""
    tk.Label(app.payment_tab, text="Payment Management", font=("Arial", 16, "bold")).pack(pady=10)

    # Input frame
    frame = tk.Frame(app.payment_tab)
    frame.pack(pady=10)

    tk.Label(frame, text="Order ID:").grid(row=0, column=0, padx=10, pady=5)
    app.payment_order = tk.Entry(frame)
    app.payment_order.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Amount:").grid(row=1, column=0, padx=10, pady=5)
    app.payment_amount = tk.Entry(frame)
    app.payment_amount.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(frame, text="Record Payment", command=app.record_payment).grid(row=2, column=0, columnspan=2, pady=10)

    # Payments list display
    app.payment_list = tk.Listbox(app.payment_tab, width=60)
    app.payment_list.pack(pady=10)