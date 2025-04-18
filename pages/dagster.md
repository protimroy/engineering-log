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

###### Pre-requisites

We will need these pre-requisites to get started:

- Ubuntu 22.04+ (I used 24.04)
- [Tailscale](https://tailscale.com) account (for secure remote access)
- Basic familiarity with Linux, systemd, and Python virtual environments

###### Install Python 3.12.9 from source

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

###### Create a virtual environment

We create a virtual environment to isolate our Dagster installation from the system Python and create a dagster workspace folder where we can store all our Dagster projects.

```bash
python3.12 -m venv ~/venv312
source ~/venv312/bin/activate
mkdir ~/Documents/dagster_workspace
```

###### Install Dagster, example project, and dependencies

We will install Dagster and the example ETL project. We will then install all the dependencies for the example project.

```bash
pip install dagster dagster-webserver
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
    base_dir: /home/user/.dagster

run_storage:
  module: dagster._core.storage.runs
  class: SqliteRunStorage
  config:
    base_dir: /home/user/.dagster

event_log_storage:
  module: dagster._core.storage.event_log
  class: SqliteEventLogStorage
  config:
    base_dir: /home/user/.dagster

schedule_storage:
  module: dagster._core.storage.schedules
  class: SqliteScheduleStorage
  config:
    base_dir: /home/user/.dagster

run_launcher:
  module: dagster._core.launcher.default_run_launcher
  class: DefaultRunLauncher
```

Then add this to your ```~/.bashrc```:

```bash
export DAGSTER_HOME=/home/user/.dagster
source ~/.bashrc
```

###### Configure systemd services

```bash
sudo vim /etc/systemd/system/dagster-webserver.service
```
```ini
[Unit]
Description=Dagster Webserver
After=network.target

[Service]
Type=simple
User=user
WorkingDirectory=/home/user/Documents/dagster_workspace
ExecStart=/home/user/venv312/bin/dagster-webserver -h 0.0.0.0 -p 3000
Restart=always
RestartSec=10
Environment=PATH=/home/user/venv312/bin:/usr/bin:/bin
Environment=PYTHONUNBUFFERED=1
Environment=DAGSTER_HOME=/home/user/.dagster

[Install]
WantedBy=multi-user.target
```

```bash
sudo vim /etc/systemd/system/dagster-daemon.service
```
```ini

[Unit]
Description=Dagster Daemon
After=network.target

[Service]
Type=simple
User=user
WorkingDirectory=/home/user/Documents/dagster_workspace
ExecStart=/home/user/venv312/bin/dagster-daemon run
Restart=always
RestartSec=10
EnvironmentFile=/etc/dagster-daemon.env
Environment=PATH=/home/user/venv312/bin:/usr/bin:/bin
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

```bash
sudo vim /etc/dagster-daemon.env
```
```bash
DAGSTER_HOME=/home/user/.dagster
```
Then reload systemd and enable both services:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable dagster-webserver dagster-daemon
sudo systemctl start dagster-webserver dagster-daemon
```

###### Create your Dagster workspace
First, open a workspace yaml file.
```bash
sudo vim ~/Documents/dagster_workspace/workspace.yaml
```
Then setup the yaml file for Dagster to load the project from relative path.
```yaml
load_from:
  - python_package:
      package_name: quickstart_etl
      working_directory: example_etl
      location_name: quickstart_etl
```

###### Enable secure remote access via Tailscale
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Then open the Dagster UI from your browser:
```
http://<tailscale-ip>:3000
```

###### Conclusion

You've now deployed Dagster with:
 - A clean Python 3.12.9 venv
 - Fully-managed daemon and webserver
 - Secure remote access via Tailscale
 - A functioning example ETL pipeline with schedules and assets

This setup is a great starting point for building and deploying your data pipelines. You can now extend this to include more complex workflows, integrate with other data sources, and scale as needed.\
Dagster sensors and schedules can be added to trigger jobs based on external events or time intervals, making it a powerful tool for data orchestration.\
When pipelines goes down, sensors should be able to detect the failure and trigger alerts or retries. \


Author: [Protim Roy](https://www.protimroy.com) with help from some LLM \
Date: 2025-04-08

```
Tags: dagster, python, data engineering, data orchestration, ubuntu, systemd, tailscale
```