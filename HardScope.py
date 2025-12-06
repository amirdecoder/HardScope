import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import tempfile
import os


def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()


def refresh():
    txt.delete("1.0", tk.END)

    txt.insert(tk.END, "=== USB Devices (lsusb) ===\n")
    txt.insert(tk.END, run_cmd("lsusb") + "\n\n")

    txt.insert(tk.END, "=== PCI Devices (lspci) ===\n")
    txt.insert(tk.END, run_cmd("lspci") + "\n\n")

    txt.insert(tk.END, "=== Storage Devices (lsblk) ===\n")
    txt.insert(tk.END, run_cmd("lsblk -o NAME,MODEL,SIZE,TYPE") + "\n\n")



def print_info():

    content = txt.get("1.0", tk.END).strip()

    if not content:
        messagebox.showerror("Error", "هیچ اطلاعاتی برای پرینت وجود ندارد!")
        return


    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmpfile.write(content.encode("utf-8"))
    tmpfile.close()


    result = subprocess.run(f"lp {tmpfile.name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        messagebox.showinfo("Success", "پرینت با موفقیت ارسال شد.")
    else:
        messagebox.showerror("Print Error", f"خطا در پرینت:\n{result.stderr}")




win = tk.Tk()
win.title("Linux Hardware Viewer")
win.geometry("850x650")

btn_frame = tk.Frame(win)
btn_frame.pack(pady=5)

btn_refresh = ttk.Button(btn_frame, text="Refresh Hardware Info", command=refresh)
btn_refresh.grid(row=0, column=0, padx=5)

btn_print = ttk.Button(btn_frame, text="Print", command=print_info)
btn_print.grid(row=0, column=1, padx=5)

txt = tk.Text(win, font=("Courier", 10))
txt.pack(expand=True, fill="both")

refresh()

win.mainloop()
