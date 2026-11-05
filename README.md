# SIWES Cybersecurity Tools

Tools and write-ups from a twelve-week SIWES industrial attachment in
cybersecurity and ethical hacking, built and tested entirely against
isolated virtual machines in a controlled lab environment.

Each tool has its own folder. Some include a working Python
implementation; others are documented as concept write-ups only,
where the working code would itself be a functional offensive
capability (traffic interception, credential attack, or malware).

| Tool | Code included? | Folder |
|---|---|---|
| MAC Address Changer | Yes | [`mac-address-changer/`](mac-address-changer) |
| Packet Sniffer | Yes | [`packet-sniffer/`](packet-sniffer) |
| ARP Spoof Detector | Yes | [`arp-spoof-detector/`](arp-spoof-detector) |
| Network Scanner (ARP host discovery) | README only | [`network-scanner/`](network-scanner) |
| ARP Spoofer | README only | [`arp-spoofer/`](arp-spoofer) |
| DNS Spoofer & MITM tools | README only | [`dns-spoofer-mitm/`](dns-spoofer-mitm) |
| Keylogger & Reverse Backdoor | README only | [`keylogger-backdoor/`](keylogger-backdoor) |
| Login Form Brute-Force Tool | README only | [`login-bruteforce-tool/`](login-bruteforce-tool) |
| Web Crawler & Basic Vulnerability Scanner | README only | [`web-crawler-vuln-scanner/`](web-crawler-vuln-scanner) |

## Why some tools have no code

Three of the tools above — the ARP spoofer, DNS spoofer/MITM tools,
and the keylogger/backdoor — are documented without runnable code
because the working implementation *is* the offensive capability:
there's no meaningful difference between "defensive research code"
and "a working exploit" for these. The login brute-force tool is
documented the same way, since it's a credential attack regardless of
framing. Each README explains how the technique works conceptually,
why it's excluded, and what defences counter it.

## Lab environment

All testing was performed exclusively against virtual machines on an
isolated, host-only or internal network, with no interaction with
production systems or any network outside the lab. See the full
SIWES report for the complete methodology, weekly logs, and technical
analysis.

## License

MIT — see individual folders. Use responsibly and only against
systems and networks you own or are explicitly authorised to test.
