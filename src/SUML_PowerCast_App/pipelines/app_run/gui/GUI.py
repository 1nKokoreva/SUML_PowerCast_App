"""
This module defines the main GUI (Graphical User Interface) for the PowerCast application.
It uses tkinter/customtkinter for the desktop interface, Matplotlib for plots, and
communicates with a FastAPI endpoint to retrieve predictions.
"""

import os
import re
import shutil
import tkinter
from tkinter import filedialog
import tkinter.messagebox as messagebox
from datetime import datetime

import pandas as pd
import customtkinter as ctk
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import requests

from dictionary import dictionery
#from SUML_PowerCast_App.pipelines.app_run.gui.dictionary import dictionery


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(
    CURRENT_PATH,
    "..", "..", "..", "..", "..", "data", "01_raw", "powerconsumption.csv"
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme(os.path.join(CURRENT_PATH, "Assets", "own_theme.json"))


class App(ctk.CTk):
    """
    Main application window class for the PowerCast App.
    Manages layout, widgets, and user interactions.
    """

    def __init__(self):
        """
        Initialize the GUI components and set up the main interface layout.
        """
        super().__init__()
        self.show_instruction()

        self.title("PowerCast_App")
        self.iconbitmap(os.path.join(CURRENT_PATH, "Assets", "iconic.ico"))
        self.geometry(f"{880}x{800}")

        self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure((1, 2), weight=1)

        self.language = "PL"

        # Logo
        self.logo_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(CURRENT_PATH, "Assets", "PowerCast.png")),
            dark_image=Image.open(os.path.join(CURRENT_PATH, "Assets", "PowerCast_white.png")),
            size=(380, 60)
        )
        self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="")
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="nw")

        # Sidebar menu
        self.left_menu = ctk.CTkFrame(self, width=140)
        self.left_menu.grid(row=1, column=0, rowspan=3, padx=(20, 20), pady=(10, 20), sticky="nsew")
        self.left_menu.grid_rowconfigure(4, weight=1)

        self.download_button = ctk.CTkButton(
            self.left_menu,
            height=37,
            text=dictionery[self.language]["download_button"],
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self.download_dataset
        )
        self.download_button.grid(row=0, column=0, padx=20, pady=10)

        self.train_button = ctk.CTkButton(
            self.left_menu,
            height=37,
            text=dictionery[self.language]["train_button"],
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self.train_model
        )
        self.train_button.grid(row=1, column=0, padx=20, pady=10)

        self.update_graph_button = ctk.CTkButton(
            self.left_menu,
            height=37,
            text=dictionery[self.language]["update_graph"],
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self.update_graph
        )
        self.update_graph_button.grid(row=2, column=0, pady=20, padx=10)

        self.language_mode_label = ctk.CTkLabel(
            self.left_menu,
            fg_color="transparent",
            text=dictionery[self.language]["language"],
            anchor="w"
        )
        self.language_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.language_mode_optionemenu = ctk.CTkOptionMenu(
            self.left_menu,
            values=["PL", "ENG", "RU"],
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self.change_language
        )
        self.language_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_label = ctk.CTkLabel(
            self.left_menu,
            fg_color="transparent",
            text=dictionery[self.language]["appearance_mode"],
            anchor="w"
        )
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.left_menu,
            values=["Light", "Dark"],
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(
            self.left_menu,
            fg_color="transparent",
            text=dictionery[self.language]["ui_scale"],
            anchor="w"
        )
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = ctk.CTkOptionMenu(
            self.left_menu,
            values=["80%", "90%", "100%", "110%", "120%"],
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self.change_scaling_event
        )
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=10)

        # Main frame
        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.center_frame.grid_rowconfigure(1, weight=1)
        self.center_frame.grid_rowconfigure((0, 2), weight=0)
        self.center_frame.grid_columnconfigure((0, 1), weight=1)

        self.info_label = ctk.CTkTextbox(
            self.center_frame,
            height=80,
            wrap="word",
            activate_scrollbars=True
        )
        self.info_label.grid(row=0, column=0, columnspan=2, padx=7, pady=7, sticky="new")

        # Entry frame
        self.entry_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent", border_width=0, height=150)
        self.entry_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.temperature_label = ctk.CTkLabel(
            self.entry_frame,
            text=dictionery[self.language]["temperature"],
            anchor="w"
        )
        self.temperature_label.grid(row=0, column=0, padx=2, pady=0, sticky="w")
        self.entry_frame.grid_columnconfigure(1, weight=1)
        self.temperature = ctk.CTkEntry(self.entry_frame, placeholder_text="6.58")
        self.temperature.grid(row=0, column=1, padx=5, pady=(0, 3), sticky="ew")

        self.humidity_label = ctk.CTkLabel(
            self.entry_frame,
            text=dictionery[self.language]["humidity"],
            anchor="w"
        )
        self.humidity_label.grid(row=1, column=0, padx=2, pady=0, sticky="w")

        self.humidity = ctk.CTkEntry(self.entry_frame, placeholder_text="77.5")
        self.humidity.grid(row=1, column=1, padx=5, pady=(0, 3), sticky="ew")

        self.wind_speed_label = ctk.CTkLabel(
            self.entry_frame,
            text=dictionery[self.language]["wind_speed"],
            anchor="w"
        )
        self.wind_speed_label.grid(row=2, column=0, padx=2, pady=0, sticky="w")

        self.wind_speed = ctk.CTkEntry(self.entry_frame, placeholder_text="0.077")
        self.wind_speed.grid(row=2, column=1, padx=5, pady=(0, 3), sticky="ew")

        self.general_diffuse_flows_label = ctk.CTkLabel(
            self.entry_frame,
            text=dictionery[self.language]["general_flows"],
            anchor="w"
        )
        self.general_diffuse_flows_label.grid(row=3, column=0, padx=2, pady=0, sticky="w")

        self.general_diffuse_flows = ctk.CTkEntry(self.entry_frame, placeholder_text="28.8")
        self.general_diffuse_flows.grid(row=3, column=1, padx=5, pady=(0, 3), sticky="ew")

        self.diffuse_flows_label = ctk.CTkLabel(
            self.entry_frame,
            text=dictionery[self.language]["flows"],
            anchor="w"
        )
        self.diffuse_flows_label.grid(row=4, column=0, padx=2, pady=0, sticky="w")

        self.diffuse_flows = ctk.CTkEntry(self.entry_frame, placeholder_text="35.29")
        self.diffuse_flows.grid(row=4, column=1, padx=5, pady=(0, 5), sticky="ew")

        # Zone selection
        self.checkbox_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent", border_width=0)
        self.checkbox_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.checkbox_label = ctk.CTkLabel(self.checkbox_frame, text=dictionery[self.language]["necessary_zone"])
        self.checkbox_label.grid(row=0, column=0, padx=5, pady=0, sticky="n")

        self.zone_1_var = tkinter.BooleanVar(value=False)
        self.zone_2_var = tkinter.BooleanVar(value=False)
        self.zone_3_var = tkinter.BooleanVar(value=False)

        self.zone_1 = ctk.CTkCheckBox(
            self.checkbox_frame,
            variable=self.zone_1_var,
            text=dictionery[self.language]["zone_one"]
        )
        self.zone_1.grid(row=1, column=0, padx=20, pady=2, sticky="w")

        self.zone_2 = ctk.CTkCheckBox(
            self.checkbox_frame,
            variable=self.zone_2_var,
            text=dictionery[self.language]["zone_two"]
        )
        self.zone_2.grid(row=2, column=0, padx=20, pady=2, sticky="w")

        self.zone_3 = ctk.CTkCheckBox(
            self.checkbox_frame,
            variable=self.zone_3_var,
            text=dictionery[self.language]["zone_three"]
        )
        self.zone_3.grid(row=3, column=0, padx=20, pady=2, sticky="w")

        self.predict_button = ctk.CTkButton(
            self.center_frame,
            height=37,
            text=dictionery[self.language]["predict_button"],
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self.predict
        )
        self.predict_button.grid(row=2, column=0, columnspan=2, pady=7, padx=7)

        self.label_frame = ctk.CTkFrame(self)
        self.label_frame.grid(row=2, column=1, padx=20, sticky="nsew")

        self.result_label = ctk.CTkLabel(
            self.label_frame,
            anchor='w',
            fg_color=["#F7F7F7", "gray17"],
            wraplength=500,
            text=dictionery[self.language]["result"]
        )
        self.result_label.grid(row=0, column=0, padx=10, pady=10)

        # Graph
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.grid(row=3, column=1, pady=20, padx=20, sticky="nsew")

        self.fig = Figure(figsize=(5, 5), dpi=87)
        self.plot1 = self.fig.add_subplot(1, 1, 1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")
        self.info_label.insert("1.0", dictionery[self.language]["info_text"])
        self.info_label.configure(state="disabled")

        self.update_texts()

    def show_instruction(self):
        instruction_window = ctk.CTkToplevel(self)
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
            "2. Wybierz odpowiednie strefy: możesz wybrać strefę 1, strefy 2 i 3, lub wszystkie 3!\n\n"
            "3. Kliknij przycisk 'Przewiduj' i poczekaj na wyniki w polu 'Wynik przewidywania'.\n\n"
            "4. Kliknij przycisk „Aktualizuj wykres”, aby wyświetlić wykres ze zaktualizowanymi informacjami."
        ))

        instruction_textbox.configure(state="disabled")


    def update_graph(self, selected_zones):
        """
        Update the graph to display only the selected zones.
        """
        try:
            dataframe = pd.read_csv(csv_path, parse_dates=["Datetime"])
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

            self.plot1.clear()

            # Plot only the selected zones
            if 1 in selected_zones:
                self.plot1.plot(
                    grouped["MonthYear"],
                    grouped["PowerConsumption_Zone1"],
                    label="Zone 1",
                    color="#66CAB3"
                )
            if 2 in selected_zones:
                self.plot1.plot(
                    grouped["MonthYear"],
                    grouped["PowerConsumption_Zone2"],
                    label="Zone 2",
                    color="#404040"
                )
            if 3 in selected_zones:
                self.plot1.plot(
                    grouped["MonthYear"],
                    grouped["PowerConsumption_Zone3"],
                    label="Zone 3",
                    color="#21F6D2"
                )

            self.plot1.set_xlabel("Month and Year")
            self.plot1.set_ylabel("Power Consumption")
            self.plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m.%y"))
            self.plot1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            self.plot1.tick_params(axis="x", rotation=45)

            self.plot1.legend()
            self.canvas.draw()

        except Exception as exc:
            messagebox.showerror("Error", f"Failed to update graph: {exc}")

    def update_texts(self):
        """
        Update all UI texts based on the currently selected language.
        """
        if hasattr(self, 'language'):
            self.download_button.configure(text=dictionery[self.language]["download_button"])
            self.train_button.configure(text=dictionery[self.language]["train_button"])
            self.update_graph_button.configure(text=dictionery[self.language]["update_graph"])
            self.language_mode_label.configure(text=dictionery[self.language]["language"])
            self.appearance_mode_label.configure(text=dictionery[self.language]["appearance_mode"])
            self.scaling_label.configure(text=dictionery[self.language]["ui_scale"])
            self.temperature_label.configure(text=dictionery[self.language]["temperature"])
            self.humidity_label.configure(text=dictionery[self.language]["humidity"])
            self.wind_speed_label.configure(text=dictionery[self.language]["wind_speed"])
            self.general_diffuse_flows_label.configure(text=dictionery[self.language]["general_flows"])
            self.diffuse_flows_label.configure(text=dictionery[self.language]["flows"])
            self.checkbox_label.configure(text=dictionery[self.language]["necessary_zone"])
            self.zone_1.configure(text=dictionery[self.language]["zone_one"])
            self.zone_2.configure(text=dictionery[self.language]["zone_two"])
            self.zone_3.configure(text=dictionery[self.language]["zone_three"])
            self.predict_button.configure(text=dictionery[self.language]["predict_button"])
            self.result_label.configure(text=dictionery[self.language]["result"])

            self.info_label.configure(state="normal")
            self.info_label.delete("1.0", "end")
            self.info_label.insert("1.0", dictionery[self.language]["info_text"])
            self.info_label.configure(state="disabled")

    def change_language(self, new_language: str):
        """
        Change the current language and update all texts.
        """
        self.language = new_language
        self.update_texts()

    def check_number_format(self):
        """
        Validate numeric entries for temperature, wind speed, etc. against a simple regex.
        """
        pattern = r"^\d{1,3}([.]\d{1,3})?$"

        fields = {
            "temperature": (self.temperature.get(), "Temperature"),
            "wind_speed": (self.wind_speed.get(), "Wind Speed (m/s)"),
            "general_diffuse_flows": (self.general_diffuse_flows.get(), "General Diffuse Flows"),
            "diffuse_flows": (self.diffuse_flows.get(), "Diffuse Flows"),
        }

        for _, (value, label) in fields.items():
            if not value.strip():
                messagebox.showerror(
                    "ERROR",
                    message=f'The "{label}" field is empty. Please enter a value.'
                )
                return

            if not re.match(pattern, value):
                messagebox.showerror(
                    "ERROR",
                    message=(
                        f'The input value in the "{label}" field does not match '
                        'the required numeric pattern.'
                    )
                )
                return

        print("The values are correct")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """
        Change the appearance mode (light/dark).
        """
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        """
        Adjust the scaling of the UI elements.
        """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        """
        Handle sidebar button clicks (e.g., 'Download' or 'Train' buttons).
        """
        print("Sidebar button clicked")

    def predict(self):
        """
        Gather user inputs, send them to the API for predictions, and update the graph for selected zones.
        """
        try:
            data = {
                "temperature": float(self.temperature.get()),
                "humidity": float(self.humidity.get()),
                "wind_speed": float(self.wind_speed.get()),
                "general_diffuse_flows": float(self.general_diffuse_flows.get()),
                "diffuse_flows": float(self.diffuse_flows.get()),
                "target_zones": self.get_target_zones(),
            }
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values in all fields.")
            return


        try:
            response = requests.post(
                "http://localhost:8000/predict",
                json=data,
                timeout=5  # Add a timeout to avoid indefinite hanging
            )
            response.raise_for_status()
            result = response.json()
            predictions = result.get("predictions", {})

            # Format the predictions
            formatted_result = "Wynik przewidywania:\n"
            for zone, value in predictions.items():
                zone_name = zone.replace("PowerConsumption_", "")
                if isinstance(value, list) and len(value) > 0:
                    value = value[0]
                formatted_result += f"{zone_name}: {int(value)}W\n"

            self.result_label.configure(text=formatted_result)


            # Update graph with selected zones
            selected_zones = self.get_target_zones()
            if selected_zones:
                self.update_graph(selected_zones)
            else:
                messagebox.showinfo("No Zones Selected", "Please select at least one zone to display.")

        except requests.RequestException as exc:
            messagebox.showerror("API Error", f"Failed to fetch prediction: {exc}")

    def train_model(self):
        """
        Send a request to the API to train the model.
        """
        try:
            response = requests.get(
                "http://localhost:8000/update",
                timeout=300
            )
            response.raise_for_status()

            messagebox.showinfo("Complete", "Your model has been trained")

        except requests.RequestException as exc:
            messagebox.showerror("Training Error", f"Failed to train the model: {exc}")

    def get_target_zones(self):
        """
        Return a list of selected zones (1, 2, 3) based on the user's checkbox choices.
        """
        zones = []
        if self.zone_1_var.get():
            zones.append(1)
        if self.zone_2_var.get():
            zones.append(2)
        if self.zone_3_var.get():
            zones.append(3)
        return zones
    
    def download_dataset(self):
        """
        Метод для скачивания CSV файла.
        """
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save CSV file"
            )

            if file_path:
                shutil.copy(csv_path, file_path)
                messagebox.showinfo("Success", f"File saved successfully at {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
