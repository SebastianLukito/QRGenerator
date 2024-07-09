import qrcode
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox, font, ttk
import threading
import re
import sys
import os
from pyzbar.pyzbar import decode

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Unified Numeric Tagging Utility Labeler (QUNTUL)")
        icon_path = self.resource_path('icon.ico')
        self.root.iconbitmap(icon_path)
        self.root.geometry("810x560")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(False, False)
        self.create_widgets()
        self.display_placeholder_qr()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def create_widgets(self):
        # Define dark mode colors
        bg_color = "#1a1a1a"
        fg_color = "#e0e0e0"
        button_bg_color = "#333333"
        button_fg_color = "#e0e0e0"
        entry_bg_color = "#262626"
        entry_fg_color = "#e0e0e0"

        # Title Font
        title_font = font.Font(family='Helvetica', size=20, weight='bold')
        label_font = font.Font(family='Helvetica', size=12)
        button_font = font.Font(family='Helvetica', size=10, weight='bold')

        # Marquee Text
        self.marquee_text = "Quick Unified Numeric Tagging Utility Labeler (QUNTUL) Quick Unified Numeric Tagging Utility Labeler (QUNTUL) "
        self.marquee_label = tk.Label(self.root, text=self.marquee_text, font=title_font, bg="#000000", fg="#e0e0e0")
        self.marquee_label.pack(pady=0, padx=20, fill='x', expand=True, anchor='center')
        self.update_marquee()

        # Main Frame
        self.main_frame = tk.Frame(self.root, bg=bg_color)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=0)

        # Left Frame for Inputs and Buttons
        self.left_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.left_frame.grid(row=0, column=0, sticky='n', padx=10, pady=5)

        # Input Data Frame
        self.data_frame = tk.LabelFrame(self.left_frame, text="Enter URL Here", font=label_font, bg=bg_color, fg=fg_color, padx=10, pady=10)
        self.data_frame.grid(row=0, column=0, sticky='ew', pady=5)

        self.data_label = tk.Label(self.data_frame, text="URL:", font=label_font, bg=bg_color, fg=fg_color)
        self.data_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.data_entry = tk.Entry(self.data_frame, width=50, bg=entry_bg_color, fg=entry_fg_color, insertbackground=fg_color)
        self.data_entry.grid(row=0, column=1, padx=5, pady=5)

        # Logo Selection Frame
        self.logo_frame = tk.LabelFrame(self.left_frame, text="Upload Logo", font=label_font, bg=bg_color, fg=fg_color, padx=10, pady=10)
        self.logo_frame.grid(row=1, column=0, sticky='ew', pady=5)

        self.logo_button = tk.Button(self.logo_frame, text="Select Logo", command=self.select_logo, font=button_font, bg=button_bg_color, fg=button_fg_color)
        self.logo_button.grid(row=0, column=0, padx=5, pady=5)
        self.logo_path_label = tk.Label(self.logo_frame, text="No logo selected", font=label_font, bg=bg_color, fg=fg_color)
        self.logo_path_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Logo Size entry
        self.logo_size_label = tk.Label(self.logo_frame, text="Logo Size (1-10):", font=label_font, bg=bg_color, fg=fg_color)
        self.logo_size_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.logo_size_entry = tk.Entry(self.logo_frame, width=5, bg=entry_bg_color, fg=entry_fg_color, insertbackground=fg_color)
        self.logo_size_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.logo_size_entry.insert(0, "4")  # Default logo size value

        # Padding entry
        self.padding_label = tk.Label(self.logo_frame, text="Padding:", font=label_font, bg=bg_color, fg=fg_color)
        self.padding_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.padding_entry = tk.Entry(self.logo_frame, width=5, bg=entry_bg_color, fg=entry_fg_color, insertbackground=fg_color)
        self.padding_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.padding_entry.insert(0, "10")  # Default padding value

        # Loading Bar
        self.progress = ttk.Progressbar(self.logo_frame, orient="horizontal", length=200, mode="indeterminate")
        self.progress.grid(row=3, column=0, columnspan=2, pady=10)

        # QR Complexity Selection
        self.complexity_frame = tk.LabelFrame(self.left_frame, text="QR Code Complexity", font=label_font, bg=bg_color, fg=fg_color, padx=10, pady=10)
        self.complexity_frame.grid(row=2, column=0, sticky='ew', pady=5)

        self.complexity_label = tk.Label(self.complexity_frame, text="Complexity (1-40):", font=label_font, bg=bg_color, fg=fg_color)
        self.complexity_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.complexity_entry = tk.Entry(self.complexity_frame, width=5, bg=entry_bg_color, fg=entry_fg_color, insertbackground=fg_color)
        self.complexity_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.complexity_entry.insert(0, "10")  # Default complexity value

        # Generate QR Code Button
        self.generate_button = tk.Button(self.left_frame, text="Generate QR Code", command=self.generate_qr_code, font=button_font, bg=button_bg_color, fg=button_fg_color)
        self.generate_button.grid(row=3, column=0, pady=5, sticky='ew')

        # Save QR Code Button
        self.save_button = tk.Button(self.left_frame, text="Save QR Code", command=self.save_qr_code, font=button_font, bg=button_bg_color, fg=button_fg_color)
        self.save_button.grid(row=4, column=0, pady=5, sticky='ew')

        # New QR Code Button
        self.new_qr_button = tk.Button(self.left_frame, text="New QR Code", command=self.reset, font=button_font, bg=button_bg_color, fg=button_fg_color)
        self.new_qr_button.grid(row=5, column=0, pady=5, sticky='ew')

        # Right Frame for QR Code Display
        self.right_frame = tk.LabelFrame(self.main_frame, text="QR Code", font=label_font, bg=bg_color, fg=fg_color, padx=10, pady=10)
        self.right_frame.grid(row=0, column=1, sticky='n', padx=10, pady=5)

        # QR Code Display Frame
        self.qr_frame = tk.Frame(self.right_frame, bg=bg_color)
        self.qr_frame.pack(padx=5, pady=5)
        self.qr_label = tk.Label(self.qr_frame, bg=bg_color)
        self.qr_label.pack()
        
        # Footer Label
        self.footer_label = tk.Label(self.right_frame, text="Sebastianus Lukito 2024", font=label_font, bg=bg_color, fg=fg_color)
        self.footer_label.pack(pady=(10, 0))

    def update_marquee(self):
        text = self.marquee_text
        self.marquee_text = text[1:] + text[0]
        self.marquee_label.config(text=self.marquee_text)
        self.root.after(100, self.update_marquee)

    def select_logo(self):
        def load_logo():
            self.progress.start()
            self.logo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if self.logo_path:
                short_path = self.shorten_path(self.logo_path, max_length=25)
                self.logo_path_label.config(text=short_path)
            self.progress.stop()
            self.progress.grid_remove()
        
        self.progress.grid()
        threading.Thread(target=load_logo).start()

    def shorten_path(self, path, max_length):
        if len(path) > max_length:
            return path[:max_length//2] + "..." + path[-max_length//2:]
        return path

    def validate_data(self, data):
        # Example validation: check if data is a valid URL
        url_pattern = re.compile(
            r'^(https?:\/\/)?'  # http:// atau https://
            r'(([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,6}'  # domain
            r'(:\d+)?(\/[-a-z\d%_.~+]*)*'  # optional port dan path
            r'(\?[;&a-z\d%_.~+=-]*)?'  # query string
            r'(\#[-a-z\d_]*)?$', re.IGNORECASE)  # fragment locator
        
        return re.match(url_pattern, data) is not None

    def generate_qr_code(self):
        data = self.data_entry.get()
        if not data:
            messagebox.showerror("Error", "Please enter a URL.")
            return
        
        if not self.validate_data(data):
            messagebox.showerror("Error", "Invalid URL. Please enter a valid URL.")
            return

        logo_path = getattr(self, 'logo_path', None)
        logo_size_factor = int(self.logo_size_entry.get())

        while logo_size_factor >= 1:
            qr_img, original_qr_img = self.create_qr_code(data, logo_path, logo_size_factor)
            if self.scan_qr_code(qr_img):
                self.display_qr_code(qr_img)
                self.original_qr_img = original_qr_img  # Save original QR code image for saving later
                return
            else:
                logo_size_factor -= 1
                self.logo_size_entry.delete(0, tk.END)
                self.logo_size_entry.insert(0, str(logo_size_factor))
                messagebox.showwarning("Warning", f"QR code not scannable with current logo size. Trying with smaller logo size: {logo_size_factor}")

        messagebox.showerror("Error", "QR code not scannable. Please try a different logo or URL.")

    def create_qr_code(self, data, logo_filename, logo_size_factor):
        complexity = int(self.complexity_entry.get())  # Get complexity value from entry
        qr = qrcode.QRCode(
            version=complexity,  # Increase version for more complexity
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img_qr = qr.make_image(fill='black', back_color='white').convert('RGB')

        # Tambahkan saluran alpha ke img_qr
        img_qr = img_qr.convert('RGBA')
        datas = img_qr.getdata()

        newData = []
        for item in datas:
            if item[:3] == (255, 255, 255):  # Ganti warna putih menjadi transparan
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img_qr.putdata(newData)

        # Membuat sudut melingkar pada QR code
        rounded_qr = Image.new('RGBA', img_qr.size)
        draw = ImageDraw.Draw(rounded_qr)
        radius = 20  # radius for rounded corners
        draw.rounded_rectangle([0, 0, img_qr.size[0], img_qr.size[1]], radius, fill="white")
        rounded_qr.paste(img_qr, mask=img_qr)

        if logo_filename:
            logo = Image.open(logo_filename).convert("RGBA")
            padding = int(self.padding_entry.get())  # Get padding value from entry
            logo_ratio = logo.width / logo.height
            # Invers ukuran logo
            logo_size = (img_qr.size[0] // (11 - logo_size_factor), int((img_qr.size[0] // (11 - logo_size_factor)) / logo_ratio))
            logo = logo.resize(logo_size, Image.LANCZOS)

            # Create a white box with padding and rounded corners behind the logo
            padded_logo_size = (logo_size[0] + 2 * padding, logo_size[1] + 2 * padding)
            mask = Image.new('L', padded_logo_size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([(0, 0), padded_logo_size], radius=20, fill=255)

            logo_box = Image.new('RGBA', padded_logo_size, (255, 255, 255, 255))
            logo_box.paste(logo, (padding, padding), mask=logo)

            pos = ((img_qr.size[0] - padded_logo_size[0]) // 2, (img_qr.size[1] - padded_logo_size[1]) // 2)
            rounded_qr.paste(logo_box, pos, mask=mask)

        # Save the original QR code image
        original_qr_img = rounded_qr.copy()

        # Resize QR code to fit the display frame
        qr_display_size = 300  # Example size, adjust as needed
        rounded_qr = rounded_qr.resize((qr_display_size, qr_display_size), Image.LANCZOS)

        return rounded_qr, original_qr_img


    def scan_qr_code(self, qr_img):
        decoded_objects = decode(qr_img)
        return len(decoded_objects) > 0

    def display_qr_code(self, qr_img):
        self.qr_imgtk = ImageTk.PhotoImage(qr_img)
        self.qr_label.config(image=self.qr_imgtk)

    def display_placeholder_qr(self):
        # Create a blank gray image
        placeholder_size = 300  # Example size, adjust as needed
        placeholder_qr = Image.new('RGB', (placeholder_size, placeholder_size), color='#1a1a1a')
        self.qr_imgtk = ImageTk.PhotoImage(placeholder_qr)
        self.qr_label.config(image=self.qr_imgtk)

    def save_qr_code(self):
        if hasattr(self, 'original_qr_img'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.original_qr_img.save(file_path)
                messagebox.showinfo("Success", f"QR code saved as {file_path}")
        else:
            messagebox.showerror("Error", "No QR code to save. Please generate a QR code first.")

    def reset(self):
        self.data_entry.delete(0, tk.END)
        self.logo_path_label.config(text="No logo selected")
        self.display_placeholder_qr()
        self.logo_path = None

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
