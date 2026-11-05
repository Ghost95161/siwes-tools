# DNS Spoofer and Related MITM Tools

## What it is

A set of tools that build on an established man-in-the-middle
position (typically via ARP spoofing) to intercept DNS queries from a
victim and return forged responses, redirecting the victim's traffic
to an attacker-controlled destination. Related tools in this category
intercept and modify in-flight HTTP content or inject code into
unencrypted responses.

## How it works, conceptually

1. Once traffic is flowing through the attacker's machine (see
   [ARP Spoofer](../arp-spoofer)), DNS queries from the victim are
   visible in transit.
2. The attacker's tool recognises a DNS query for a target domain and
   races a forged DNS response back to the victim before the real
   DNS server's reply arrives.
3. The victim's device accepts the forged response (since plain DNS
   has no authentication) and connects to whatever IP address the
   attacker chose.
4. Related MITM tools operate similarly on intercepted HTTP traffic —
   rewriting pages or injecting content into unencrypted responses.

## Why no working code is included

This is a functional traffic-interception and redirection capability
— it can be used to redirect victims to malicious sites, serve fake
login pages, or inject arbitrary content. Providing runnable code
would hand over real offensive capability, so this repo documents the
concept and its defences only.

## Defensive takeaway

- Use **DNSSEC** where available, to cryptographically validate DNS
  responses.
- Prefer **encrypted DNS** (DNS-over-HTTPS or DNS-over-TLS) so queries
  can't be read or forged in transit.
- Enforce **HTTPS everywhere**, including HSTS, so a spoofed DNS
  response alone isn't enough to intercept meaningful content.
- Treat DNS spoofing as a downstream consequence of ARP spoofing in
  most LAN scenarios — the ARP-level defences in the
  [ARP Spoofer](../arp-spoofer) README are the first line of defence.

## Where this is covered

The full write-up, including how DNS spoofing was studied against
virtual lab targets, is in Chapter Three (3.4 Domain Name System and
Spoofing Concepts) and the Week 8 section of the accompanying SIWES
report.
