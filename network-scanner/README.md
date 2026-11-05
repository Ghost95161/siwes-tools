# Network Scanner (ARP-based Host Discovery)

## What it is

A tool that discovers which hosts are live on a local network segment
by sending ARP "who-has" requests across a given IP range and
recording which hosts reply, along with their MAC addresses. This is
the same technique behind `nmap -sn` (a "ping sweep") and `arp-scan`.

## How it works

1. An ARP request is broadcast for each IP address in the target
   range (e.g. 192.168.56.1–192.168.56.254).
2. Any live host on that range replies with its MAC address, since
   ARP has no authentication and every host must answer to keep
   communicating normally.
3. The tool records each IP/MAC pair that responds and prints a
   simple table of discovered hosts.

## Typical output

```
IP Address        MAC Address
-----------------  -----------------
192.168.56.1       08:00:27:aa:bb:cc
192.168.56.101     08:00:27:dd:ee:ff
```

## Why this one isn't included as code here

Host discovery itself is a benign, everyday admin technique — it's
exactly what `nmap -sn` does, and there's nothing attack-specific
about it. It's left as documentation only here simply because it
wasn't part of the batch of tools requested for this round; it's
straightforward to implement with Scapy (`sr()`/`srp()` against
`ARP()/Ether()` packets) if you'd like it added later, and is lower
risk than most of the other tools in this report.

## Legal note

Even simple host discovery can trigger intrusion-detection alerts or
violate acceptable-use policies if run against a network you don't
own or have permission to scan. Use only on networks you control or
are explicitly authorised to test — for example, your own lab subnet.
