import tkinter
import tkinter.messagebox
import customtkinter as ctk
from PIL import Image, ImageTk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("src\hemes\ed.json")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PowerCast")
        self.iconbitmap(r"src\Assets\iconic.ico")
        self.geometry("900x600")

        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure((1, 2), weight=1)  
        self.grid_columnconfigure(0, weight=0)  
        self.grid_columnconfigure((1, 2), weight=1) 

        # logo

        self.logo_image = ctk.CTkImage(light_image=Image.open(r"src/Assets/PowerCast.png"),dark_image=Image.open(r"src\Assets\PowerCast_white.png"), size=(380, 60))
        self.logo_label = ctk.CTkLabel(self, image=self.logo_image, text="")
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

        self.language_mode_label = ctk.CTkLabel(self.left_menu, text="Language:", anchor="w")
        self.language_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.language_mode_optionemenu = ctk.CTkOptionMenu(self.left_menu, values=["PL", "ENG", "RU"],
                                                           font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                                           command=self.change_appearance_mode_event)
        self.language_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_label = ctk.CTkLabel(self.left_menu, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.left_menu, values=["Light", "Dark"],
                                                             font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self.left_menu, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.left_menu, values=["80%", "90%", "100%", "110%", "120%"],
                                                     font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                                     command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=10)


        # Основная область
        self.background_label = ctk.CTkLabel(self, width=800, fg_color=["#72958F", "#72958F"], text="") #1290
        self.background_label.grid(row=1, column=1, padx=(40, 20), pady=(10, 20), sticky="nsew")
      

        self.info_label = ctk.CTkTextbox(self.background_label, fg_color="transparent")  
        self.info_label.grid(row=0, column=0, columnspan =1, padx=10, pady=10, sticky="new")

        # self.date_frame = ctk.CTkFrame(self.background_label)
        # self.date_frame.grid(row =2, column=0, padx=10, pady=10,sticky="nsew")

        # self.date_frame2 = ctk.CTkFrame(self.background_label)
        # self.date_frame2.grid(row =2, column=1, padx=10, pady=10, sticky="nsew")

        # self.temperature_label = ctk.CTkLabel(self.background_label, text="Temperature",
        #                                       font=ctk.CTkFont(size=16, weight="bold"))
        # self.temperature_label.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        # self.temperature_entry = ctk.CTkEntry(self.background_label)
        # self.temperature_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        # self.submit_button = ctk.CTkButton(self.background_label, text="Submit", command=self.sidebar_button_event)
        # self.submit_button.grid(row=1, column=0, columnspan=2, padx=20, pady=20)


        #graph 
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.grid(row=2, column=1, pady=(20, 20), padx=(40,20), sticky="nsew")
        
        #graph Matplotlib example
        # self.fig, self.ax = plt.subplots()
        # self.ax.plot([1, 2, 3, 4], [10, 20, 25, 30], label="Zone 1")  
        # self.ax.plot([1, 2, 3, 4], [5, 15, 22, 27], label="Zone 2")  
        # self.ax.plot([1, 2, 3, 4], [2, 10, 18, 26], label="Zone 3") 

        # self.ax.legend() 
        
    
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        # self.canvas.draw()

        # self.canvas.get_tk_widget().pack(padx=(20,20), pady=(20,20))


        #
        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")
        self.info_label.insert("0.0", "Aplikacja umożliwia przewidywanie zużycia energii elektrycznej w gospodarstwie domowym na podstawie danych pogodowych i strefy docelowej. Dzięki temu użytkownicy mogą lepiej planować zużycie energii, optymalizować koszty oraz unikać przeciążeń w sieci energetycznej.")


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
