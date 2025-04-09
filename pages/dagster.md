---
slug: /dagster
title: Dagster
description: Deploying Dagster on Ubuntu with Python 3.12.9, Systemd, and Tailscale
allow_html: true
template: page.html
---

###### In this guide, I’ll walk you through how I deployed [Dagster](https://dagster.io/), a powerful data orchestration platform, on an Ubuntu server using:

- Python 3.12.9 (via source build)
- Virtual environments
- systemd for managing services
- Tailscale for secure remote access

By the end, you'll have a production-ready Dagster instance that you can access from anywhere securely.

###### Prerequisites

- Ubuntu 22.04+ (I used 24.04)
- [Tailscale](https://tailscale.com) account (for secure remote access)
- Basic familiarity with Linux, systemd, and Python virtual environments

###### Install Python 3.12.9 from Source

```bash
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev \
  libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget curl libbz2-dev

cd /tmp
wget https://www.python.org/ftp/python/3.12.9/Python-3.12.9.tgz
tar -xf Python-3.12.9.tgz
cd Python-3.12.9
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
```

###### Create a Virtual Environment
```bash
python3.12 -m venv ~/venv312
source ~/venv312/bin/activate
mkdir ~/Documents/dagster_workspace
```

###### Install Dagster and Example Project

```bash
pip install dagster dagster-webserver dagster-daemon

dagster project from-example --example getting_started_etl_tutorial --name example_etl

pip install -e ~/Documents/dagster_workspace/example_etl
```

###### Set Up DAGSTER_HOME
```bash
mkdir -p ~/.dagster
vim ~/.dagster/dagster.yaml
```
```yaml
local_artifact_storage:
  module: dagster._core.storage.root
  class: LocalArtifactStorage
  config:
    base_dir: /home/protim/.dagster

run_storage:
  module: dagster._core.storage.runs
  class: SqliteRunStorage
  config:
    base_dir: /home/protim/.dagster

event_log_storage:
  module: dagster._core.storage.event_log
  class: SqliteEventLogStorage
  config:
    base_dir: /home/protim/.dagster

schedule_storage:
  module: dagster._core.storage.schedules
  class: SqliteScheduleStorage
  config:
    base_dir: /home/protim/.dagster

run_launcher:
  module: dagster._core.launcher.default_run_launcher
  class: DefaultRunLauncher
```

Then add this to your ~/.bashrc:
```bash
export DAGSTER_HOME=/home/protim/.dagster
source ~/.bashrc
```

