"""
This module defines the main GUI (Graphical User Interface) for the PowerCast application.
It uses tkinter/customtkinter for the desktop interface, Matplotlib for plots, and
communicates with a FastAPI endpoint to retrieve predictions.
"""
import os
import shutil
import tkinter
from tkinter import filedialog
import tkinter.messagebox as messagebox

import customtkinter as ctk
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

from SUML_PowerCast_App.pipelines.app_run.gui.dictionary import dictionery
from SUML_PowerCast_App.pipelines.app_run.gui.visual_managment import show_instruction, update_graph, change_scaling_event, check_number_format

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

        show_instruction()

        self.title("PowerCast_App")
        self.iconbitmap(os.path.join(CURRENT_PATH, "Assets", "iconic.ico"))
        self.geometry(f"{900}x{800}")

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
            command=self.train_process
        )
        self.train_button.grid(row=1, column=0, padx=20, pady=10)


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
            command=change_scaling_event
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

        # Entry frames
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

        self.fig = Figure(figsize=(5, 5), dpi=85)
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

        

    def validate_fields(self):
        try:
            print("Temperature:", self.temperature.get())
            print("Wind Speed:", self.wind_speed.get())
            print("General Diffuse Flows:", self.general_diffuse_flows.get())
            print("Diffuse Flows:", self.diffuse_flows.get())

            # Вызов проверки
            check_number_format(
                self.temperature.get(),
                self.wind_speed.get(),
                self.general_diffuse_flows.get(),
                self.diffuse_flows.get(),
            )
            print("All fields validated successfully!")
        except AttributeError as e:
            print(f"AttributeError: {e}")
            messagebox.showerror("ERROR", "An attribute is missing. Please check all fields.")
        except ValueError:
            pass
        except Exception as e:
            print(f"Unexpected error: {e}")
            messagebox.showerror("ERROR", "An unexpected error occurred.")

    def update_texts(self):
        """
        Update all UI texts based on the currently selected language.
        """
        if hasattr(self, 'language'):
            self.download_button.configure(text=dictionery[self.language]["download_button"])
            self.train_button.configure(text=dictionery[self.language]["train_button"])
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

    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        """
        Change the appearance mode (light/dark).
        """
        ctk.set_appearance_mode(new_appearance_mode)


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
                update_graph(self.plot1, self.canvas, selected_zones)
            else:
                messagebox.showinfo("No Zones Selected", "Please select at least one zone to display.")

        except requests.RequestException as exc:
            messagebox.showerror("API Error", f"Failed to fetch prediction: {exc}")
    
    def train_process(self):
        """Обработчик для кнопки тренировки модели"""
        messagebox.showinfo("Start process", "Please wait a bit. The process will take some time...") 
        self.train_model()  



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
        The method for downloading a CSV file.        
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
