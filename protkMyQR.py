import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
from DrissionPage import ChromiumPage, ChromiumOptions
import os

def generate_qr():
    text = text_entry.get()
    if not text:
        messagebox.showerror("错误", "请输入内容！")
        return

    logo_path = logo_path_var.get()
    background_path = bg_path_var.get()

    try:
        co = ChromiumOptions().set_paths(browser_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe').headless()
        page = ChromiumPage(co)
        page.get('https://www.easyproject.cn/easyqrcodejs/tryit.html')

        text_area = page.ele('tag:textarea@@name:text')
        text_area.clear()
        text_area.input(text)

        # Only input logo if a path is provided
        if logo_path:
            page.ele('tag:input@@id=logo').input(logo_path)

        # Only input background image if a path is provided
        if background_path:
            page.ele('tag:input@@id=backgroundImage').input(background_path)

        page.ele('tag:button@@id=generatorBtn').click()

        # Get current time and format it as filename
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_path = f'qrcode_{current_time}.png'

        # Save QR code screenshot
        page.ele('tag:canvas').get_screenshot(path=image_path)

        # Display the generated QR code image
        display_image(image_path)

        messagebox.showinfo("恭喜", f"'{image_path}生成并保存成功'")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误: {e}，请反馈给开发者！")

def select_logo():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
    if path:
        logo_path_var.set(path)

def select_background():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
    if path:
        bg_path_var.set(path)

def display_image(image_path):
    """Displays the generated QR code image."""
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((200, 200), Image.LANCZOS)  # Resize for display
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk

# Create the main window
root = tk.Tk()
root.title("二维码生成器")

# Text input
tk.Label(root, text="二维码内容:").grid(row=0, column=0, padx=10, pady=10)
text_entry = tk.Entry(root, width=40)
text_entry.grid(row=0, column=1, padx=10, pady=10)

# Logo image selection (optional)
tk.Label(root, text="选择Logo（可选）:").grid(row=1, column=0, padx=10, pady=10)
logo_path_var = tk.StringVar()
logo_entry = tk.Entry(root, textvariable=logo_path_var, width=30)
logo_entry.grid(row=1, column=1, padx=10, pady=10)
logo_button = tk.Button(root, text="Logo文件", command=select_logo)
logo_button.grid(row=1, column=2, padx=10, pady=10)

# Background image selection (optional)
tk.Label(root, text="选择底图（可选）:").grid(row=2, column=0, padx=10, pady=10)
bg_path_var = tk.StringVar()
bg_entry = tk.Entry(root, textvariable=bg_path_var, width=30)
bg_entry.grid(row=2, column=1, padx=10, pady=10)
bg_button = tk.Button(root, text="底图文件", command=select_background)
bg_button.grid(row=2, column=2, padx=10, pady=10)

# Generate button
generate_button = tk.Button(root, text="二维码生成", command=generate_qr)
generate_button.grid(row=3, column=1, pady=20)

# Label to display the generated image
img_label = tk.Label(root)
img_label.grid(row=4, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()
