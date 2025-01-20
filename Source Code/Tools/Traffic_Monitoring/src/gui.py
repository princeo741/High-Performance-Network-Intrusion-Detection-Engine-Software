# src/gui.py

import tkinter as tk
from tkinter import ttk
from packet_capture import PacketCapture

class PacketMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Traffic Monitoring")
        
        # Create a Treeview for displaying packets
        self.tree = ttk.Treeview(root, columns=('Source IP', 'Destination IP', 'Protocol', 'Length'), show='headings')
        self.tree.heading('Source IP', text='Source IP')
        self.tree.heading('Destination IP', text='Destination IP')
        self.tree.heading('Protocol', text='Protocol')
        self.tree.heading('Length', text='Packet Length')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Start and Stop buttons
        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_button.pack(side=tk.LEFT)

        self.packet_capture = PacketCapture(self.tree)
        self.is_monitoring = False

    def start_monitoring(self):
        self.is_monitoring = True
        self.packet_capture.start_capture()

    def stop_monitoring(self):
        self.is_monitoring = False
        self.packet_capture.stop_capture()
