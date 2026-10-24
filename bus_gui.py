import tkinter as tk
from tkinter import ttk, messagebox

# ==================== DATA ====================

bookings = []
next_booking_id = 101

routes = [
    {"id": 1, "from": "Karachi", "to": "Hyderabad",
     "fare": 800, "seats": 40, "departure": "08:00 AM"},
    {"id": 2, "from": "Karachi", "to": "Lahore",
     "fare": 3500, "seats": 40, "departure": "10:00 AM"},
    {"id": 3, "from": "Lahore", "to": "Islamabad",
     "fare": 1200, "seats": 35, "departure": "09:00 AM"},
    {"id": 4, "from": "Lahore", "to": "Rawalpindi",
     "fare": 1200, "seats": 35, "departure": "11:30 AM"},
    {"id": 5, "from": "Islamabad", "to": "Multan",
     "fare": 1200, "seats": 35, "departure": "09:00 AM"}
]

# ==================== COLORS ====================

NAVY = "#142D4E"
BLUE = "#2563EB"
BG = "#F3F6FB"
WHITE = "#FFFFFF"
TEXT = "#1E293B"
MUTED = "#64748B"
GREEN = "#15803D"
RED = "#DC2626"
PURPLE = "#6D5AE6"
BORDER = "#E2E8F0"

# ==================== MAIN WINDOW ====================

root = tk.Tk()
root.title("Smart Bus | Reservation Management")
root.geometry("1100x750")
root.minsize(950, 680)
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    font=("Segoe UI", 10),
    rowheight=36,
    background=WHITE,
    foreground=TEXT,
    fieldbackground=WHITE,
    borderwidth=0
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold"),
    background=NAVY,
    foreground=WHITE,
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", "#DBEAFE")],
    foreground=[("selected", NAVY)]
)

style.configure("TEntry", padding=8)
style.configure("TCombobox", padding=8)


# ==================== HELPER FUNCTIONS ====================

def make_button(parent, text, command, color=BLUE):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=NAVY,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=12,
        pady=12
    )


def open_window(title, size):
    window = tk.Toplevel(root)
    window.title(title)
    window.geometry(size)
    window.configure(bg=BG)
    window.transient(root)
    return window


def heading(parent, text):
    tk.Label(
        parent,
        text=text,
        font=("Segoe UI", 19, "bold"),
        bg=BG,
        fg=NAVY
    ).pack(anchor="w", padx=24, pady=(22, 14))


def make_table(parent, columns, labels, widths):
    container = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    container.pack(
        fill="both", expand=True, padx=24, pady=12
    )

    table = ttk.Treeview(
        container,
        columns=columns,
        show="headings"
    )

    for col, label, width in zip(columns, labels, widths):
        table.heading(col, text=label)
        table.column(
            col, width=width, minwidth=70, anchor="center"
        )

    scrollbar = ttk.Scrollbar(
        container,
        orient="vertical",
        command=table.yview
    )
    table.configure(yscrollcommand=scrollbar.set)

    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return table


def refresh_dashboard():
    total_bookings_var.set(str(len(bookings)))
    total_revenue_var.set(
        f"Rs. {sum(b['fare'] for b in bookings):,}"
    )
    seats_var.set(str(sum(r["seats"] for r in routes)))


# ==================== VIEW ROUTES ====================

def show_routes():
    window = open_window("Available Bus Routes", "850x430")
    heading(window, "Available Bus Routes")

    table = make_table(
        window,
        ("id", "route", "departure", "fare", "seats"),
        ("Route ID", "Route", "Departure", "Fare (Rs.)", "Seats"),
        (90, 240, 140, 130, 100)
    )

    for route in routes:
        table.insert(
            "",
            "end",
            values=(
                route["id"],
                f"{route['from']} -> {route['to']}",
                route["departure"],
                f"{route['fare']:,}",
                route["seats"]
            )
        )


# ==================== BOOK TICKET ====================

def book_ticket():
    window = open_window("Book a Ticket", "500x490")
    heading(window, "Book Your Bus Ticket")

    form = tk.Frame(window, bg=WHITE)
    form.pack(fill="x", padx=24, pady=8)

    tk.Label(
        form,
        text="Passenger Name",
        font=("Segoe UI", 11, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=20, pady=(20, 6))

    name_entry = ttk.Entry(form, font=("Segoe UI", 11))
    name_entry.pack(fill="x", padx=20, ipady=4)

    tk.Label(
        form,
        text="Select Route",
        font=("Segoe UI", 11, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", padx=20, pady=(18, 6))

    route_options = [
        f"{r['id']} - {r['from']} to {r['to']} "
        f"(Rs. {r['fare']:,})"
        for r in routes
    ]

    route_combo = ttk.Combobox(
        form,
        values=route_options,
        state="readonly",
        font=("Segoe UI", 10)
    )
    route_combo.pack(fill="x", padx=20, ipady=4)

    def confirm_booking():
        global next_booking_id

        name = name_entry.get().strip().title()
        selected = route_combo.current()

        if not name:
            messagebox.showerror(
                "Missing Information",
                "Please enter the passenger name.",
                parent=window
            )
            return

        if selected < 0:
            messagebox.showerror(
                "Missing Information",
                "Please select a route.",
                parent=window
            )
            return

        route = routes[selected]

        if route["seats"] <= 0:
            messagebox.showerror(
                "No Seats",
                "No seats are available on this route.",
                parent=window
            )
            return

        booking = {
            "id": next_booking_id,
            "name": name,
            "route": f"{route['from']} to {route['to']}",
            "fare": route["fare"],
            "departure": route["departure"],
            "route_id": route["id"]
        }

        bookings.append(booking)
        route["seats"] -= 1
        next_booking_id += 1

        refresh_dashboard()

        messagebox.showinfo(
            "Booking Confirmed",
            f"Ticket booked successfully!\n\n"
            f"Booking ID: {booking['id']}\n"
            f"Passenger: {name}\n"
            f"Route: {booking['route']}\n"
            f"Departure: {booking['departure']}\n"
            f"Fare: Rs. {booking['fare']:,}",
            parent=window
        )
        window.destroy()

    make_button(
        window, "CONFIRM BOOKING", confirm_booking, GREEN
    ).pack(fill="x", padx=24, pady=16)


# ==================== MY BOOKINGS ====================

def show_bookings():
    window = open_window("Passenger Bookings", "1000x440")
    heading(window, "Passenger Bookings")

    table = make_table(
        window,
        ("id", "name", "route", "departure", "fare"),
        ("Booking ID", "Passenger", "Route", "Departure", "Fare (Rs.)"),
        (110, 170, 260, 140, 140)
    )

    if not bookings:
        tk.Label(
            window,
            text="No bookings available yet.",
            font=("Segoe UI", 11),
            bg=BG,
            fg=MUTED
        ).pack(pady=8)

    for booking in bookings:
        table.insert(
            "",
            "end",
            values=(
                booking["id"],
                booking["name"],
                booking["route"],
                booking["departure"],
                f"{booking['fare']:,}"
            )
        )


# ==================== BOOKING REPORT ====================

def show_report():
    window = open_window("Booking Report", "560x430")
    heading(window, "Booking & Revenue Report")

    total = len(bookings)
    revenue = sum(b["fare"] for b in bookings)
    remaining = sum(r["seats"] for r in routes)

    report_items = [
        ("Total Tickets Booked", str(total)),
        ("Total Revenue", f"Rs. {revenue:,}"),
        ("Available Seats", str(remaining)),
        ("Total Routes", str(len(routes)))
    ]

    for label, value in report_items:
        card = tk.Frame(
            window,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill="x", padx=24, pady=7)

        tk.Label(
            card,
            text=label,
            font=("Segoe UI", 11),
            bg=WHITE,
            fg=MUTED
        ).pack(side="left", padx=18, pady=15)

        tk.Label(
            card,
            text=value,
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(side="right", padx=18, pady=15)


# ==================== CANCEL BOOKING ====================

def cancel_booking():
    if not bookings:
        messagebox.showinfo(
            "No Bookings",
            "There are no bookings to cancel.",
            parent=root
        )
        return

    window = open_window("Cancel Booking", "500x340")
    heading(window, "Cancel a Booking")

    tk.Label(
        window,
        text="Enter the Booking ID:",
        font=("Segoe UI", 11),
        bg=BG,
        fg=TEXT
    ).pack(anchor="w", padx=24, pady=8)

    id_entry = ttk.Entry(window, font=("Segoe UI", 12))
    id_entry.pack(fill="x", padx=24, ipady=5)

    def confirm_cancel():
        booking_id = id_entry.get().strip()

        if not booking_id.isdigit():
            messagebox.showerror(
                "Invalid ID",
                "Please enter a numeric Booking ID.",
                parent=window
            )
            return

        booking = next(
            (b for b in bookings if b["id"] == int(booking_id)),
            None
        )

        if booking is None:
            messagebox.showerror(
                "Not Found",
                "That Booking ID was not found.",
                parent=window
            )
            return

        if not messagebox.askyesno(
            "Confirm Cancellation",
            f"Cancel booking #{booking['id']} for "
            f"{booking['name']}?",
            parent=window
        ):
            return

        route = next(
            (
                r for r in routes
                if r["id"] == booking.get("route_id")
            ),
            None
        )

        if route is None:
            route = next(
                (
                    r for r in routes
                    if f"{r['from']} to {r['to']}" == booking["route"]
                ),
                None
            )

        if route:
            route["seats"] += 1

        bookings.remove(booking)
        refresh_dashboard()

        messagebox.showinfo(
            "Cancelled",
            "Booking cancelled successfully.",
            parent=window
        )
        window.destroy()

    make_button(
        window, "CONFIRM CANCELLATION", confirm_cancel, RED
    ).pack(fill="x", padx=24, pady=20)


# ==================== PROFESSIONAL DASHBOARD ====================

# Main layout
app = tk.Frame(root, bg=BG)
app.pack(fill="both", expand=True)

# Left sidebar
sidebar = tk.Frame(app, bg=NAVY, width=225)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="SB",
    font=("Segoe UI", 25, "bold"),
    bg=BLUE,
    fg=WHITE,
    width=3,
    pady=8
).pack(anchor="w", padx=22, pady=(25, 12))

tk.Label(
    sidebar,
    text="SMART BUS",
    font=("Segoe UI", 17, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(anchor="w", padx=22)

tk.Label(
    sidebar,
    text="RESERVATION SYSTEM",
    font=("Segoe UI", 8, "bold"),
    bg=NAVY,
    fg="#A9BED6"
).pack(anchor="w", padx=22, pady=(3, 30))

tk.Label(
    sidebar,
    text="MAIN MENU",
    font=("Segoe UI", 9, "bold"),
    bg=NAVY,
    fg="#91A8C2"
).pack(anchor="w", padx=22, pady=(0, 10))


def sidebar_button(text, command, color=NAVY):
    button = tk.Button(
        sidebar,
        text="   " + text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        anchor="w",
        padx=12,
        pady=12
    )
    button.pack(fill="x", padx=12, pady=3)
    return button


sidebar_button("Dashboard", lambda: refresh_dashboard(), BLUE)
sidebar_button("View Bus Routes", show_routes)
sidebar_button("Book a Ticket", book_ticket)
sidebar_button("Passenger Bookings", show_bookings)
sidebar_button("Booking Report", show_report)
sidebar_button("Cancel Booking", cancel_booking)

tk.Frame(sidebar, bg="#34506E", height=1).pack(
    fill="x", padx=18, pady=(25, 15)
)

sidebar_button("Exit Application", root.destroy, "#9F3038")

tk.Label(
    sidebar,
    text="BUS MANAGEMENT\nSYSTEM  •  v1.0",
    font=("Segoe UI", 8),
    bg=NAVY,
    fg="#A9BED6",
    justify="left"
).pack(side="bottom", anchor="w", padx=22, pady=22)


# Main workspace
workspace = tk.Frame(app, bg=BG)
workspace.pack(side="left", fill="both", expand=True)

# Top navigation bar
topbar = tk.Frame(
    workspace,
    bg=WHITE,
    height=65,
    highlightbackground=BORDER,
    highlightthickness=1
)
topbar.pack(fill="x")
topbar.pack_propagate(False)

tk.Label(
    topbar,
    text="Overview",
    font=("Segoe UI", 12, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(side="left", padx=25)

tk.Label(
    topbar,
    text="ADMIN DASHBOARD",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(side="right", padx=25)


# Page heading
page_head = tk.Frame(workspace, bg=BG)
page_head.pack(fill="x", padx=28, pady=(25, 18))

tk.Label(
    page_head,
    text="Dashboard",
    font=("Segoe UI", 25, "bold"),
    bg=BG,
    fg=NAVY
).pack(anchor="w")

tk.Label(
    page_head,
    text="Welcome back! Manage your bus operations here.",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(5, 0))


# Statistics
stats_frame = tk.Frame(workspace, bg=BG)
stats_frame.pack(fill="x", padx=20, pady=5)

total_bookings_var = tk.StringVar()
total_revenue_var = tk.StringVar()
seats_var = tk.StringVar()


def stat_card(parent, title, variable, accent, subtitle):
    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=7,
        pady=5
    )

    tk.Frame(card, bg=accent, height=4).pack(fill="x")

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 9, "bold"),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w", padx=15, pady=(15, 6))

    tk.Label(
        card,
        textvariable=variable,
        font=("Segoe UI", 19, "bold"),
        bg=WHITE,
        fg=NAVY
    ).pack(anchor="w", padx=15)

    tk.Label(
        card,
        text=subtitle,
        font=("Segoe UI", 8),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w", padx=15, pady=(5, 15))


stat_card(
    stats_frame, "TOTAL BOOKINGS",
    total_bookings_var, BLUE, "Tickets issued"
)
stat_card(
    stats_frame, "TOTAL REVENUE",
    total_revenue_var, GREEN, "From current bookings"
)
stat_card(
    stats_frame, "SEATS AVAILABLE",
    seats_var, "#E9A23B", "Across all routes"
)

refresh_dashboard()


# Quick actions section
actions_section = tk.Frame(workspace, bg=BG)
actions_section.pack(fill="both", expand=True, padx=27, pady=(25, 10))

tk.Label(
    actions_section,
    text="Quick Actions",
    font=("Segoe UI", 16, "bold"),
    bg=BG,
    fg=NAVY
).pack(anchor="w")

tk.Label(
    actions_section,
    text="Choose an operation to continue",
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(4, 15))

action_grid = tk.Frame(actions_section, bg=BG)
action_grid.pack(fill="x")

quick_actions = [
    ("01", "View Bus Routes", "Explore routes and seat availability",
     show_routes, BLUE),
    ("02", "Book a Ticket", "Create a passenger reservation",
     book_ticket, GREEN),
    ("03", "Passenger Bookings", "Review all current bookings",
     show_bookings, BLUE),
    ("04", "Booking Report", "Check revenue and seat totals",
     show_report, PURPLE),
    ("05", "Cancel Booking", "Cancel an existing reservation",
     cancel_booking, RED),
    ("06", "Exit Application", "Close the reservation system",
     root.destroy, NAVY)
]


def action_card(parent, number, title, description, command, accent):
    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1,
        cursor="hand2"
    )

    tk.Label(
        card,
        text=number,
        font=("Segoe UI", 10, "bold"),
        bg=accent,
        fg=WHITE,
        padx=9,
        pady=5
    ).pack(anchor="w", padx=14, pady=(14, 10))

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 11, "bold"),
        bg=WHITE,
        fg=NAVY,
        wraplength=190,
        justify="left"
    ).pack(anchor="w", padx=14)

    tk.Label(
        card,
        text=description,
        font=("Segoe UI", 9),
        bg=WHITE,
        fg=MUTED,
        wraplength=190,
        justify="left"
    ).pack(anchor="w", padx=14, pady=(5, 10))

    tk.Button(
        card,
        text="Open  >",
        command=command,
        font=("Segoe UI", 9, "bold"),
        bg=WHITE,
        fg=accent,
        activebackground="#EFF6FF",
        activeforeground=accent,
        relief="flat",
        bd=0,
        cursor="hand2"
    ).pack(anchor="w", padx=10, pady=(0, 10))

    return card


for index, item in enumerate(quick_actions):
    number, title, description, command, accent = item

    card = action_card(
        action_grid, number, title,
        description, command, accent
    )

    card.grid(
        row=index // 2,
        column=index % 2,
        sticky="nsew",
        padx=7,
        pady=7
    )

for column in range(2):
    action_grid.columnconfigure(column, weight=1)

# Footer
tk.Label(
    workspace,
    text="Smart Bus Reservation System  |  Management Dashboard",
    font=("Segoe UI", 8),
    bg=BG,
    fg=MUTED
).pack(anchor="w", padx=28, pady=(5, 12))

root.mainloop()