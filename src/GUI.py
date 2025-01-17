import tkinter
import tkinter.messagebox
import customtkinter as ctk
from PIL import Image, ImageTk 

ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("src\hemes\ed.json")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("SUML PowerCast.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.left_menu = ctk.CTkFrame(self, width=140)
        self.left_menu.grid(row=0, column=0, rowspan=5, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.left_menu.grid_rowconfigure(4, weight=1)

        self.dowload_button = ctk.CTkButton(self.left_menu, height=37, text="Dowload CSV", font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), command=self.sidebar_button_event)
        self.dowload_button.grid(row=0, column=0, padx=20, pady=20)
        self.train_button = ctk.CTkButton(self.left_menu, height=37, text="Train model", font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), command=self.sidebar_button_event)
        self.train_button.grid(row=1, column=0, padx=20, pady=10)

        self.language_mode_label = ctk.CTkLabel(self.left_menu, text="Language:", anchor="w")
        self.language_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.language_mode_optionemenu = ctk.CTkOptionMenu(self.left_menu, values=["PL", "ENG", "RU"], font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                                           command=self.change_appearance_mode_event)
        self.language_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_label = ctk.CTkLabel(self.left_menu, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.left_menu, values=["Light", "Dark", "System"], font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                                           command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        self.scaling_label = ctk.CTkLabel(self.left_menu, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.left_menu, values=["80%", "90%", "100%", "110%", "120%"], font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                                                     command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=10)

        # Load background image
        self.my_background_image = Image.open(r"src/Assets/background.jpg")

        # Resize the image to fit the window size while maintaining aspect ratio
        self.background_resized = self.my_background_image.resize((1100, 580), Image.Resampling.LANCZOS)  # Заменено на LANCZOS

        # Convert the image to a format Tkinter can use
        self.my_background = ImageTk.PhotoImage(self.background_resized)

        # Create label for background image using grid
        self.background_label = ctk.CTkLabel(self, image=self.my_background, corner_radius=21)
        self.background_label.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.background_label.grid_columnconfigure(0, weight=1)
        self.background_label.grid_rowconfigure(0, weight=1)

        # Create the layout for the three rows inside background_label
        self.row1_radio_button1 = ctk.CTkRadioButton(self.background_label, text="Option 1", value=1)
        self.row1_radio_button1.grid(row=0, column=0, padx=20, pady=10)


        self.temperature_label = ctk.CTkLabel(self.background_label, text="Temperature", font=ctk.CTkFont(size=16, weight="bold"))
        self.temperature_label.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        self.temperature_entry = ctk.CTkEntry(self.background_label)
        self.temperature_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        self.submit_button = ctk.CTkButton(self.background_label, text="Submit", command=self.sidebar_button_event)
        self.submit_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")

    def open_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

if __name__ == "__main__":
    app = App()
    app.mainloop()
