---
slug: /dagster
title: Dagster
description: This page is about setting up dagster for data ingestion.
allow_html: true
template: page.html
---

#  Deploying Dagster on Ubuntu with Python 3.12.9, Systemd, and Tailscale

In this guide, I’ll walk you through how I deployed [Dagster](https://dagster.io/), a powerful data orchestration platform, on an Ubuntu server using:

- Python 3.12.9 (via source build)
- Virtual environments
- systemd for managing services
- Tailscale for secure remote access

By the end, you'll have a production-ready Dagster instance that you can access from anywhere securely. 💪
