#!/usr/bin/env python3
"""
ARP Spoof Detector
-------------------
A defensive monitoring tool that watches ARP traffic on a network
interface and raises an alert when it sees a sign of ARP spoofing:
the same IP address being claimed by more than one MAC address.

This is a purely passive, read-only tool. It does not send any
packets, does not alter any ARP table, and does not interfere with
network traffic in any way — it only listens and reports.

Usage:
    sudo python3 arp_spoof_detector.py -i eth0
    sudo python3 arp_spoof_detector.py -i eth0 --gateway-ip 192.168.56.1
"""

import argparse
import sys
import time
from collections import defaultdict
from datetime import datetime

try:
    from scapy.all import sniff, ARP, conf
except ImportError:
    print("[!] Scapy is required: pip install scapy", file=sys.stderr)
    sys.exit(1)


class ArpWatcher:
    """Tracks IP -> set of MAC addresses seen, and flags conflicts."""

    def __init__(self, gateway_ip: str | None = None):
        self.ip_to_macs: dict[str, set[str]] = defaultdict(set)
        self.gateway_ip = gateway_ip
        self.alerts_raised = 0

    def _timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def handle_packet(self, packet) -> None:
        if not packet.haslayer(ARP):
            return
        arp = packet[ARP]

        # op=1 is "who-has" (request), op=2 is "is-at" (reply).
        # Spoofing is most meaningfully observed in replies, since
        # that is what poisons a victim's ARP cache.
        if arp.op != 2:
            return

        ip = arp.psrc
        mac = arp.hwsrc
        if ip == "0.0.0.0" or mac == "00:00:00:00:00:00":
            return

        known_macs = self.ip_to_macs[ip]
        if known_macs and mac not in known_macs:
            self.alerts_raised += 1
            print(f"[!] [{self._timestamp()}] POSSIBLE ARP SPOOFING DETECTED")
            print(f"    IP {ip} was previously seen as {sorted(known_macs)}")
            print(f"    but is now claimed by {mac}")
            if self.gateway_ip and ip == self.gateway_ip:
                print(f"    WARNING: {ip} is your configured gateway address — "
                      f"this may be a man-in-the-middle attempt.")
            print()
        known_macs.add(mac)

    def summary(self) -> None:
        print(f"\n[*] Monitoring ended. {self.alerts_raised} alert(s) raised.")
        conflicted = {ip: macs for ip, macs in self.ip_to_macs.items() if len(macs) > 1}
        if conflicted:
            print("[*] IP addresses seen with more than one MAC address:")
            for ip, macs in conflicted.items():
                print(f"    {ip}: {sorted(macs)}")
        else:
            print("[*] No IP address was seen with more than one MAC address.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Passively monitor ARP traffic for signs of ARP spoofing."
    )
    parser.add_argument("-i", "--interface", required=True,
                         help="Network interface to monitor (e.g. eth0)")
    parser.add_argument("--gateway-ip", default=None,
                         help="Your network gateway's IP address, for extra warnings "
                              "if it appears to be spoofed")
    parser.add_argument("--duration", type=int, default=0,
                         help="Seconds to monitor for (0 = run until Ctrl+C)")
    args = parser.parse_args()

    conf.verb = 0
    watcher = ArpWatcher(gateway_ip=args.gateway_ip)

    print(f"[*] Watching ARP traffic on {args.interface}. Press Ctrl+C to stop.\n")

    try:
        sniff(
            iface=args.interface,
            filter="arp",
            prn=watcher.handle_packet,
            store=False,
            timeout=args.duration or None,
        )
    except PermissionError:
        print("[!] Permission denied. Try running with sudo.", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"[!] Could not open interface '{args.interface}': {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        pass

    watcher.summary()
    return 0


if __name__ == "__main__":
    sys.exit(main())
