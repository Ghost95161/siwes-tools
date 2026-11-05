#!/usr/bin/env python3
"""
MAC Address Changer
--------------------
Changes the MAC address of a specified network interface on Linux.

Legitimate uses:
  - Privacy (avoiding tracking by MAC on public Wi-Fi)
  - Testing network access-control / MAC-filtering configurations
  - Working around hardware-bound license or MAC-reservation issues
  - General network administration and lab work

This tool only modifies settings on interfaces you own or are
authorised to administer. It requires root privileges to run,
since changing an interface's hardware address needs CAP_NET_ADMIN.

Usage:
    sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
    sudo python3 mac_changer.py -i eth0 --random
    sudo python3 mac_changer.py -i eth0 --restore
"""

import argparse
import random
import re
import subprocess
import sys


def get_current_mac(interface: str) -> str | None:
    """Return the interface's current MAC address, or None if unreadable."""
    try:
        result = subprocess.run(
            ["ip", "link", "show", interface],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError:
        return None
    match = re.search(r"link/ether ([0-9a-f:]{17})", result.stdout)
    return match.group(1) if match else None


def is_valid_mac(mac: str) -> bool:
    """Validate the standard colon-separated MAC address format."""
    pattern = r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"
    return re.match(pattern, mac) is not None


def random_mac() -> str:
    """
    Generate a random, locally-administered, unicast MAC address.

    The second-least-significant bit of the first octet is set to 1
    (locally administered) and the least-significant bit is left at 0
    (unicast), which avoids colliding with real vendor-assigned
    addresses and avoids generating a multicast address.
    """
    first_octet = random.randint(0, 255)
    first_octet = (first_octet & 0b11111100) | 0b00000010
    octets = [first_octet] + [random.randint(0, 255) for _ in range(5)]
    return ":".join(f"{o:02x}" for o in octets)


def change_mac(interface: str, new_mac: str) -> bool:
    """Bring the interface down, change its MAC, then bring it back up."""
    try:
        subprocess.run(["ip", "link", "set", "dev", interface, "down"], check=True)
        subprocess.run(["ip", "link", "set", "dev", interface, "address", new_mac], check=True)
        subprocess.run(["ip", "link", "set", "dev", interface, "up"], check=True)
        return True
    except subprocess.CalledProcessError as exc:
        print(f"[!] Failed to change MAC address: {exc}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("[!] The 'ip' command was not found. Install iproute2.", file=sys.stderr)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Change the MAC address of a network interface."
    )
    parser.add_argument("-i", "--interface", required=True,
                         help="Network interface to modify (e.g. eth0, wlan0)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--mac", help="New MAC address, e.g. 00:11:22:33:44:55")
    group.add_argument("--random", action="store_true",
                        help="Generate and assign a random MAC address")
    group.add_argument("--restore", metavar="ORIGINAL_MAC",
                        help="Restore a previously saved original MAC address")
    args = parser.parse_args()

    current = get_current_mac(args.interface)
    if current is None:
        print(f"[!] Could not read current MAC for interface '{args.interface}'. "
              "Does it exist?", file=sys.stderr)
        return 1
    print(f"[*] Current MAC on {args.interface}: {current}")

    if args.random:
        new_mac = random_mac()
    elif args.restore:
        new_mac = args.restore
    else:
        new_mac = args.mac

    if not is_valid_mac(new_mac):
        print(f"[!] '{new_mac}' is not a valid MAC address.", file=sys.stderr)
        return 1

    print(f"[*] Setting new MAC: {new_mac}")
    if not change_mac(args.interface, new_mac):
        return 1

    updated = get_current_mac(args.interface)
    if updated and updated.lower() == new_mac.lower():
        print(f"[+] Success. {args.interface} is now using {updated}")
        print(f"[i] To restore the original MAC later, run:\n"
              f"    sudo python3 {sys.argv[0]} -i {args.interface} --restore {current}")
        return 0
    else:
        print("[!] The MAC address does not appear to have changed. "
              "Some drivers ignore software-set MAC addresses.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    if sys.platform != "linux":
        print("[!] This tool targets Linux (uses the 'ip' command).", file=sys.stderr)
        sys.exit(1)
    sys.exit(main())
