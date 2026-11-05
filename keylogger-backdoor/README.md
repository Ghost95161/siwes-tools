# Keylogger and Reverse Backdoor

## What these are

- **Keylogger**: software that records every keystroke typed on a
  system, typically writing them to a local log file or exfiltrating
  them to a remote listener.
- **Reverse backdoor**: a small client that connects outward from a
  target machine to an attacker-controlled listener, giving the
  attacker a remote command shell on the target — "reverse" because
  the target initiates the connection, which helps it slip past
  inbound firewall rules.

## How they work, conceptually

- A keylogger hooks into the operating system's input handling (for
  example, via a low-level keyboard hook on Windows or an input
  device read on Linux) and writes each keystroke to a file or socket
  as it occurs.
- A reverse backdoor opens an outbound socket connection from the
  target to a listener controlled by the attacker, then pipes
  `stdin`/`stdout` through that socket so commands typed by the
  attacker execute on the target and the output is sent back.

## Why no working code is included

Both of these are textbook malware, independent of framing or stated
intent. A keylogger is built to covertly capture someone else's
credentials and private communications; a reverse backdoor is built
to give an attacker remote control of a machine they don't own. These
tools have essentially no legitimate general-purpose use outside of
malware analysis in a controlled environment, so this repo documents
the concepts and their defences without a working implementation.

## Defensive takeaway

- **Endpoint protection / EDR** to detect keyboard-hooking and
  anomalous outbound connections.
- **Application allow-listing**, so unrecognised executables can't
  run in the first place.
- **Egress filtering** on firewalls, limiting which outbound
  connections a host can make — reverse shells depend on being able
  to freely connect out.
- **User education** on how these tools are typically delivered
  (phishing attachments, trojanised downloads), since the delivery
  vector is usually the weaker link, not the network.

## Where this is covered

The full write-up, including how these concepts were studied against
virtual lab targets and the corresponding detection strategies, is in
Chapter Three (3.7 Common Attack Vectors and Defensive Concepts) and
the Week 9–10 sections of the accompanying SIWES report.
