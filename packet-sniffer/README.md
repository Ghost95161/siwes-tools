# Packet Sniffer

A small, read-only network traffic inspector built with
[Scapy](https://scapy.net/). It captures packets visible to a given
interface and prints a one-line summary of each, with an optional
filter for plaintext HTTP traffic.

Built during a SIWES industrial attachment to explore packet capture,
the TCP/IP stack, and Scapy's packet-dissection API in a controlled
lab setting.

## What it does

- Captures packets on a chosen interface, optionally filtered with a
  standard BPF filter string (the same syntax tcpdump uses).
- Prints source/destination IP, port, protocol and packet length.
- Optionally flags and prints the first line of any plaintext HTTP
  request or response it sees (`--http-only`), to demonstrate why
  unencrypted HTTP traffic is visible to anyone sharing the network
  segment — and why HTTPS matters.

## What it does *not* do

This tool only reads traffic that is already reaching the interface —
it does not inject, redirect, modify, drop, or retransmit any packet.
It has no ARP-spoofing or MITM capability of its own; it is purely a
capture-and-display tool, like a minimal version of `tcpdump`.

## Requirements

```bash
pip install scapy
```

Root privileges (or `CAP_NET_RAW`) are required for raw packet
capture on Linux.

## Usage

```bash
# Capture all IP traffic on eth0
sudo python3 packet_sniffer.py -i eth0

# Capture only HTTP (port 80) traffic
sudo python3 packet_sniffer.py -i eth0 -f "tcp port 80"

# Stop automatically after 50 packets
sudo python3 packet_sniffer.py -i eth0 --count 50

# Only show packets that look like plaintext HTTP
sudo python3 packet_sniffer.py -i eth0 --http-only
```

## Legal and ethical note

Capturing network traffic that is not yours, or that you are not
authorised to monitor, is illegal in most jurisdictions and a
violation of most network acceptable-use policies. Only run this on
networks and interfaces you own or have explicit permission to
inspect — for example, your own home network, a virtual lab network,
or infrastructure you administer professionally.
