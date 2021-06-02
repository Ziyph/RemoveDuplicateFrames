import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from threading import Thread
from subprocess import Popen, run, PIPE


class RemoveDuplicateFrames(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent_directory = Path(__file__).parent.absolute()

        def select_file():
            self.selected_file = filedialog.askopenfilename(
                initialdir="/",
                title="Select file",
                filetypes=(("MOV files", "*.mov"), ("All files", "*.*")),
            )
            if self.selected_file:
                remove_duplicate_frames_button.config(state=tk.NORMAL)
                selected_file_label.configure(
                    text=f"Selected file: {self.selected_file}"
                )

        def remove_duplicate_frames():
            def ffmpeg():
                ffmpeg = Popen(
                    [
                        f"{self.parent_directory}/ffmpeg",
                        "-v",
                        "0",
                        "-progress",
                        "/dev/stdout",
                        "-i",
                        f"{self.selected_file}",
                        "-c:v",
                        run(
                            [
                                f"{self.parent_directory}/ffprobe",
                                "-v",
                                "0",
                                "-select_streams",
                                "v:0",
                                "-show_entries",
                                "stream=codec_name",
                                "-of",
                                "default=noprint_wrappers=1:nokey=1",
                                self.selected_file,
                            ],
                            capture_output=True,
                            text=True,
                        ).stdout.split("\n", 1)[0],
                        "-vf",
                        "mpdecimate,setpts=N/FRAME_RATE/TB",
                        f"{Path(self.selected_file).parent.absolute()}/{Path(self.selected_file).stem}_processed.mov",
                    ],
                    stdout=PIPE,
                    bufsize=0,
                    text=True,
                )
                log(f"Operation started.\nFile: {self.selected_file}")
                for line in ffmpeg.stdout:
                    if "frame=" in line:
                        log(f"Frame: " + line.split("=", 1)[1].split("\n")[0])
                log("Operation ended.")

            thread = Thread(target=ffmpeg, daemon=True)
            thread.start()

        tk.Button(self.parent, text="Select file", command=select_file).pack(
            fill=tk.BOTH, expand=True, padx=4, pady=4
        )
        remove_duplicate_frames_button = tk.Button(
            self.parent,
            text="Remove duplicate frames",
            state=tk.DISABLED,
            command=remove_duplicate_frames,
        )
        remove_duplicate_frames_button.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        selected_file_label = tk.Label(self.parent, text="Selected file: none")
        selected_file_label.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        operation_log = tk.Text(self.parent, state=tk.DISABLED, bg="black", fg="lime")
        operation_log.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        def log(text):
            operation_log.config(state=tk.NORMAL)
            operation_log.insert(tk.END, f"{text}\n")
            operation_log.config(state=tk.DISABLED)
            operation_log.see(tk.END)

        log("The progress of operations will be here.")


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0, 0)
    root.title("Remove Duplicate Frames")
    RemoveDuplicateFrames(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()
