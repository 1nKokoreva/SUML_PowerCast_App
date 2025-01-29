"""
Module for managing the visualization and user interface of PowerCast.
This module includes functions for data analysis, validation, and UI updates.

Technologies used:
- Pandas: for data handling and processing.
- Matplotlib & Seaborn: for visualization.
- CustomTkinter: for UI management.
- Re (Regular Expressions): for input validation.
- Tkinter Messagebox: for displaying error messages.
"""

import re
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import seaborn as sns
import customtkinter as ctk
from tkinter import messagebox


def show_instruction():
    """
    Displays an instruction window with guidelines on using the application.
    """
    instruction_window = ctk.CTkToplevel()
    instruction_window.title("PowerCast_Instruction")
    instruction_window.geometry("400x300")
    instruction_window.grab_set()

    instruction_textbox = ctk.CTkTextbox(
        instruction_window,
        width=360,
        height=260,
        fg_color="transparent",
        border_width=0,
        wrap="word",
        font=("Arial", 12),
    )
    instruction_textbox.pack(pady=10, padx=10, fill="both", expand=True)

    instruction_text = (
        "Witamy w aplikacji PowerCast!\n\n"
        "Aby rozpocząć korzystanie z aplikacji, przeczytaj instrukcje:\n\n"
        "1. Wprowadź dane pogodowe na podstawie podpowiedzi w polu, w którym zapisany jest akceptowalny format.\n\n"
        "2. Wybierz odpowiednie strefy: możesz wybrać na przykład strefę 1, strefę 2 i 3 lub wszystkie 3 itp.\n\n"
        "3. Kliknij przycisk 'Przewiduj' i poczekaj na wyniki w polu 'Wynik przewidywania'.\n"
        "   Wykres w dolnym polu również wizualizuje wyniki.\n\n"
        "4. Możesz użyć przycisku 'Trenuj model', gdy istnieje potrzeba przetrenowania modelu na nowych danych dodanych przez Ciebie."
    )

    instruction_textbox.insert("1.0", instruction_text)
    instruction_textbox.configure(state="disabled")


def update_graph(plot1, canvas, selected_zones):
    """
    Updates the graph based on the selected zones.

    Args:
        plot1 (matplotlib.axes.Axes): The plot to update.
        canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg): The canvas to redraw.
        selected_zones (list): List of selected zone numbers (1, 2, or 3).
    """
    try:
        dataframe = pd.read_csv(
            r"data\01_raw\powerconsumption.csv", parse_dates=["Datetime"]
        )
        dataframe["Datetime"] = pd.to_datetime(dataframe["Datetime"], errors="coerce")
        dataframe["MonthYear"] = dataframe["Datetime"].dt.strftime("%m.%y")

        grouped = (
            dataframe.groupby("MonthYear")[
                ["PowerConsumption_Zone1", "PowerConsumption_Zone2", "PowerConsumption_Zone3"]
            ]
            .mean()
            .reset_index()
        )

        grouped["MonthYear"] = pd.to_datetime(grouped["MonthYear"], format="%m.%y")
        grouped = grouped.sort_values("MonthYear")

        plot1.clear()

        # Plot selected zones
        colors = {1: "#66CAB3", 2: "#404040", 3: "#21F6D2"}
        labels = {1: "Zone 1", 2: "Zone 2", 3: "Zone 3"}

        for zone in selected_zones:
            plot1.plot(
                grouped["MonthYear"],
                grouped[f"PowerConsumption_Zone{zone}"],
                label=labels[zone],
                color=colors[zone]
            )

        plot1.set_xlabel("Month and Year")
        plot1.set_ylabel("Power Consumption")
        plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m.%y"))
        plot1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plot1.tick_params(axis="x", rotation=45)
        plot1.legend()
        canvas.draw()

    except Exception as exc:
        messagebox.showerror("Error", f"Failed to update graph: {exc}")


def check_number_format(temperature, wind_speed, general_diffuse_flows, diffuse_flows):
    """
    Validates numeric input fields using regex and range constraints.

    Args:
        temperature (str): Temperature input.
        wind_speed (str): Wind speed input.
        general_diffuse_flows (str): General diffuse flows input.
        diffuse_flows (str): Diffuse flows input.

    Raises:
        ValueError: If any value is empty, improperly formatted, or out of range.
    """
    pattern = r"^\d{1,3}(\.\d{1,3})?$"
    fields = {
        "Temperature": temperature,
        "Wind Speed (m/s)": wind_speed,
        "General Diffuse Flows": general_diffuse_flows,
        "Diffuse Flows": diffuse_flows,
    }

    for label, value in fields.items():
        print(f"Validating field '{label}': {value}")

        if not value or not isinstance(value, str):
            messagebox.showerror("ERROR", f'The "{label}" field is empty or invalid.')
            raise ValueError(f"Invalid or empty value for field '{label}': {value}")

        if not re.match(pattern, value.strip()):
            messagebox.showerror("ERROR", f'The input in "{label}" does not match the numeric pattern.')
            raise ValueError(f"Invalid format for field '{label}': {value.strip()}")

        try:
            numeric_value = float(value.strip())
            if not (0 <= numeric_value <= 100):
                messagebox.showerror("ERROR", f'The value in "{label}" must be between 0 and 100.')
                raise ValueError(f"Value out of range for field '{label}': {numeric_value}")
        except ValueError:
            messagebox.showerror("ERROR", f'The value in "{label}" is not a valid number.')
            raise


def change_scaling_event(new_scaling: str):
    """
    Adjusts the scaling of the UI elements.

    Args:
        new_scaling (str): New scaling percentage (e.g., "100%").
    """
    try:
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
    except ValueError:
        messagebox.showerror("ERROR", "Invalid scaling value. Please enter a percentage (e.g., 100%).")
