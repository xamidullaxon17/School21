1. run qilish:
    ```
    ./main.sh
    ```
- agar ishga tushmasa:
- `sudo systemctl daemon-reload`
- `sudo systemctl enable promethues`
- `sudo systemctl start promethues`

1. **Prometheus ishlayotganini terminalda tekshirish:**
    - `sudo systemctl status prometheus`
    - Prometheus ishlaganini tekshirish: localhost:ip
    - `http://10.0.2.15:9090`

2. **Grafana ishlayotganini terminalda tekshirish:**
    - `sudo systemctl status grafana-server`
    - Grafana ishlaganini tekshirish: localhost:ip
    - `http://10.0.2.15:3000`

3. **Node exporter ishlayotganini terminalda tekshirish:**
    - `sudo systemctl status node_exporter`
    - Node exporter ishlaganini tekshirish: localhost:ip
    - `http://10.0.2.15:3000`

