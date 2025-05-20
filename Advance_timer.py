import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import time

BG = "#121212"
FG = "#e0e0e0"
ENTRY_BG = "#1e1e1e"
BTN_BG = "#2a2a2a"
BTN_HOVER = "#3a3a3a"
HIGHLIGHT = "#00ffc3"
FONT = ("Consolas", 12)
BIG_FONT = ("Consolas", 22, "bold")

timer_running = False
timer_thread = None
stop_event = threading.Event()

root = tk.Tk()
root.title("⚡ Cool Countdown Timer")
root.geometry("600x350")
root.configure(bg=BG)

title = tk.Label(root, text="🕒 Advanced Countdown Timer", font=("Consolas", 18, "bold"), fg=HIGHLIGHT, bg=BG)
title.pack(pady=10)

frame = tk.Frame(root, bg=BG)
frame.pack()

def create_labeled_entry(label, row, column, width=6):
    tk.Label(frame, text=label, font=FONT, fg=FG, bg=BG).grid(row=row, column=column, padx=5, pady=5, sticky="e")
    entry = tk.Entry(frame, width=width, font=FONT, bg=ENTRY_BG, fg=FG, insertbackground=FG, bd=1, relief="solid")
    entry.grid(row=row, column=column + 1, padx=5, pady=5)
    return entry

year_entry = create_labeled_entry("Year*", 0, 0)
month_entry = create_labeled_entry("Month*", 0, 2)
day_entry = create_labeled_entry("Day*", 0, 4)

hour_entry = create_labeled_entry("Hour", 1, 0)
minute_entry = create_labeled_entry("Minute", 1, 2)
second_entry = create_labeled_entry("Second", 1, 4)

tk.Label(frame, text="AM/PM", font=FONT, fg=FG, bg=BG).grid(row=2, column=0, padx=5, pady=5, sticky="e")
am_pm_var = tk.StringVar(value="AM")
am_pm_menu = tk.OptionMenu(frame, am_pm_var, "AM", "PM")
am_pm_menu.config(bg=ENTRY_BG, fg=FG, font=FONT, highlightbackground=BG, activebackground=BTN_HOVER)
am_pm_menu.grid(row=2, column=1, padx=5, pady=5)

time_label = tk.Label(root, text="", font=BIG_FONT, fg=HIGHLIGHT, bg=BG)
time_label.pack(pady=15)

def update_display(text):
    time_label.config(text=text)
    time_label.update()

def start_timer():
    global timer_thread, timer_running, stop_event
    try:
        year = int(year_entry.get())
        month = int(month_entry.get())
        day = int(day_entry.get())

        hour = int(hour_entry.get()) if hour_entry.get() else 12
        minute = int(minute_entry.get()) if minute_entry.get() else 0
        second = int(second_entry.get()) if second_entry.get() else 0

        am_pm = am_pm_var.get()
        if am_pm == "PM" and hour < 12:
            hour += 12
        elif am_pm == "AM" and hour == 12:
            hour = 0

        target = datetime(year, month, day, hour, minute, second)
        now = datetime.now()

        if target <= now:
            messagebox.showerror("⛔ Invalid Time", "Target time must be in the future.")
            return

        stop_event.clear()
        timer_thread = threading.Thread(target=run_timer, args=(target,), daemon=True)
        timer_thread.start()
        timer_running = True

    except ValueError:
        messagebox.showerror("⛔ Invalid Input", "Please enter valid date/time values.")

def stop_timer():
    global timer_running
    stop_event.set()
    timer_running = False
    update_display("⏸️ Paused")

def reset_timer():
    global timer_running
    stop_event.set()
    timer_running = False
    year_entry.delete(0, tk.END)
    month_entry.delete(0, tk.END)
    day_entry.delete(0, tk.END)
    hour_entry.delete(0, tk.END)
    minute_entry.delete(0, tk.END)
    second_entry.delete(0, tk.END)
    am_pm_var.set("AM")
    update_display("")

def run_timer(target):
    global timer_running
    while not stop_event.is_set():
        now = datetime.now()
        if now >= target:
            update_display("🔥 Time's up!")
            messagebox.showinfo("Countdown Done", "⏰ Time's up!")
            break

        remaining = target - now
        days = remaining.days
        hours, rem = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        time_str = f"{days}d {hours:02d}h:{minutes:02d}m:{seconds:02d}s"
        update_display(time_str)
        time.sleep(1)

def style_button(button):
    button.bind("<Enter>", lambda e: button.config(bg=BTN_HOVER))
    button.bind("<Leave>", lambda e: button.config(bg=BTN_BG))

btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack()

start_button = tk.Button(btn_frame, text="🚀 Start", command=start_timer, font=FONT, bg=BTN_BG, fg=FG)
stop_button = tk.Button(btn_frame, text="🛑 Stop", command=stop_timer, font=FONT, bg=BTN_BG, fg=FG)
reset_button = tk.Button(btn_frame, text="🔁 Reset", command=reset_timer, font=FONT, bg=BTN_BG, fg=FG)

for btn in [start_button, stop_button, reset_button]:
    btn.pack(side=tk.LEFT, padx=10, pady=10)
    style_button(btn)

root.mainloop()
