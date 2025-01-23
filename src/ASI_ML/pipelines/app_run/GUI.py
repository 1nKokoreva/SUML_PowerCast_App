import os
import re
import tkinter
import tkinter.messagebox as messagebox
import customtkinter as ctk
from PIL import Image, ImageTk 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

current_path = os.path.dirname(os.path.realpath(__file__))

ctk.set_appearance_mode("light") 
ctk.set_default_color_theme(current_path + "/Assets/own_theme.json")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

      

        self.title("PowerCast_App")
        self.iconbitmap(current_path +"/Assets/iconic.ico")
        self.geometry(f"{800}x{680}")
    
        self.grid_rowconfigure((0,1), weight=0)  
        self.grid_rowconfigure( 2, weight=1)  
        self.grid_columnconfigure(0, weight=0)  
        self.grid_columnconfigure((1, 2), weight=1) 
        #self.bg_image = ctk.CTkImage(Image.open(current_path + "/Assets/background.jpg"), size=(500, 250))
       
        # logo
        self.logo_image = ctk.CTkImage(light_image=Image.open(current_path + "/Assets/PowerCast.png"),dark_image=Image.open(current_path + "/Assets/PowerCast_white.png"), size=(380, 60))
        self.logo_label = ctk.CTkLabel(self,  image=self.logo_image, text="")
        self.logo_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="nw")

        # sidebar menu
        self.left_menu = ctk.CTkFrame(self, width=140)
        self.left_menu.grid(row=1, column=0, rowspan=3, padx=(20, 20), pady=(10, 20), sticky="nsew")
        self.left_menu.grid_rowconfigure(4, weight=1)

        self.download_button = ctk.CTkButton(self.left_menu, height=37, text="Download CSV",
                                             font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                             command=self.sidebar_button_event)
        self.download_button.grid(row=0, column=0, padx=20, pady=10)

        self.train_button = ctk.CTkButton(self.left_menu, height=37, text="Train model",
                                          font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                          command=self.sidebar_button_event)
        self.train_button.grid(row=1, column=0, padx=20, pady=10)

        self.language_mode_label = ctk.CTkLabel(self.left_menu, fg_color="transparent", text="Language:", anchor="w")
        self.language_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.language_mode_optionemenu = ctk.CTkOptionMenu(self.left_menu, values=["PL", "ENG", "RU"],
                                                           font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                                           command=self.change_appearance_mode_event)
        self.language_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_label = ctk.CTkLabel(self.left_menu, fg_color="transparent", text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.left_menu, values=["Light", "Dark"],
                                                             font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self.left_menu, fg_color="transparent", text="UI Scaling:", anchor="w")
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
        self.temperature_label = ctk.CTkLabel(self.entry_frame, text="Temperature:", anchor="w")
        self.temperature_label.grid(row=0, column=0, padx=2, pady=0, sticky="w")
        self.temperature = ctk.CTkEntry(self.entry_frame, placeholder_text="6.58")
        self.temperature.grid(row=0, column=1, padx=5, pady=(0, 3), sticky="ew")

        # Humidity
        self.humidity_label = ctk.CTkLabel(self.entry_frame, text="Humidity:", anchor="w")
        self.humidity_label.grid(row=1, column=0, padx=2, pady=0, sticky="w")  
        self.humidity = ctk.CTkEntry(self.entry_frame, placeholder_text="77.5")
        self.humidity.grid(row=1, column=1, padx=5, pady=(0, 3), sticky="ew")  


        # Wind Speed
        self.wind_speed_label = ctk.CTkLabel(self.entry_frame, text="Wind Speed(m/s):", anchor="w")
        self.wind_speed_label.grid(row=2, column=0, padx=2, pady=0, sticky="w")
        self.wind_speed = ctk.CTkEntry(self.entry_frame, placeholder_text="0.077")
        self.wind_speed.grid(row=2, column=1, padx=5, pady=(0, 3), sticky="ew")

        # General Diffuse Flows
        self.general_diffuse_flows_label = ctk.CTkLabel(self.entry_frame, text="General diffuse flows:", anchor="w")
        self.general_diffuse_flows_label.grid(row=3, column=0, padx=2, pady=0, sticky="w")
        self.general_diffuse_flows = ctk.CTkEntry(self.entry_frame, placeholder_text="208.8")
        self.general_diffuse_flows.grid(row=3, column=1, padx=5, pady=(0, 3), sticky="ew")

        # Diffuse Flows
        self.diffuse_flows_label = ctk.CTkLabel(self.entry_frame, text="Diffuse flows:", anchor="w")
        self.diffuse_flows_label.grid(row=4, column=0, padx=2, pady=0, sticky="w")
        self.diffuse_flows = ctk.CTkEntry(self.entry_frame, placeholder_text="35.29")
        self.diffuse_flows.grid(row=4, column=1, padx=5, pady=(0, 5), sticky="ew")
        
        
        # Zone selection
        self.checkbox_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent", border_width=0)
        self.checkbox_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")


        self.checkbox_label = ctk.CTkLabel(self.checkbox_frame, text="Select the necessary zones")
        self.checkbox_label.grid(row=0, column=0, padx=5, pady=0, sticky="n")

       
        #self.checkboxes["Zone 1"].get(), который вернёт 1 (активен) или 0 (неактивен).
        self.radio_var = tkinter.IntVar(value=1)
        self.checkboxes1 = ctk.CTkRadioButton(self.checkbox_frame, variable=self.radio_var, value=1, text="Zone 1")
        self.checkboxes1.grid(row=1, column=0, padx=20, pady=2, sticky="w")

        self.checkboxes2 = ctk.CTkRadioButton(self.checkbox_frame,  variable=self.radio_var, value=2, text="Zone 2")
        self.checkboxes2.grid(row=2, column=0, padx=20, pady=2, sticky="w")
 
        self.checkboxes3 = ctk.CTkRadioButton(self.checkbox_frame,  variable=self.radio_var, value=3, text="Zone 3")
        self.checkboxes3.grid(row=3, column=0, padx=20, pady=2, sticky="w")

        self.checkboxes4 = ctk.CTkRadioButton(self.checkbox_frame,  variable=self.radio_var, value=0, text="All")
        self.checkboxes4.grid(row=4, column=0, padx=20, pady=2, sticky="w")

            
        self.button = ctk.CTkButton(self.center_frame,  height=37,  text="Predict",
                                             font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                             command=self.check_number_format)
        self.button.grid(row=2, column=0, columnspan=2, pady=7, padx=7)

        #graph 
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.grid(row=2, column=1, pady=20, padx=40, sticky="nsew")
        
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
        self.info_label.insert("0.0", "Aplikacja umożliwia przewidywanie zużycia energii elektrycznej w gospodarstwie domowym na podstawie danych pogodowych i strefy docelowej. Dzięki temu użytkownicy mogą lepiej planować zużycie energii, optymalizować koszty oraz unikać przeciążeń w sieci energetycznej.")
        self.info_label.configure(state="disabled")

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

if __name__ == "__main__":
    app = App()
    app.mainloop()
