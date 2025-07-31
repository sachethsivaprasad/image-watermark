import tkinter as tk
from tkinter import filedialog, simpledialog

from PIL import Image, ImageDraw, ImageFont, ImageTk

LABEL_FONT = ("Courier", 40, "bold")
BUTTON_FONT = ("Courier", 20, "bold")

BG_COLOR = "#DFFFE1"
TEXT_COLOR = "#F48FB1"

BUTTON_BG_COLOR = "#C8E6C9"
BUTTON_TEXT_COLOR = "#AD1457"

WATERMARK_TEXT_COLOR = "#ffffff"
WATERMARK_TEXT_FONTSIZE = 40

MAX_IMG_WIDTH = 500
MAX_IMG_HEIGHT = 500


class Watermark:
    def __init__(self):
        # variables
        self.current_img = None
        self.add_text_btn = None
        self.add_logo_btn = None
        self.save_btn = None
        self.img_format = None
        self.watermark_added = False

        # main window
        self.window = tk.Tk()
        self.window.state(newstate="zoomed")
        self.window.title("Image Watermarking App")
        self.window.config(padx=100, pady=50, bg=BG_COLOR)
        self.window.grid_columnconfigure(0, weight=1)

        # title of the window
        self.title_label = tk.Label(
            text="Add custom watermarks to your images",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=LABEL_FONT,
        )
        self.title_label.grid(row=0, column=0, pady=20)

        # button to import image
        self.import_btn = tk.Button(
            text="Import Image",
            command=self.import_img,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR,
            font=BUTTON_FONT,
            highlightthickness=0,
        )
        self.import_btn.grid(row=1, column=0)

        # canvas to show the image
        self.canvas = tk.Canvas(
            width=600, height=400, bg=BG_COLOR, highlightthickness=0
        )
        self.canvas.grid(row=2, column=0, pady=(20, 20))

        # run the tkinter app indefinetely
        self.window.mainloop()

    def import_img(self):
        self.watermark_added = False

        img_path = filedialog.askopenfilename(
            title="Select an image (.jpeg, .jpg, .png)",
            filetypes=[
                ("Image files", ("*.jpeg", "*.jpg", "*.png")),
                ("All files", "."),
            ],
        )
        if img_path:
            self.current_img = Image.open(img_path)
            self.img_format = self.current_img.format
            self.display_img()

    def display_img(self):
        if self.current_img:
            self.canvas.delete("all")

            img_w, img_h = self.current_img.size

            ratio = min(MAX_IMG_WIDTH / img_w, MAX_IMG_HEIGHT / img_h)
            new_size = (int(img_w * ratio), int(img_h * ratio))

            img = self.current_img.resize(new_size)
            tk_img = ImageTk.PhotoImage(img)

            self.canvas.config(width=new_size[0], height=new_size[1])
            self.canvas.create_image(0, 0, anchor="nw", image=tk_img)
            self.canvas.img = tk_img

            if self.watermark_added:
                self.display_save_button()
            else:
                self.display_add_buttons()

    def display_add_buttons(self):
        if self.save_btn:
            self.save_btn.destroy()
            self.save_btn = None

        btn_frame = tk.Frame(bg=BG_COLOR)
        btn_frame.grid(row=3, column=0, pady=20)

        self.add_text_btn = tk.Button(
            btn_frame,
            text="Add text",
            command=self.add_text,
            font=BUTTON_FONT,
            highlightthickness=0,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR,
        )
        self.add_text_btn.pack(side="left", padx=10)

        self.add_logo_btn = tk.Button(
            btn_frame,
            text="Add logo",
            command=self.add_logo,
            font=BUTTON_FONT,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR,
            highlightthickness=0,
        )
        self.add_logo_btn.pack(side="right", padx=10)

    def display_save_button(self):
        if self.add_text_btn:
            self.add_text_btn.destroy()
            self.add_text_btn = None
        if self.add_logo_btn:
            self.add_logo_btn.destroy()
            self.add_logo_btn = None

        self.save_btn = tk.Button(
            text="Save image",
            command=self.save_img,
            font=BUTTON_FONT,
            bg=BUTTON_BG_COLOR,
            fg=BUTTON_TEXT_COLOR,
            highlightthickness=0,
        )
        self.save_btn.grid(row=3, column=0, pady=20)

    def add_text(self):
        text = simpledialog.askstring(
            title="Watermark Text", prompt="Enter the text to add as watermark"
        )

        if text and self.current_img:
            draw = ImageDraw.Draw(self.current_img)
            font = ImageFont.truetype("arial.ttf", WATERMARK_TEXT_FONTSIZE)
            position = (self.current_img.width - 300, self.current_img.height - 200)

            draw.text(xy=position, text=text, fill=WATERMARK_TEXT_COLOR, font=font)

            self.watermark_added = True
            self.display_img()

    def add_logo(self):
        logo_path = filedialog.askopenfilename(
            title="Select a logo",
            filetypes=[
                ("Image files", ("*.jpeg", "*.jpg", "*.png")),
                ("All files", "."),
            ],
        )

        if logo_path and self.current_img:
            logo_img = Image.open(logo_path)

            max_logo_size = (self.current_img.width // 8, self.current_img.height // 8)
            logo_img.thumbnail(max_logo_size)

            position = (
                self.current_img.width - logo_img.width - 100,
                self.current_img.height - logo_img.height - 100,
            )
            self.current_img.paste(logo_img, position)

            self.watermark_added = True
            self.display_img()

    def save_img(self):
        if self.watermark_added and self.current_img and self.img_format:
            extension = (
                "jpg" if self.img_format.upper() == "JPEG" else self.img_format.lower()
            )
            self.current_img.save(
                f"watermarked_image.{extension.lower()}", format=self.img_format.upper()
            )


if __name__ == "__main__":
    Watermark()