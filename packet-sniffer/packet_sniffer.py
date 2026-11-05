#!/usr/bin/env python3
"""
Packet Sniffer
--------------
A read-only network traffic inspector, built with Scapy, similar in
spirit to a very small subset of tcpdump or Wireshark's capture
functionality.

This tool only listens to and displays traffic visible to the
interface it runs on. It does not alter, redirect, inject, or block
any traffic. Only run it on networks and interfaces you own or are
authorised to monitor — in most jurisdictions, capturing traffic that
is not yours or that you are not authorised to see is illegal.

Usage:
    sudo python3 packet_sniffer.py -i eth0
    sudo python3 packet_sniffer.py -i eth0 -f "tcp port 80"
    sudo python3 packet_sniffer.py -i eth0 --count 50 --http-only
"""

import argparse
import sys
from datetime import datetime

try:
    from scapy.all import sniff, IP, TCP, UDP, Raw, conf
except ImportError:
    print("[!] Scapy is required: pip install scapy", file=sys.stderr)
    sys.exit(1)


def extract_http_hint(packet) -> str | None:
    """Return a short printable snippet if the packet looks like plaintext HTTP."""
    if packet.haslayer(Raw):
        payload = bytes(packet[Raw].load)
        try:
            text = payload.decode("utf-8", errors="ignore")
        except Exception:
            return None
        first_line = text.split("\r\n", 1)[0].strip()
        http_markers = ("GET ", "POST ", "PUT ", "DELETE ", "HTTP/1.", "Host:")
        if any(marker in text[:200] for marker in http_markers):
            return first_line[:120]
    return None


def describe_packet(packet, http_only: bool) -> str | None:
    """Build a one-line human-readable summary of a captured packet."""
    if not packet.haslayer(IP):
        return None

    ts = datetime.now().strftime("%H:%M:%S")
    src = packet[IP].src
    dst = packet[IP].dst

    if packet.haslayer(TCP):
        proto, sport, dport = "TCP", packet[TCP].sport, packet[TCP].dport
    elif packet.haslayer(UDP):
        proto, sport, dport = "UDP", packet[UDP].sport, packet[UDP].dport
    else:
        if http_only:
            return None
        proto, sport, dport = packet[IP].proto, "-", "-"

    http_hint = extract_http_hint(packet)
    if http_only and not http_hint:
        return None

    line = f"[{ts}] {proto:<4} {src}:{sport} -> {dst}:{dport}  len={len(packet)}"
    if http_hint:
        line += f"\n           HTTP: {http_hint}"
    return line


def make_handler(http_only: bool):
    def handle(packet):
        summary = describe_packet(packet, http_only)
        if summary:
            print(summary)
    return handle


def main() -> int:
    parser = argparse.ArgumentParser(
        description="A simple, read-only packet sniffer built on Scapy."
    )
    parser.add_argument("-i", "--interface", required=True,
                         help="Network interface to capture on (e.g. eth0)")
    parser.add_argument("-f", "--filter", default="ip",
                         help="BPF capture filter (default: 'ip')")
    parser.add_argument("-c", "--count", type=int, default=0,
                         help="Number of packets to capture (0 = unlimited, Ctrl+C to stop)")
    parser.add_argument("--http-only", action="store_true",
                         help="Only print packets that look like plaintext HTTP")
    args = parser.parse_args()

    conf.verb = 0
    print(f"[*] Sniffing on {args.interface} (filter: '{args.filter}'). "
          f"Press Ctrl+C to stop.\n")

    try:
        sniff(
            iface=args.interface,
            filter=args.filter,
            prn=make_handler(args.http_only),
            count=args.count or 0,
            store=False,
        )
    except PermissionError:
        print("[!] Permission denied. Try running with sudo.", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"[!] Could not open interface '{args.interface}': {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n[*] Capture stopped.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
