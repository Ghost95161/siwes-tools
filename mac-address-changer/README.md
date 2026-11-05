# MAC Address Changer

A small command-line tool that changes the MAC (hardware) address of a
network interface on Linux, using the standard `ip` command from
`iproute2`.

Built during a SIWES industrial attachment as an introduction to
network interfaces, Linux networking tools, and `subprocess`-based
automation in Python.

## What it does

- Reads and displays an interface's current MAC address.
- Sets a MAC address you specify, or generates a random
  locally-administered one.
- Lets you restore the original MAC address later.

## Why this is useful

- **Privacy** — avoid being tracked by MAC address on public networks.
- **Testing** — verify MAC-based access control or filtering rules on
  a router or switch.
- **Lab work** — reset a virtual machine's interface to a known state.

## Requirements

- Linux with `iproute2` installed (the `ip` command).
- Python 3.10+ (for the `str | None` type hint syntax; remove it for
  older Python).
- Root privileges (changing a MAC address requires `CAP_NET_ADMIN`).

## Usage

```bash
# Set a specific MAC address
sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55

# Generate and assign a random MAC address
sudo python3 mac_changer.py -i eth0 --random

# Restore a previously noted original MAC address
sudo python3 mac_changer.py -i eth0 --restore aa:bb:cc:dd:ee:ff
```

## Notes

- Some network drivers and virtual NICs ignore software-set MAC
  addresses, or reset them after a reboot — this is a driver
  limitation, not a bug in the script.
- Only run this against interfaces you own or are authorised to
  administer.
