import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CSV_FILE = "Temperatura UPB.csv"

def preprocess_data(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'Temperature' in df.columns and 'Date' in df.columns and 'Time' in df.columns:
            df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
            df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y', errors='coerce')
            df['Time'] = pd.to_datetime(df['Time'], format='%I:%M:%S %p', errors='coerce').dt.time
            df = df.dropna(subset=['Date', 'Time'])
            df['Datetime'] = df.apply(lambda row: datetime.combine(row['Date'], row['Time']), axis=1)
            df = df.dropna(subset=['Datetime'])
            print(df.dtypes)
            return df
        else:
            raise ValueError("The CSV file does not have the required columns: 'Temperature', 'Date', 'Time'")
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return None

def display_graph(df, year, parent):
    df_filtered = df[df['Datetime'].dt.year == year]
    graph_window = tk.Toplevel(parent)
    graph_window.title(f"Graph for {year}")
    graph_window.geometry("800x600")
    figure, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df_filtered['Datetime'], df_filtered['Temperature'], label=f"Temperature in {year}", color="blue")
    ax.set_title(f"Temperature Over Time - {year}")
    ax.set_xlabel("Datetime")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    canvas = FigureCanvasTkAgg(figure, master=graph_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

df = preprocess_data(CSV_FILE)
if df is None:
    raise RuntimeError("Failed to load or process the predefined CSV file.")

root = tk.Tk()
root.geometry("400x200")
root.title("Preconizare Meteo")

unique_years = sorted(df['Datetime'].dt.year.unique())
tk.Label(root, text="Select Year:").grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
year_combobox = ttk.Combobox(root, values=unique_years, state="readonly")
year_combobox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

def on_year_selected(event):
    selected_year = year_combobox.get()
    if selected_year.isdigit():
        display_graph(df, int(selected_year), root)

year_combobox.bind("<<ComboboxSelected>>", on_year_selected)

root.mainloop()
