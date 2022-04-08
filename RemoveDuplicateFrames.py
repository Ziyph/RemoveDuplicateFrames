import pathlib
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

ffmpeg = f"{pathlib.Path(__file__).parent}/ffmpeg"


def open_file():
    global opened_files
    opened_files = filedialog.askopenfilenames(
        filetypes=(
            ("MP4 Files", "*.mp4"),
            ("MOV Files", "*.mov"),
            ("All Files", "*.*"),
        ),
    )
    if opened_files:
        opened_files_label.configure(text=f"Opened files: {', '.join(opened_files)}")


def remove_duplicate_frames():
    for opened_file in opened_files:
        subprocess.Popen(
            [
                ffmpeg,
                "-i",
                opened_file,
                "-vf",
                "mpdecimate,setpts=N/FRAME_RATE/TB",
                f"{pathlib.Path(opened_file).parent}/{pathlib.Path(opened_file).stem}_proccessed{pathlib.Path(opened_file).suffix}",
            ]
        )


root = Tk()
root.title("Remove Duplicate Frames")
mainframe = ttk.Frame(root)
mainframe.grid()
ttk.Button(mainframe, text="Open file", command=open_file).grid()
opened_files_label = ttk.Label(mainframe, text="No file opened.")
opened_files_label.grid()
ttk.Button(
    mainframe, text="Remove duplicate frames", command=remove_duplicate_frames
).grid()
root.mainloop()
