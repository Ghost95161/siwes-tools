# ARP Spoofer

## What it is

A man-in-the-middle tool that exploits ARP's lack of authentication
to associate an attacker's MAC address with another host's IP address
(commonly the network gateway), causing traffic meant for that IP to
be routed through the attacker's machine instead.

## How it works, conceptually

1. The tool repeatedly sends forged ARP "is-at" replies to a target
   device, claiming that the gateway's IP address belongs to the
   attacker's MAC address.
2. It does the same in reverse to the gateway, claiming the target's
   IP belongs to the attacker.
3. Both devices update their ARP caches to point at the attacker,
   who now sits between them and can observe or alter their traffic
   (often paired with IP forwarding so the connection keeps working
   and the attack stays unnoticed).

## Why no working code is included

This is a functional man-in-the-middle capability: it lets the
operator intercept, read, and potentially modify someone else's
network traffic. Providing ready-to-run code would give real
capability to attack a network, regardless of the stated intent, so
this repo intentionally documents the concept and its defences
without an executable implementation.

## Defensive takeaway

- Deploy switch-level protections such as **Dynamic ARP Inspection
  (DAI)**, which validates ARP packets against a trusted DHCP
  binding table.
- Use **static ARP entries** for critical infrastructure such as
  gateways, where practical.
- Monitor for ARP anomalies — see the
  [ARP Spoof Detector](../arp-spoof-detector) in this collection,
  which watches for exactly this kind of attack.
- Prefer encrypted protocols (HTTPS, SSH, VPNs) so that even a
  successful MITM position yields little to an attacker.

## Where this is covered

The full write-up of this technique, including how it was studied and
tested against virtual machines in an isolated lab environment, is in
Chapter Three (3.2 Network Fundamentals) and Appendix A of the
accompanying SIWES report.
