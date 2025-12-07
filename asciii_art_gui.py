import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import webbrowser
import os
import sys

# --- Configuration & Constants ---
APP_VERSION = "1.0.1"
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class ASCIIArtApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- ICON SETUP ---
        # This applies the icon to the main window and taskbar
        try:
            icon_path = resource_path("icon.ico")
            self.iconbitmap(icon_path)
        except Exception:
            pass # Use default if icon is missing

        # Window Setup
        self.title(f"MeyTiii's ASCII Art Generator (v{APP_VERSION})")
        self.geometry("900x700")
        
        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Header Section ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.title_label = ctk.CTkLabel(self.header_frame, text="🎨 Image to ASCII Converter", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(side="left", padx=20, pady=10)

        self.browse_button = ctk.CTkButton(self.header_frame, text="Browse Image", command=self.load_image, font=ctk.CTkFont(weight="bold"))
        self.browse_button.pack(side="right", padx=20, pady=10)

        # --- Main Display Section ---
        self.textbox = ctk.CTkTextbox(self, font=("Courier New", 12))
        self.textbox.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        self.textbox.insert("0.0", "\n\n      Please select an image to generate ASCII art...")
        self.textbox.configure(state="disabled")

        # --- Footer Section ---
        self.footer_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.help_button = ctk.CTkButton(self.footer_frame, text="Help / About", command=self.show_help, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.help_button.pack(side="left")

        self.copy_button = ctk.CTkButton(self.footer_frame, text="Copy to Clipboard", command=self.copy_to_clipboard, state="disabled")
        self.copy_button.pack(side="right")

    # --- Logic ---

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.webp")]
        )

        if not file_path:
            return

        try:
            image = Image.open(file_path)
            ascii_art = self.convert_to_ascii(image)
            self.display_art(ascii_art)
            self.copy_button.configure(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"Could not process image.\nReason: {e}")

    def convert_to_ascii(self, image, new_width=100):
        width, height = image.size
        aspect_ratio = height / width / 1.65
        new_height = int(new_width * aspect_ratio)
        resized_image = image.resize((new_width, new_height))
        
        grayscale_image = resized_image.convert("L")
        
        chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
        pixels = grayscale_image.getdata()
        new_pixels = [chars[pixel // 25] for pixel in pixels]
        new_pixels = "".join(new_pixels)
        
        pixel_count = len(new_pixels)
        ascii_image = "\n".join([new_pixels[index:(index + new_width)] for index in range(0, pixel_count, new_width)])
        return ascii_image

    def display_art(self, art):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", art)
        self.textbox.configure(state="disabled")

    def copy_to_clipboard(self):
        art = self.textbox.get("0.0", "end")
        self.clipboard_clear()
        self.clipboard_append(art)
        messagebox.showinfo("Success", "ASCII Art copied to clipboard!")

    def show_help(self):
        help_window = ctk.CTkToplevel(self)
        help_window.title("About")
        help_window.geometry("400x300")
        help_window.attributes("-topmost", True)
        
        # --- Apply Icon to Popup too ---
        try:
            help_window.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass
        # -------------------------------

        label = ctk.CTkLabel(help_window, text="Made by MeyTiii", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=(30, 5))

        version_label = ctk.CTkLabel(help_window, text=f"Version {APP_VERSION}", text_color="gray50")
        version_label.pack(pady=(0, 10))

        sub_label = ctk.CTkLabel(help_window, text="If you enjoyed, visit my GitHub and drop a star!", text_color="gray70")
        sub_label.pack(pady=5)

        link_button = ctk.CTkButton(help_window, text="🔗 github.com/meytiii/img-to-ascii-cli", 
                                    command=lambda: webbrowser.open("https://github.com/meytiii/img-to-ascii-cli"),
                                    fg_color="transparent", text_color="#3B8ED0", hover_color="#141414")
        link_button.pack(pady=20)

if __name__ == "__main__":
    app = ASCIIArtApp()
    app.mainloop()
