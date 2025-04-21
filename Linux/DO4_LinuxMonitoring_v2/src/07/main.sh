#!/bin/bash

# Prometheus o‘rnatish
PROM_VERSION="2.32.1"
sudo useradd --system --no-create-home --shell /bin/false prometheus
sudo apt install -y wget tar

wget https://github.com/prometheus/prometheus/releases/download/v${PROM_VERSION}/prometheus-${PROM_VERSION}.linux-amd64.tar.gz
tar -xvf prometheus-${PROM_VERSION}.linux-amd64.tar.gz
cd prometheus-${PROM_VERSION}.linux-amd64

sudo mkdir -p /data /etc/prometheus
sudo mv prometheus promtool /usr/local/bin/
sudo mv consoles console_libraries /etc/prometheus/
sudo chown -R prometheus:prometheus /etc/prometheus /data

# prometheus.yml fayli
cat <<EOF | sudo tee /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node"
    static_configs:
      - targets: ["10.0.2.15:9100"]
EOF

sudo chown prometheus:prometheus /etc/prometheus/prometheus.yml

# Prometheus systemd servisi
cat <<EOF | sudo tee /etc/systemd/system/prometheus.service
[Unit]
Description=Prometheus Monitoring
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \\
  --config.file=/etc/prometheus/prometheus.yml \\
  --storage.tsdb.path=/data \\
  --web.console.templates=/etc/prometheus/consoles \\
  --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
EOF

# Prometheusni ishga tushurish
sudo systemctl daemon-reload
sudo systemctl enable prometheus
sudo systemctl start prometheus
sudo systemctl status prometheus --no-pager

# Node Exporter o‘rnatish
NODE_VERSION="1.3.1"
sudo useradd --system --no-create-home --shell /bin/false node_exporter

wget https://github.com/prometheus/node_exporter/releases/download/v${NODE_VERSION}/node_exporter-${NODE_VERSION}.linux-amd64.tar.gz
tar -xvf node_exporter-${NODE_VERSION}.linux-amd64.tar.gz
sudo mv node_exporter-${NODE_VERSION}.linux-amd64/node_exporter /usr/local/bin/
sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter

# Node Exporter systemd servisi
cat <<EOF | sudo tee /etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

# Node Exporterni ishga tushirish
sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter
sudo systemctl status node_exporter --no-pager

# Grafana o‘rnatish
sudo apt-get install -y apt-transport-https software-properties-common wget adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_9.4.3_amd64.deb
sudo dpkg -i grafana_9.4.3_amd64.deb
sudo apt-get update && sudo apt-get -y install grafana

# Grafanani ishga tushurish
sudo systemctl daemon-reload
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
sudo systemctl status grafana-server --no-pager

# Firewalld (agar kerak bo‘lsa)
sudo apt install -y firewalld
sudo systemctl start firewalld
sudo firewall-cmd --zone=public --add-port=3000/tcp --permanent
sudo systemctl reload firewalld

# Stress test uchun
sudo apt install -y stress
stress -c 2 -i 1 -m 1 --vm-bytes 32M -t 10s

# Ortiqcha fayllarni o‘chirish
cd ..
sudo rm -rf prometheus-${PROM_VERSION}.linux-amd64*
sudo rm -rf node_exporter-${NODE_VERSION}.linux-amd64*
sudo rm -f grafana_9.4.3_amd64.deb
