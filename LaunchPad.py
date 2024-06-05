import os
import customtkinter
import subprocess as sub
from PIL import Image

# Get the user's profile directory
user_profile = os.environ['USERPROFILE']
    
# Specify the wifi folder name as a variable
app_name = 'GSNAPX'
    
# Construct the full path
directory = os.path.join(user_profile, 'Desktop', app_name)

class MyLogoFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, logo_path):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.logo_path = logo_path

        self.title_label = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        # Create a frame to hold the logo and the label
        self.logo_frame = customtkinter.CTkFrame(self)
        self.logo_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")      

        # Load and place the logo inside the logo_frame
        self.logo = customtkinter.CTkImage(Image.open(self.logo_path), size=(200, 140))
        self.logo_label = customtkinter.CTkLabel(self.logo_frame, image=self.logo, text="")
        self.logo_label.grid(row=2, column=2, padx=(10, 0), pady=(30, 50), sticky="nsew")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("GSnapX")
        self.geometry("300x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.logo_frame = MyLogoFrame(self, "PHOTO ID SOLUTION", logo_path="./img/launchpad_logo.png")
        self.logo_frame.grid(row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")      

        self.button_1 = customtkinter.CTkButton(self, text="PHOTO ID Package-A", text_color='black', font=('Arial', 15), height=45, fg_color="#27cfcf", hover_color="#1c8989", command=self.pid_pkg1)
        self.button_1.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.button_2 = customtkinter.CTkButton(self, text="PHOTO ID Package-B", text_color='black', font=('Arial', 15), height=45, fg_color="#27cfcf", hover_color="#1c8989", command=self.pid_pkg2)
        self.button_2.grid(row=2, column=0, padx=10, pady=5, sticky="ew")        

        self.button_3 = customtkinter.CTkButton(self, text="PHOTO ID Package-C", text_color='black', font=('Arial', 15), height=45, fg_color="#27cfcf", hover_color="#1c8989", command=self.pid_pkg3)
        self.button_3.grid(row=3, column=0, padx=10, pady=5, sticky="ew")        

        self.button_4 = customtkinter.CTkButton(self, text="PHOTO ID Package-D", text_color='black', font=('Arial', 15), height=45, fg_color="#27cfcf", hover_color="#1c8989", command=self.pid_pkg4)
        self.button_4.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        
        self.button_5 = customtkinter.CTkButton(self, text="PHOTO ID Package-E", text_color='black', font=('Arial', 15), height=45, fg_color="#27cfcf", hover_color="#1c8989", command=self.pid_pkg5)
        self.button_5.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        # Footer
        self.footer_frame = customtkinter.CTkFrame(self)
        self.footer_frame.grid(row=6, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.footer_label = customtkinter.CTkLabel(self.footer_frame, 
                                                   text="\nCopyright © 2024 Toto's Digital Services Ltd. \nAll rights reserved. \n",
                                                   font=("Arial", 9))
        self.footer_label.pack()

    def pid_pkg1(self):
        sub.run(["python", "PHOTOIDPKG1.py"])        

    def pid_pkg2(self):
        sub.run(["python", "PHOTOIDPKG2.py"])

    def pid_pkg3(self):
        sub.run(["python", "PHOTOIDPKG3.py"]) 

    def pid_pkg4(self):
        sub.run(["python", "PHOTOIDPKG4.py"])        

    def pid_pkg5(self):
        sub.run(["python", "PHOTOIDPKG5.py"])

app = App()
app.mainloop()
