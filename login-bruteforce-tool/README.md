# Login Form Brute-Force Tool

## What it is

A tool that automates repeated login attempts against a web
application's authentication form, trying many username/password
combinations from a wordlist in order to find valid credentials.

## How it works, conceptually

1. The tool submits an HTTP POST request to a login endpoint with a
   candidate username and password from a wordlist.
2. It inspects the response (status code, redirect, or a specific
   page element) to determine whether the login succeeded or failed.
3. It repeats this for every combination in the wordlist, optionally
   in parallel, until it finds a working credential pair or exhausts
   the list.

## Why no working code is included

This is a credential-attack tool aimed at breaking into accounts that
don't belong to the operator. Even when framed as a security-testing
tool, the resulting code is directly usable to attack real login
systems, so this repo documents the technique and its defences rather
than providing a runnable implementation.

## Defensive takeaway

- **Rate limiting and account lockout** after a small number of
  failed attempts.
- **CAPTCHAs** on login forms after repeated failures.
- **Multi-factor authentication (MFA)**, so a correct password alone
  isn't sufficient to gain access.
- **Strong password policies** and breach-password screening, to
  reduce the number of accounts vulnerable to common-password
  guessing in the first place.
- **Centralised logging and alerting** on repeated failed logins from
  a single source, to catch an attack in progress.

## Where this is covered

The full write-up, including how this was tested against a
self-hosted login form in an isolated lab environment, is in Chapter
Three (3.7 Common Attack Vectors and Defensive Concepts) and the Week
11 section of the accompanying SIWES report.
