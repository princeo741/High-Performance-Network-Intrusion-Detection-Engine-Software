# src/packet_capture.py

from scapy.all import sniff
import threading

class PacketCapture:
    def __init__(self, tree):
        self.tree = tree
        self.is_monitoring = False
        self.sniff_thread = None

    def packet_callback(self, packet):
        if self.is_monitoring:
            # Extract packet details
            src_ip = packet[1].src if hasattr(packet, 'src') else 'N/A'
            dst_ip = packet[1].dst if hasattr(packet, 'dst') else 'N/A'
            protocol = packet[1].proto if hasattr(packet, 'proto') else 'N/A'
            length = len(packet)
            self.tree.insert('', 'end', values=(src_ip, dst_ip, protocol, length))

    def start_capture(self):
        self.is_monitoring = True
        self.sniff_thread = threading.Thread(target=self.sniff_packets)
        self.sniff_thread.start()

    def stop_capture(self):
        self.is_monitoring = False
        if self.sniff_thread:
            self.sniff_thread.join()

    def sniff_packets(self):
        sniff(prn=self.packet_callback, store=0)
