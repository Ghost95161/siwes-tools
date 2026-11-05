# ARP Spoof Detector

A passive, defensive monitoring tool that watches ARP traffic for the
tell-tale sign of ARP spoofing: an IP address suddenly being claimed
by a new MAC address. Built with [Scapy](https://scapy.net/).

Built during a SIWES industrial attachment to understand ARP cache
poisoning from the defender's side, as a counterpart to studying how
the attack itself works.

## What it does

- Passively listens to ARP replies on a chosen interface.
- Remembers which MAC address(es) have claimed each IP address.
- Raises an alert the moment an IP address is claimed by a MAC
  address it hasn't been seen with before — the core signature of
  ARP spoofing / cache poisoning.
- Gives an extra warning if your network gateway's IP is the one
  being reclaimed, since that's the classic setup for a
  man-in-the-middle attack.
- Prints a summary of every conflicting IP/MAC pairing seen when you
  stop it.

## What it does *not* do

This tool is entirely passive. It never sends a packet, never writes
to any ARP table, and never interferes with network traffic — it only
observes and reports. It is the direct defensive counterpart to an
ARP spoofing tool, not a variant of one.

## Requirements

```bash
pip install scapy
```

Root privileges (or `CAP_NET_RAW`) are required for packet capture on
Linux.

## Usage

```bash
# Basic monitoring
sudo python3 arp_spoof_detector.py -i eth0

# Flag extra warnings if your gateway's IP looks spoofed
sudo python3 arp_spoof_detector.py -i eth0 --gateway-ip 192.168.56.1

# Monitor for a fixed duration (e.g. 5 minutes) then print a summary
sudo python3 arp_spoof_detector.py -i eth0 --duration 300
```

## How it works

ARP has no authentication: any device on a local network segment can
send an ARP reply claiming to own any IP address, and most operating
systems will trust the most recent reply they receive. ARP spoofing
exploits this to redirect traffic through an attacker's machine. This
tool simply keeps a running record of which MAC address has claimed
each IP address, and flags the moment that mapping changes
unexpectedly — a strong, simple heuristic for spotting an active ARP
spoofing attempt, which is the same underlying event that most
production ARP-spoofing detection tools look for.

## Notes

- False positives are possible if a device's network card is
  legitimately replaced, or after DHCP reassigns an IP to a different
  device — so treat alerts as something to investigate, not an
  automatic verdict.
- For production environments, pair this kind of detection with
  switch-level protections such as Dynamic ARP Inspection (DAI).
