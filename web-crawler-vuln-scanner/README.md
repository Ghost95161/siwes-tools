# Web Crawler & Basic Vulnerability Scanner

## What these are

- **Web crawler**: a tool that starts from a URL, follows links and
  form actions within a site, and builds a map of reachable pages,
  directories, and files — used here for reconnaissance of a lab
  target before testing.
- **Basic vulnerability scanner**: a tool that checks a web target
  for common, low-risk issues such as missing security headers
  (e.g. `X-Frame-Options`, `Content-Security-Policy`), enabled
  directory listing, and simple reflected-input injection points.

## Why these aren't included as code here

Unlike most of the other tools in this collection, a basic crawler
and a header/misconfiguration checker are largely benign,
reconnaissance-level utilities — closer in spirit to what a browser
or `curl` does automatically, or what free online tools like
Security Headers already offer. They're documented here only because
they weren't part of the batch of tools requested for this round, not
because of a safety concern. They're reasonable to add later if
useful — happy to write them if you want them included.

## How they work, conceptually

- The crawler fetches a starting URL, parses the HTML for `<a href>`
  and `<form action>` targets, and recursively visits newly
  discovered same-site links, recording a sitemap-like structure.
- The scanner sends ordinary HTTP requests to discovered pages, then
  inspects the response headers and basic input fields for the
  absence of standard protections (not active exploitation — just
  checking what's missing or exposed).

## Where this is covered

The full write-up, including how these were built and tested against
a self-hosted lab target, is in Chapter Three (3.7 Common Attack
Vectors) and the Week 11–12 sections of the accompanying SIWES
report.
