import tkinter as tk
from tkinter import ttk

class ExpandableTextSection(tk.Frame):
    def __init__(self, parent, title, sid, content, details, mitigation, severity, **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title
        self.sid = sid
        self.content = content
        self.details = details
        self.mitigation = mitigation
        self.severity = severity
        self.is_expanded = False

        # Main frame styling
        self.configure(bg="#2b2b2b", relief="solid", bd=1)

        # Title label (clickable to toggle expansion)
        self.title_label = ttk.Label(self, text=f"{self.title} (SID: {self.sid})", font=("Helvetica", 12, "bold"), anchor="w", foreground="white")
        self.title_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.title_label.bind("<Button-1>", self.toggle_expansion)

        # Details container (hidden by default)
        self.details_frame = tk.Frame(self, bg="#2b2b2b")

        # Detailed information labels
        self.content_label = ttk.Label(self.details_frame, text=f"Description: {self.content}", wraplength=850, font=("Helvetica", 10), foreground="white")
        self.content_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)

        self.details_label = ttk.Label(self.details_frame, text=f"Alert Details: {self.details}", wraplength=850, font=("Helvetica", 10), foreground="white")
        self.details_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        self.mitigation_label = ttk.Label(self.details_frame, text=f"Mitigation: {self.mitigation}", wraplength=850, font=("Helvetica", 10), foreground="white")
        self.mitigation_label.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        self.severity_label = ttk.Label(self.details_frame, text=f"Severity: {self.severity}", wraplength=850, font=("Helvetica", 10, "bold"), foreground="red")
        self.severity_label.grid(row=3, column=0, sticky="w", padx=10, pady=2)

    def toggle_expansion(self, event):
        if self.is_expanded:
            self.details_frame.grid_forget()
        else:
            self.details_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.is_expanded = not self.is_expanded


class SecurityEventViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Security Event Viewer")
        self.geometry("900x700")
        self.configure(bg="#1e1e1e")

        # Title label
        self.header_label = ttk.Label(self, text="Security Event Rules", font=("Helvetica", 16, "bold"), background="#1e1e1e", foreground="white")
        self.header_label.pack(anchor="w", padx=20, pady=10)

        # Scrollable frame setup
        self.scroll_canvas = tk.Canvas(self, bg="#1e1e1e", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg="#1e1e1e")
        self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bindings for resizing and scrolling
        self.scrollable_frame.bind("<Configure>", self.update_scroll_region)
        self.scroll_canvas.bind_all("<MouseWheel>", self.mouse_scroll)

        # Dark mode style configuration
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", font=("Helvetica", 12), background="#1e1e1e", foreground="white")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TButton", font=("Helvetica", 10), background="#007ACC", foreground="white")

        # Adding the expandable text sections
        self.add_events()

    def update_scroll_region(self, event=None):
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def mouse_scroll(self, event):
        self.scroll_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def add_events(self):
        events = [
            ("Reconnaissance and Scanning", [
                ("TCP SYN Port Scan", "2000001", "This rule detects a TCP SYN scan, a common technique used by attackers to identify open ports.", 
                 "Attackers use this method to gather information about target systems and vulnerabilities.", 
                 "To mitigate, block SYN packets from untrusted sources or limit SYN packets rate.", "Medium"),

                ("UDP Scan", "2000002", "Similar to the SYN scan, but it applies to UDP traffic.", 
                 "Used by attackers to probe for open UDP ports.", 
                 "Mitigate by filtering and rate-limiting UDP traffic or using firewalls to block suspicious scans.", "Low"),

                ("ICMP Sweep", "2000003", "Detects an ICMP sweep, where an attacker sends ICMP Echo Request packets to a range of IP addresses.",
                 "An attacker tries to identify live hosts in a network.", 
                 "Mitigate by blocking unnecessary ICMP traffic or rate-limiting ICMP Echo Requests.", "Low"),

                ("DNS Zone Transfer Attempt", "2000004", "Detects an attempt to perform a DNS zone transfer.", 
                 "Attackers can gather information about the internal structure of the network.", 
                 "Mitigate by securing DNS servers and limiting zone transfers to authorized IPs.", "High"),

                ("SSH Brute Force", "2000005", "Detects multiple failed SSH login attempts in a short period, indicative of a brute force attack.", 
                 "Attackers attempt to guess the login credentials of a system via SSH.", 
                 "Mitigate by using stronger passwords, two-factor authentication, or rate-limiting SSH attempts.", "High"),
            ]),

            ("Exploitation and Intrusions", [
                ("EternalBlue SMB Exploit", "2000010", "Detects activity indicative of the EternalBlue exploit targeting SMB vulnerabilities.",
                 "This exploit allows attackers to execute arbitrary code on vulnerable systems, often leading to ransomware deployment.",
                 "Ensure all systems are patched against MS17-010 and restrict SMB access to trusted networks only.", "Critical"),

                ("SQL Injection", "2000011", "Detects patterns in traffic indicative of SQL injection attacks.",
                 "SQL injection enables attackers to manipulate database queries and potentially exfiltrate sensitive information.",
                 "Validate input rigorously and use parameterized queries to mitigate such attacks.", "High"),

                ("Shellshock Exploit", "2000012", "Identifies attempts to exploit the Shellshock vulnerability in Bash.",
                 "Attackers can exploit Shellshock to execute arbitrary commands on affected servers.",
                 "Upgrade Bash to a version patched against CVE-2014-6271 and restrict untrusted traffic.", "Critical"),

                ("RDP Exploit Detection", "2000013", "Detects suspicious RDP traffic often linked to exploits or brute-force attempts.",
                 "Such activity may indicate attempts to exploit RDP vulnerabilities or gain unauthorized access.",
                 "Restrict RDP access to trusted IPs and use multi-factor authentication.", "High"),

                ("XSS Attack", "2000014", "Identifies malicious input typical of cross-site scripting (XSS) attempts.",
                 "XSS can enable attackers to execute scripts in the context of a user’s browser session.",
                 "Sanitize all user input and implement Content Security Policy (CSP) headers.", "Medium"),
            ]),

            ("Malware Activity", [
                ("Malicious User-Agent Strings", "2000020", "Detects suspicious User-Agent strings indicative of malware communication.",
                 "Such User-Agents often identify malicious bots or compromised systems.",
                 "Monitor and block suspicious User-Agent strings at the proxy level.", "Medium"),

                ("Suspicious Executable Download", "2000021", "Detects attempts to download executable files, often linked to malware delivery.",
                 "Downloading executables from untrusted sources is a common malware vector.",
                 "Restrict executable downloads and inspect traffic for known malware signatures.", "High"),

                ("Cobalt Strike Beacon Traffic", "2000022", "Identifies traffic patterns characteristic of Cobalt Strike beacons.",
                 "Cobalt Strike is a popular tool for advanced persistent threats (APTs).",
                 "Detect and block command-and-control (C2) traffic at the firewall level.", "Critical"),

                ("Ransomware File Extensions", "2000023", "Detects suspicious file extensions often linked to ransomware activity.",
                 "Ransomware encrypts files and appends specific extensions.",
                 "Backup data regularly and monitor file activity for suspicious extensions.", "Critical"),
            ]),

            ("Command and Control (C2)", [
                ("DNS Tunneling Detection", "2000030", "Detects patterns indicative of DNS tunneling used for C2 communication.",
                 "DNS tunneling can exfiltrate data or enable remote command execution.",
                 "Monitor DNS traffic and use domain filtering to detect and block tunneling attempts.", "High"),

                ("Suspicious HTTPS Certificate", "2000031", "Identifies the use of suspicious HTTPS certificates in encrypted traffic.",
                 "Attackers may use self-signed or expired certificates for malicious purposes.",
                 "Inspect SSL traffic and enforce strict certificate validation policies.", "Medium"),
            ]),

            ("Data Exfiltration", [
                ("Large DNS TXT Response", "2000040", "Detects unusually large DNS TXT record responses indicative of exfiltration.",
                 "Attackers can encode data within DNS responses to exfiltrate information covertly.",
                 "Limit DNS TXT record sizes and monitor DNS traffic for anomalies.", "High"),

                ("FTP Suspicious Upload", "2000041", "Identifies suspicious file upload activities via FTP.",
                 "Attackers may use FTP to exfiltrate sensitive files.",
                 "Restrict FTP access and monitor upload activities for unauthorized transfers.", "High"),

                ("HTTP Data Leak", "2000042", "Detects keywords like 'password' in HTTP client body indicative of data leaks.",
                 "Sensitive data can be leaked through unencrypted HTTP traffic.",
                 "Enforce HTTPS for all communications and monitor outgoing traffic for sensitive terms.", "High"),
            ]),

            ("Denial of Service (DoS)", [
                ("SYN Flood", "2000050", "Detects high volumes of SYN packets indicative of a SYN flood DoS attack.",
                 "Such attacks can overwhelm servers, leading to service unavailability.",
                 "Implement SYN rate limiting and enable SYN cookies.", "Critical"),

                ("ICMP Flood", "2000051", "Detects high volumes of ICMP Echo Requests indicative of an ICMP flood DoS attack.",
                 "These attacks can saturate network bandwidth, disrupting services.",
                 "Rate-limit ICMP traffic and block unnecessary ICMP packets.", "Medium"),
            ]),

            ("Abuse of Services", [
                ("SMTP Spam", "2000060", "Detects spam activity through SMTP traffic.",
                 "Attackers often use compromised systems to send bulk spam emails.",
                 "Enforce rate limits on outgoing emails, monitor email traffic, and implement spam filters.", "Medium"),

                ("NTP Amplification", "2000061", "Detects NTP reflection attacks used for amplifying DoS attacks.",
                 "Attackers send forged requests to NTP servers, which then flood the victim with responses.",
                 "Disable unused NTP services or configure NTP servers to ignore MONLIST requests.", "High"),
            ]),

            ("Anomalous Behavior", [
                ("Non-Standard Protocols", "2000070", "Detects traffic using non-standard or custom protocols.",
                 "May indicate data exfiltration or custom malware C2 communication.",
                 "Inspect and block unknown or unauthorized protocols in network traffic.", "Medium"),

                ("Excessive Data Transfer", "2000071", "Detects unusually large volumes of data transfer.",
                 "Such activity could indicate data theft or large file transfers during an attack.",
                 "Implement data transfer rate limiting and monitor for unusual patterns.", "High"),
            ]),
        ]

        for category, alerts in events:
            category_label = ttk.Label(self.scrollable_frame, text=category, font=("Helvetica", 14, "bold"), background="#1e1e1e", foreground="cyan")
            category_label.pack(anchor="w", padx=10, pady=5)

            for title, sid, content, details, mitigation, severity in alerts:
                section = ExpandableTextSection(self.scrollable_frame, title, sid, content, details, mitigation, severity)
                section.pack(fill="x", padx=10, pady=5)


if __name__ == "__main__":
    app = SecurityEventViewer()
    app.mainloop()
