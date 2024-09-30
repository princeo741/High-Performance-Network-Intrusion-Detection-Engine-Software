# src/main.py

import tkinter as tk
from gui import PacketMonitorApp

def main():
    root = tk.Tk()
    app = PacketMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
