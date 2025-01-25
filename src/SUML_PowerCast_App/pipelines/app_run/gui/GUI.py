import os
import re
import tkinter
import tkinter.messagebox as messagebox
import customtkinter as ctk
from PIL import Image, ImageTk 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dictionary import dictionery
import requests
from datetime import datetime

current_path = os.path.dirname(os.path.realpath(__file__))

ctk.set_appearance_mode("light") 
ctk.set_default_color_theme(current_path + "/Assets/own_theme.json")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.title("PowerCast_App")
        self.iconbitmap(current_path +"/Assets/iconic.ico")
        self.geometry(f"{880}x{700}")
    
        self.grid_rowconfigure((0,1,2), weight=0)  
        self.grid_rowconfigure( 3, weight=1)  
        self.grid_columnconfigure(0, weight=0)  
        self.grid_columnconfigure((1, 2), weight=1) 
        #self.bg_image = ctk.CTkImage(Image.open(current_path + "/Assets/background.jpg"), size=(500, 250))
        self.language = "PL"
        # logo
        self.logo_image = ctk.CTkImage(light_image=Image.open(current_path + "/Assets/PowerCast.png"),dark_image=Image.open(current_path + "/Assets/PowerCast_white.png"), size=(380, 60))
        self.logo_label = ctk.CTkLabel(self,  image=self.logo_image, text="")
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="nw")

        # sidebar menu
        self.left_menu = ctk.CTkFrame(self, width=140)
        self.left_menu.grid(row=1, column=0, rowspan=3, padx=(20, 20), pady=(10, 20), sticky="nsew")
        self.left_menu.grid_rowconfigure(4, weight=1)

        self.download_button = ctk.CTkButton(self.left_menu, height=37, text=dictionery[self.language]["download_button"],
                                             font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                             command=self.sidebar_button_event)
        self.download_button.grid(row=0, column=0, padx=20, pady=10)

        self.train_button = ctk.CTkButton(self.left_menu, height=37, text=dictionery[self.language]["train_button"],
                                          font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                          command=self.sidebar_button_event)
        self.train_button.grid(row=1, column=0, padx=20, pady=10)

        self.language_mode_label = ctk.CTkLabel(self.left_menu, fg_color="transparent", text=dictionery[self.language]["language"], anchor="w")
        self.language_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.language_mode_optionemenu = ctk.CTkOptionMenu(self.left_menu, values=["PL", "ENG", "RU"],
                                                           font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                                           command=self.change_language)
        self.language_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_label = ctk.CTkLabel(self.left_menu, fg_color="transparent", text=dictionery[self.language]["appearance_mode"], anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.left_menu, values=["Light", "Dark"],
                                                             font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self.left_menu, fg_color="transparent", text=dictionery[self.language]["ui_scale"], anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.left_menu, values=["80%", "90%", "100%", "110%", "120%"],
                                                     font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                                     command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=10)

        # ==========================================================================================
        
        # Main frame
        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.center_frame.grid_rowconfigure(1, weight=1)
        self.center_frame.grid_rowconfigure((0, 2), weight=0)
        self.center_frame.grid_columnconfigure((0, 1), weight=1)

        # Вложенный текстовый заголовок
        self.info_label = ctk.CTkTextbox(self.center_frame,  height=80, wrap="word", activate_scrollbars=True)
        self.info_label.grid(row=0, column=0, columnspan=2, padx=7, pady=7, sticky="new")

        # Вложенный текстовый блок (левый)
        self.entry_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent", border_width=0, height=150)
        self.entry_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")


        # Temperature
        #self.humidity = ctk.CTkSlider(self.entry_frame, from_=0, to=100, command=self.slider_event)
        self.temperature_label = ctk.CTkLabel(self.entry_frame, text=dictionery[self.language]["temperature"], anchor="w")
        self.temperature_label.grid(row=0, column=0, padx=2, pady=0, sticky="w")
        self.temperature = ctk.CTkEntry(self.entry_frame, placeholder_text="6.58")
        self.temperature.grid(row=0, column=1, padx=5, pady=(0, 3), sticky="ew")

        # Humidity
        self.humidity_label = ctk.CTkLabel(self.entry_frame, text=dictionery[self.language]["humidity"], anchor="w")
        self.humidity_label.grid(row=1, column=0, padx=2, pady=0, sticky="w")  
        self.humidity = ctk.CTkEntry(self.entry_frame, placeholder_text="77.5")
        self.humidity.grid(row=1, column=1, padx=5, pady=(0, 3), sticky="ew")  


        # Wind Speed
        self.wind_speed_label = ctk.CTkLabel(self.entry_frame, text=dictionery[self.language]["wind_speed"], anchor="w")
        self.wind_speed_label.grid(row=2, column=0, padx=2, pady=0, sticky="w")
        self.wind_speed = ctk.CTkEntry(self.entry_frame, placeholder_text="0.077")
        self.wind_speed.grid(row=2, column=1, padx=5, pady=(0, 3), sticky="ew")

        # General Diffuse Flows
        self.general_diffuse_flows_label = ctk.CTkLabel(self.entry_frame, text=dictionery[self.language]["general_flows"], anchor="w")
        self.general_diffuse_flows_label.grid(row=3, column=0, padx=2, pady=0, sticky="w")
        self.general_diffuse_flows = ctk.CTkEntry(self.entry_frame, placeholder_text="208.8")
        self.general_diffuse_flows.grid(row=3, column=1, padx=5, pady=(0, 3), sticky="ew")

        # Diffuse Flows
        self.diffuse_flows_label = ctk.CTkLabel(self.entry_frame, text=dictionery[self.language]["flows"], anchor="w")
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

        self.zone_1 = ctk.CTkCheckBox(self.checkbox_frame, variable=self.zone_1_var, text=dictionery[self.language]["zone_one"])
        self.zone_1.grid(row=1, column=0, padx=20, pady=2, sticky="w")

        self.zone_2 = ctk.CTkCheckBox(self.checkbox_frame, variable=self.zone_2_var, text=dictionery[self.language]["zone_two"])
        self.zone_2.grid(row=2, column=0, padx=20, pady=2, sticky="w")

        self.zone_3 = ctk.CTkCheckBox(self.checkbox_frame, variable=self.zone_3_var, text=dictionery[self.language]["zone_three"])
        self.zone_3.grid(row=3, column=0, padx=20, pady=2, sticky="w")

            
        self.predict_button = ctk.CTkButton(self.center_frame,  height=37,  text=dictionery[self.language]["predict_button"],
                                             font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                             command=self.predict)
        self.predict_button.grid(row=2, column=0, columnspan=2, pady=7, padx=7)

        self.label_frame = ctk.CTkFrame(self)
        self.label_frame.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")
        self.result_label = ctk.CTkLabel(self.label_frame, fg_color=["#F7F7F7", "gray17"], wraplength= 500, text=dictionery[self.language]["result"])
        self.result_label.grid(row=0, column=0, padx=10, pady=10)
                
        #graph 
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.grid(row=3, column=1, pady=20, padx=20, sticky="nsew")
        
        #graph Matplotlib example
        self.fig = Figure(figsize=(5, 5), dpi=100)

        # Добавление subplot
        self.plot1 = self.fig.add_subplot(1, 1, 1)

        # Данные для графика
        x = [1, 2, 3, 4]
        y1 = [10, 20, 25, 30] 
        y2 = [5, 15, 22, 27]   
        y3 = [2, 10, 18, 26]   

        # Построение графиков
        self.plot1.plot(x, y1, label="Zone 1", color="#66CAB3")
        self.plot1.plot(x, y2, label="Zone 2", color="#404040")
        self.plot1.plot(x, y3, label="Zone 3", color="#21F6D2")

        # Легенда
        self.plot1.legend()

        # Создание FigureCanvasTkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()

        # Размещение холста на окне
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Растягиваем graph_frame, чтобы холст заполнил всё пространство
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)

        #
        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")
        self.info_label.insert("1.0", dictionery[self.language]["info_text"])
        self.info_label.configure(state="disabled")
        self.update_texts()

        

    def update_texts(self):
    # Обновляем текст всех элементов в интерфейсе
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

            self.info_label.configure(state="normal")  # Разрешите редактирование
            self.info_label.delete("1.0", "end")  # Очистка старого текста
            self.info_label.insert("1.0", dictionery[self.language]["info_text"])  # Вставка нового текста
            self.info_label.configure(state="disabled")  # Запретите редактирование

    def change_language(self, new_language):
        self.language = new_language
        self.update_texts()

    

    def check_number_format(self):
        pattern = r"^\d{1,3}([.]\d{1,3})?$"

        fields = {
            "temperature": (self.temperature.get(), "Temperature"),
            "wind_speed": (self.wind_speed.get(), "Wind Speed (m/s)"),
            "general_diffuse_flows": (self.general_diffuse_flows.get(), "General Diffuse Flows"),
            "diffuse_flows": (self.diffuse_flows.get(), "Diffuse Flows"),
        }

        for field_name, (value, label) in fields.items():
            if not value.strip():
                messagebox.showerror(
                    "ERROR",
                    message=f"The \"{label}\" field is empty. Please enter a value."
                )
                return
            
            if not re.match(pattern, value):
                messagebox.showerror(
                    "ERROR",
                    message=f"The input value in the \"{label}\" field does not match the pattern."
                )
                return 
            
        print("The values are correct")


    # def slider_event(self, value):
    #     self.humidity_label.configure(text=f"Humidity: {value:.0f}%")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("Sidebar button clicked")


    ############### Event handler для кнопки предикшина
    def predict(self):
        try:
            data = {
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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

        # Отправка данных на API
        try:
            response = requests.post("http://localhost:8000/predict", json=data)
            response.raise_for_status()
            result = response.json()
            self.result_label.configure(text=f"{dictionery[self.language]['result']} {result}")
        except requests.RequestException as e:
            messagebox.showerror("API Error", f"Failed to fetch prediction: {e}")

    def get_target_zones(self):
        zones = []
        if self.zone_1_var.get():
            zones.append(1)
        if self.zone_2_var.get():
            zones.append(2)
        if self.zone_3_var.get():
            zones.append(3)
        return zones

if __name__ == "__main__":
    app = App()
    app.mainloop()
