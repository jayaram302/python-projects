import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
import time
import threading
import winsound

# Global variables
alarm_time = None
alarm_tone = None
snooze_minutes = 5
alarm_running = False

# Select alarm tone
def select_tone():
    global alarm_tone

    file = filedialog.askopenfilename(
        title="Select Alarm Tone",
        filetypes=[("WAV files", "*.wav")]
    )

    if file:
        alarm_tone = file
        tone_label.config(text="Tone: " + file.split("/")[-1])

# Set Alarm

def set_alarm():
    global alarm_time, snooze_minutes

    hour = hour_entry.get()
    minute = minute_entry.get()

    if not hour.isdigit() or not minute.isdigit():
        messagebox.showerror("Error", "Enter valid hour and minute")
        return

    hour = int(hour)
    minute = int(minute)

    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        messagebox.showerror("Error", "Invalid time")
        return

    alarm_time = f"{hour:02d}:{minute:02d}"

    snooze_minutes = int(snooze_entry.get())

    status_label.config(
        text=f"Alarm set for {alarm_time}"
    )

    threading.Thread(
        target=check_alarm,
        daemon=True
    ).start()


# Check Alarm
def check_alarm():
    global alarm_running

    while alarm_time:
        current_time = datetime.datetime.now().strftime("%H:%M")

        if current_time == alarm_time:
            alarm_running = True
            play_alarm()
            break

        time.sleep(1)

# Play Alarm

def play_alarm():
    alarm_window = tk.Toplevel(root)
    alarm_window.title("⏰ ALARM!")
    alarm_window.geometry("350x220")

    tk.Label(
        alarm_window,
        text="⏰ ALARM RINGING!",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    def ring():
        while alarm_running:
            if alarm_tone:
                winsound.PlaySound(
                    alarm_tone,
                    winsound.SND_FILENAME
                )
            else:
                winsound.Beep(1000, 1000)

    threading.Thread(
        target=ring,
        daemon=True
    ).start()

    def stop_alarm():
        global alarm_running
        alarm_running = False
        alarm_window.destroy()

    def snooze_alarm():
        global alarm_time, alarm_running

        alarm_running = False
        alarm_window.destroy()

        new_time = (
            datetime.datetime.now()
            + datetime.timedelta(minutes=snooze_minutes)
        )

        alarm_time = new_time.strftime("%H:%M")

        status_label.config(
            text=f"Snoozed until {alarm_time}"
        )

        threading.Thread(
            target=check_alarm,
            daemon=True
        ).start()

    tk.Button(
        alarm_window,
        text="🛑 Stop",
        width=12,
        command=stop_alarm
    ).pack(pady=5)

    tk.Button(
        alarm_window,
        text=f"😴 Snooze {snooze_minutes} min",
        width=18,
        command=snooze_alarm
    ).pack(pady=5)


# Main Window

root = tk.Tk()
root.title("⏰ Python Alarm Clock")
root.geometry("450x400")

tk.Label(
    root,
    text="⏰ ALARM CLOCK",
    font=("Arial", 26, "bold")
).pack(pady=20)

# Time
tk.Label(root, text="Set Alarm Time (24-hour format)").pack()

frame = tk.Frame(root)
frame.pack(pady=10)

hour_entry = tk.Entry(frame, width=5, font=("Arial", 16))
hour_entry.pack(side=tk.LEFT)

tk.Label(frame, text=" : ", font=("Arial", 16)).pack(side=tk.LEFT)

minute_entry = tk.Entry(frame, width=5, font=("Arial", 16))
minute_entry.pack(side=tk.LEFT)

# Snooze
tk.Label(
    root,
    text="Snooze duration (minutes)"
).pack(pady=10)

snooze_entry = tk.Entry(root, width=10)
snooze_entry.insert(0, "5")
snooze_entry.pack()

# Tone
tk.Button(
    root,
    text="🔔 Choose Alarm Tone",
    command=select_tone
).pack(pady=15)

tone_label = tk.Label(
    root,
    text="Tone: Default Beep"
)
tone_label.pack()

# Set alarm
tk.Button(
    root,
    text="⏰ SET ALARM",
    font=("Arial", 14, "bold"),
    command=set_alarm
).pack(pady=20)

status_label = tk.Label(
    root,
    text="No alarm set",
    font=("Arial", 12)
)
status_label.pack()

root.mainloop()