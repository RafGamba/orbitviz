import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import LabelFrame, Entry, Button, Label, Separator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
from tkinter import messagebox

from orbital_calculator import generate_orbit
from plotter import plot_orbit

import os

# ---------- Funzioni ----------
def on_calculate():
    try:
        a = float(entry_a.get())
        e = float(entry_e.get())
        i = float(entry_i.get())
        raan = float(entry_raan.get())
        argp = float(entry_argp.get())
        nu = float(entry_nu.get())

        coords = generate_orbit(a, e, i, raan, argp, nu)
        ax.clear()
        plot_orbit(ax, coords)
        canvas.draw()

        # Tipo di orbita
        if e < 1e-3:
            orbit_type.set("Circolare")
        elif e < 1:
            orbit_type.set("Ellittica")
        elif abs(e - 1.0) < 1e-2:
            orbit_type.set("Parabolica")
        else:
            orbit_type.set("Iperbolica")

        error_label.config(text="")
        status_var.set("Calcolo completato con successo.")
        show_details_btn.config(state="normal")
    except Exception as e:
        error_label.config(text=f"Errore: {e}")
        status_var.set("Errore nel calcolo.")

def on_save():
    fig.savefig("orbita.png")
    error_label.config(text="Grafico salvato come 'orbita.png'")
    status_var.set("Grafico salvato.")

def on_reset():
    for entry in [entry_a, entry_e, entry_i, entry_raan, entry_argp, entry_nu]:
        entry.delete(0, tk.END)
    orbit_type.set("")
    error_label.config(text="")
    ax.clear()
    canvas.draw()
    status_var.set("Reset completato.")
    show_details_btn.config(state="disabled")

def add_tooltip(widget, text):
    def on_enter(e):
        tooltip.config(text=text)
        tooltip.place(x=e.x_root - root.winfo_rootx() + 10,
                      y=e.y_root - root.winfo_rooty() + 10)
    def on_leave(e):
        tooltip.place_forget()
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

def show_details():
    try:
        a = float(entry_a.get())
        e = float(entry_e.get())
        i = float(entry_i.get())
        raan = float(entry_raan.get())
        argp = float(entry_argp.get())
        nu = float(entry_nu.get())
        details = (
            f"Semiasse maggiore (a): {a:.2f} km\n"
            f"Eccentricità (e): {e:.4f}\n"
            f"Inclinazione (i): {i:.2f}°\n"
            f"RAAN: {raan:.2f}°\n"
            f"Argomento del perigeo (ω): {argp:.2f}°\n"
            f"Anomalia vera (ν): {nu:.2f}°\n"
            f"Tipo di orbita: {orbit_type.get()}"
        )
        messagebox.showinfo("Dettagli Orbitali", details)
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile mostrare i dettagli: {e}")

def validate_float(P):
    if P == "" or P == "-":
        return True
    try:
        float(P)
        return True
    except ValueError:
        root.bell()
        return False

def switch_theme():
    global current_theme
    if current_theme == "darkly":
        style.theme_use("flatly")
        current_theme = "flatly"
        status_var.set("Tema chiaro attivo.")
    else:
        style.theme_use("darkly")
        current_theme = "darkly"
        status_var.set("Tema scuro attivo.")

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("OrbitViz")
root.geometry("1200x700")
style = Style("darkly")
current_theme = "darkly"

# ---------- Menu Bar ----------
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Salva Grafico", command=on_save)
file_menu.add_separator()
file_menu.add_command(label="Esci", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="Guida", command=lambda: messagebox.showinfo("Guida", "Inserisci i parametri orbitali e premi 'Genera Orbita'."))
help_menu.add_command(label="Informazioni", command=lambda: messagebox.showinfo("Info", "Orbital Visualizer Pro\nby Orbitviz Team"))
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

# ---------- Header con logo ----------
header = tk.Frame(root, bg="#1f1f1f", height=80)
header.pack(side=tk.TOP, fill=tk.X)

title = tk.Label(header, text="OrbitViz", font=("Segoe UI", 22, "bold"), bg="#1f1f1f", fg="white")
title.pack(side=tk.LEFT, padx=20)

# (Facoltativo) Logo a destra
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path).resize((50, 50))
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header, image=logo, bg="#1f1f1f")
    logo_label.pack(side=tk.RIGHT, padx=20)

# ---------- Input Panel ----------
input_frame = LabelFrame(root, text="Parametri Orbitali", padding=10)
input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

vcmd = (root.register(validate_float), "%P")

def make_input(label, row, tooltip_text, unit):
    lbl = Label(input_frame, text=label)
    lbl.grid(row=row, column=0, sticky="w", pady=5, padx=(0,5))
    ent = Entry(input_frame, validate="key", validatecommand=vcmd, width=12)
    ent.grid(row=row, column=1, pady=5, sticky="ew")
    unit_lbl = Label(input_frame, text=unit, foreground="#888")
    unit_lbl.grid(row=row, column=2, sticky="w")
    add_tooltip(ent, tooltip_text)
    return ent

entry_a = make_input("a", 0, "Semiasse maggiore in km (es: 7000)", "km")
entry_e = make_input("e", 1, "Eccentricità orbitale (0=circolare)", "")
entry_i = make_input("i", 2, "Inclinazione rispetto all'equatore", "°")
entry_raan = make_input("RAAN", 3, "Longitudine nodo ascendente", "°")
entry_argp = make_input("ω", 4, "Argomento del perigeo", "°")
entry_nu = make_input("ν", 5, "Anomalia vera iniziale", "°")

Button(input_frame, text="Genera Orbita", command=on_calculate, bootstyle="success").grid(row=6, columnspan=3, pady=15, sticky="ew")
Button(input_frame, text="Salva Grafico", command=on_save, bootstyle="secondary").grid(row=7, columnspan=3, pady=5, sticky="ew")
Button(input_frame, text="Reset", command=on_reset, bootstyle="warning").grid(row=8, columnspan=3, pady=5, sticky="ew")

orbit_type = tk.StringVar(value="")
Label(input_frame, textvariable=orbit_type, font=("Segoe UI", 12, "bold")).grid(row=9, columnspan=3, pady=10)

error_label = Label(input_frame, text="", foreground="red")
error_label.grid(row=10, columnspan=3)

show_details_btn = Button(input_frame, text="Mostra Dettagli", command=show_details, bootstyle="info", state="disabled")
show_details_btn.grid(row=11, columnspan=3, pady=5, sticky="ew")

theme_btn = Button(input_frame, text="Cambia Tema", command=switch_theme, bootstyle="dark")
theme_btn.grid(row=12, columnspan=3, pady=5, sticky="ew")

tooltip = tk.Label(root, text="", bg="yellow", fg="black", relief="solid", bd=1, padx=4, pady=2, font=("Segoe UI", 8))
tooltip.place_forget()

# ---------- Plot Area ----------
plot_frame = LabelFrame(root, text="Visualizzazione Orbitale", padding=10)
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

fig = Figure(figsize=(7, 7), dpi=100)
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect([1, 1, 1])
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ---------- Status Bar ----------
status_var = tk.StringVar(value="Pronto.")
Separator(root, orient="horizontal").pack(side=tk.BOTTOM, fill=tk.X)
status_bar = Label(root, textvariable=status_var, anchor="w", font=("Segoe UI", 9), background="#222", foreground="#eee")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()