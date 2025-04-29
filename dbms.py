import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

conn = sqlite3.connect('railway_gui.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Trains (
        train_id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_name TEXT,
        source TEXT,
        destination TEXT,
        departure TEXT,
        arrival TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_id INTEGER,
        passenger_name TEXT,
        journey_date TEXT,
        seat_no TEXT,
        status TEXT,
        FOREIGN KEY(train_id) REFERENCES Trains(train_id)
    )
''')
conn.commit()


root = tk.Tk()
root.title("Railway Reservation System")
root.geometry("700x600")
def add_train():
    def save_train():
        data = (tname.get(), src.get(), dest.get(), dep.get(), arr.get())
        cursor.execute("INSERT INTO Trains (train_name, source, destination, departure, arrival) VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        messagebox.showinfo("Success", "Train Added")
        win.destroy()

    win = tk.Toplevel(root)
    win.title("Add Train")
    win.geometry("300x300")

    tk.Label(win, text="Train Name").pack()
    tname = tk.Entry(win)
    tname.pack()

    tk.Label(win, text="Source").pack()
    src = tk.Entry(win)
    src.pack()

    tk.Label(win, text="Destination").pack()
    dest = tk.Entry(win)
    dest.pack()

    tk.Label(win, text="Departure").pack()
    dep = tk.Entry(win)
    dep.pack()

    tk.Label(win, text="Arrival").pack()
    arr = tk.Entry(win)
    arr.pack()

    tk.Button(win, text="Add Train", command=save_train).pack(pady=10)

def view_trains():
    win = tk.Toplevel(root)
    win.title("View Trains")

    tree = ttk.Treeview(win, columns=("ID", "Name", "Source", "Dest", "Dep", "Arr"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill=tk.BOTH, expand=True)

    cursor.execute("SELECT * FROM Trains")
    for row in cursor.fetchall():
        tree.insert('', tk.END, values=row)


def book_ticket():
    def book():
        data = (int(train_id.get()), name.get(), date.get(), seat.get(), "Confirmed")
        cursor.execute("INSERT INTO Bookings (train_id, passenger_name, journey_date, seat_no, status) VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        messagebox.showinfo("Booked", "Ticket Booked Successfully")
        win.destroy()

    win = tk.Toplevel(root)
    win.title("Book Ticket")
    win.geometry("300x300")

    tk.Label(win, text="Train ID").pack()
    train_id = tk.Entry(win)
    train_id.pack()

    tk.Label(win, text="Passenger Name").pack()
    name = tk.Entry(win)
    name.pack()

    tk.Label(win, text="Journey Date (YYYY-MM-DD)").pack()
    date = tk.Entry(win)
    date.pack()

    tk.Label(win, text="Seat No").pack()
    seat = tk.Entry(win)
    seat.pack()

    tk.Button(win, text="Book", command=book).pack(pady=10)


def view_bookings():
    win = tk.Toplevel(root)
    win.title("View Bookings")

    tree = ttk.Treeview(win, columns=("ID", "Train", "Name", "Date", "Seat", "Status"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill=tk.BOTH, expand=True)

    cursor.execute('''
        SELECT B.booking_id, T.train_name, B.passenger_name, B.journey_date, B.seat_no, B.status
        FROM Bookings B JOIN Trains T ON B.train_id = T.train_id
    ''')
    for row in cursor.fetchall():
        tree.insert('', tk.END, values=row)


def cancel_ticket():
    def cancel():
        bid = int(booking_id.get())
        cursor.execute("UPDATE Bookings SET status = 'Cancelled' WHERE booking_id = ?", (bid,))
        conn.commit()
        messagebox.showinfo("Cancelled", "Booking Cancelled")
        win.destroy()

    win = tk.Toplevel(root)
    win.title("Cancel Ticket")
    win.geometry("250x100")

    tk.Label(win, text="Booking ID").pack()
    booking_id = tk.Entry(win)
    booking_id.pack()

    tk.Button(win, text="Cancel", command=cancel).pack(pady=5)


tk.Label(root, text="RAILWAY RESERVATION SYSTEM", font=("Arial", 20), pady=20).pack()

tk.Button(root, text="Add Train", width=25, command=add_train).pack(pady=10)
tk.Button(root, text="View Trains", width=25, command=view_trains).pack(pady=10)
tk.Button(root, text="Book Ticket", width=25, command=book_ticket).pack(pady=10)
tk.Button(root, text="View Bookings", width=25, command=view_bookings).pack(pady=10)
tk.Button(root, text="Cancel Ticket", width=25, command=cancel_ticket).pack(pady=10)
tk.Button(root, text="Exit", width=25, command=root.quit).pack(pady=10)

root.mainloop()
