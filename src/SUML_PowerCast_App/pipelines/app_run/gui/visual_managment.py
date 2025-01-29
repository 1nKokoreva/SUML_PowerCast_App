import pandas as pd
import matplotlib.dates as mdates
from tkinter import messagebox
import customtkinter as ctk
import re

def show_instruction():
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

    instruction_textbox.insert("1.0", (
         "Witamy w aplikacji PowerCast!\n\n"
        "Aby rozpocząć korzystanie z aplikacji, przeczytaj instrukcje:\n\n"
        "1. Wprowadź dane pogodowe na podstawie podpowiedzi w polu, w którym zapisany jest akceptowalny format.\n\n"
        "2. Wybierz odpowiednie strefy: możesz wybrać na przykład strefę 1, strefę 2 i 3 lub wszystkie 3 itp.\n\n"
        "3. Kliknij przycisk 'Przewiduj' i poczekaj na wyniki w polu 'Wynik przewidywania'.\nWykres w dolnym polu również wizualizuje wyniki.\n\n"
        "4. Możesz użyć przycisku 'Trenuj model', gdy istnieje potrzeba przetrenowania modelu na nowych danych dodanych przez Ciebie"

    ))

    instruction_textbox.configure(state="disabled")


def update_graph(plot1, canvas, selected_zones):
        """
        Update the graph to display only the selected zones.
        """
        try:
            dataframe = pd.read_csv(r"data\01_raw\powerconsumption.csv", parse_dates=["Datetime"])
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

            # Plot only the selected zones
            if 1 in selected_zones:
                plot1.plot(
                    grouped["MonthYear"],
                    grouped["PowerConsumption_Zone1"],
                    label="Zone 1",
                    color="#66CAB3"
                )
            if 2 in selected_zones:
                plot1.plot(
                    grouped["MonthYear"],
                    grouped["PowerConsumption_Zone2"],
                    label="Zone 2",
                    color="#404040"
                )
            if 3 in selected_zones:
                plot1.plot(
                    grouped["MonthYear"],
                    grouped["PowerConsumption_Zone3"],
                    label="Zone 3",
                    color="#21F6D2"
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
    Validate numeric entries for temperature, wind speed, etc. against a simple regex.
    """
    pattern = r"^\d{1,3}([.]\d{1,3})?$"

    fields = {
        "temperature": (temperature, "Temperature"),
        "wind_speed": (wind_speed, "Wind Speed (m/s)"),
        "general_diffuse_flows": (general_diffuse_flows, "General Diffuse Flows"),
        "diffuse_flows": (diffuse_flows, "Diffuse Flows"),
    }

    for field, (value, label) in fields.items():
        print(f"Validating field '{label}': {value}")

        if not value or not isinstance(value, str):
            messagebox.showerror(
                "ERROR",
                message=f'The "{label}" field is empty or invalid. Please enter a value.'
            )
            raise ValueError(f"Invalid or empty value for field '{label}': {value}")

        if not re.match(pattern, value.strip()):
            messagebox.showerror(
                "ERROR",
                message=(
                    f'The input value in the "{label}" field does not match '
                    'the required numeric pattern.'
                )
            )
            raise ValueError(f"Invalid format for field '{label}': {value.strip()}")

        try:
            numeric_value = float(value.strip())
            if not (0 <= numeric_value <= 100):
                messagebox.showerror(
                    "ERROR",
                    message=f'The value in the "{label}" field must be between 0 and 100.'
                )
                raise ValueError(f"Value out of range for field '{label}': {numeric_value}")
        except ValueError:
            messagebox.showerror(
                "ERROR",
                message=f'The value in the "{label}" field is not a valid number.'
            )
            raise

def change_scaling_event(new_scaling: str):
        """
        Adjust the scaling of the UI elements.
        """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)