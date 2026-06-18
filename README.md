
[![Apache License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/OT-OSM/tempo)
[![Ansible](https://img.shields.io/badge/Ansible-Role-red.svg)](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%2020.04%20%7C%2022.04-orange.svg)](https://ubuntu.com)

[![Opstree Solutions][opstree_avatar]][opstree_homepage]<br/>[Opstree Solutions][opstree_homepage]

[opstree_homepage]: https://opstree.github.io/
[opstree_avatar]: https://img.cloudposse.com/150x150/https://github.com/opstree.png

---

# Alert-Manager — Ansible Role

A production-grade Ansible role to install, configure, and manage **Grafana Tempo** on Ubuntu systems. Tempo is an open-source, high-scale distributed tracing backend that ingests traces from instrumented applications via OTLP, Jaeger, Zipkin, or other protocols, and integrates natively with Grafana for trace visualization.

## Key Features

- [x] Installs Tempo from official Grafana GitHub releases
- [x] Supports architecture-specific binary selection (e.g. `linux_amd64`, `linux_arm64`)
- [x] Creates a dedicated system user and group for security isolation
- [x] Configures Tempo via Jinja2 templates
- [x] Manages service lifecycle using Ansible handlers
- [x] Idempotent — safe to re-run without side effects
- [x] All variables are role-namespaced to avoid conflicts

---

## Requirements

| Requirement | Details |
|-------------|---------|
| **OS** | Ubuntu `focal` (20.04) or `jammy` (22.04) |
| **Privileges** | Root or sudo access on target hosts |
| **Ansible Collection** | `community.general` |

Install the required collection:

```bash
ansible-galaxy collection install community.general
```

> **Security Note:** Sensitive defaults are placeholders in `defaults/main.yml`.  
> Always override secrets via **Semaphore environment variables** or **Ansible Vault** — never commit credentials to source control.

---

## Role Structure

```
tempo/
├── tasks/
│   └── main.yml               # Main task entry point
│   └── install.yml
│   └── service.yml
│   └── config.yml
|   └── config.yml          
├── handlers/
│   └── main.yml
├── vars/
│   └── main.yml
├── defaults/
│   └── main.yml
├── meta/
│   └── main.yml                    # Service restart / reload handlers
└── templates/
    ├── tempo.yaml.j2             # Main Tempo configuration template
    └── tempo.service.j2          # Jinja2 systemd unit template
```

---

## File Descriptions

### `tasks/main.yml`

Orchestrates all installation and configuration steps:

1. Create dedicated `tempo` system user and group
2. Create data, WAL, and configuration directories with correct ownership
3. Download the Tempo binary archive from Grafana GitHub releases for the target architecture
4. Extract and install the binary to the system PATH
5. Render and deploy the Tempo config and systemd unit from templates
6. Enable and start the `tempo` service

### `handlers/main.yml`

Triggered automatically when configuration changes are detected:

- **`restart tempo`** — restarts the Tempo service
- **`reload systemd`** — reloads the systemd daemon after service file updates

### `templates/tempo.yaml.j2`

Jinja2 template that renders the main Tempo configuration installed to `/etc/tempo/tempo.yaml`. Defines the server, distributor, ingester, compactor, storage backend, and receiver protocol sections using role variables.

### `templates/tempo.service.j2`

Jinja2 template that renders the systemd unit file installed to `/etc/systemd/system/tempo.service`. References the configuration file path and runs Tempo under the dedicated service user.

---

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `tempo_version` | `2.4.1` | Version of Tempo to install |
| `tempo_arch` | `linux_amd64` | Target architecture for the binary download (`linux_amd64`, `linux_arm64`) |
| `tempo_user` | `tempo` | System user that runs the service |
| `tempo_group` | `tempo` | System group for the service user |
| `tempo_http_port` | `3200` | Port for the Tempo HTTP API and health endpoint |
| `tempo_grpc_port` | `9095` | Port for the Tempo gRPC API |
| `tempo_otlp_grpc_port` | `4317` | Port to receive traces via OTLP gRPC |
| `tempo_otlp_http_port` | `4318` | Port to receive traces via OTLP HTTP |
| `tempo_config_dir` | `/etc/tempo` | Directory for configuration files |
| `tempo_data_dir` | `/var/lib/tempo` | Directory for persistent trace data and WAL |
| `tempo_install_dir` | `/usr/local/bin` | Directory for the installed binary |
| `tempo_storage_backend` | `local` | Storage backend to use (`local`, `s3`, `gcs`, `azure`) |
| `tempo_retention_duration` | `720h` | How long to retain trace data (default 30 days) |

> Override any variable in your playbook, inventory, or via `--extra-vars`.

---

## Usage

### Quick Start

```bash
ansible-playbook -i inventory playbook.yml
```

### Run Specific Phases

```bash
# Install binary only
ansible-playbook -i inventory playbook.yml --tags install

# Configure service only
ansible-playbook -i inventory playbook.yml --tags configure

# Restart service only
ansible-playbook -i inventory playbook.yml --tags service
```

### Example Playbook

```yaml
---
- name: Deploy Grafana Tempo
  hosts: tracing_servers
  become: true
  roles:
    - role: tempo
      vars:
        tempo_version: "2.4.1"
        tempo_arch: "linux_amd64"
        tempo_user: "tempo"
        tempo_group: "tempo"
        tempo_http_port: 3200
        tempo_storage_backend: "local"
        tempo_retention_duration: "720h"
```

---

## Tags

| Tag | Description |
|-----|-------------|
| `install` | Download and install the Tempo binary |
| `configure` | Render and deploy all configuration templates |
| `service` | Start, stop, or restart the service |

---

## Handlers

| Handler | Trigger Condition | Action |
|---------|------------------|--------|
| `restart tempo` | Config or binary change | Restarts the Tempo service |
| `reload systemd` | Service unit file updated | Reloads the systemd daemon |

---

## Templates

| Template | Destination | Description |
|----------|-------------|-------------|
| `tempo.yaml.j2` | `/etc/tempo/tempo.yaml` | Main Tempo pipeline configuration (server, ingester, storage, receivers) |
| `tempo.service.j2` | `/etc/systemd/system/tempo.service` | Systemd service definition |

---

## Verification

After running the playbook, confirm Tempo is running correctly.

### Check service status

```bash
systemctl status tempo
```

### Verify the HTTP API is reachable

```bash
curl -s http://localhost:3200/ready
```

Expected output:

```
ready
```

### Check overall health

```bash
curl -s http://localhost:3200/status
```

Expected output (summary):

```
Tempo is up and ready to receive traces
```

### Confirm all listening ports

```bash
ss -tulpn | grep tempo
```

Expected output:

```
LISTEN   0   4096   *:3200   *:*   users:(("tempo",pid=XXXX,fd=3))
LISTEN   0   4096   *:4317   *:*   users:(("tempo",pid=XXXX,fd=4))
LISTEN   0   4096   *:4318   *:*   users:(("tempo",pid=XXXX,fd=5))
```

### Send a test trace via OTLP HTTP

```bash
curl -s -X POST http://localhost:4318/v1/traces \
  -H "Content-Type: application/json" \
  -d '{"resourceSpans": []}'
```

Expected output:

```json
{}
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Service fails to start | Config YAML syntax error | Run `tempo -config.file=/etc/tempo/tempo.yaml` manually to see the error |
| Port conflict on 4317/4318 | Another OTLP receiver already running | Change `tempo_otlp_grpc_port` / `tempo_otlp_http_port` or stop the conflicting process |
| Traces not appearing in Grafana | Grafana datasource URL wrong | Set the Tempo datasource URL to `http://<host>:3200` in Grafana |
| Data directory permission error | Wrong ownership on data dir | Ensure `tempo_data_dir` is owned by `tempo_user` |
| High disk usage | Retention period too long | Reduce `tempo_retention_duration` (e.g. `168h` for 7 days) |
| Binary not found after install | Wrong architecture selected | Verify `tempo_arch` matches the target host (`uname -m`) |
| `systemctl` not found | Non-systemd system | This role requires systemd — not supported on older init systems |

---

## References

| Resource | Link |
|----------|------|
| Grafana Tempo Official Documentation | https://grafana.com/docs/tempo/latest/ |
| Tempo GitHub | https://github.com/grafana/tempo |
| Tempo Configuration Reference | https://grafana.com/docs/tempo/latest/configuration/ |
| OpenTelemetry Protocol (OTLP) | https://opentelemetry.io/docs/specs/otel/protocol/ |
| Ansible Roles Documentation | https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html |
| Ansible Handlers Documentation | https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html |

---

## Authors

| Name | Email | Organization |
|------|-------|-------------|
| Abhishek Vishwakarma | abhishek.vishwakarma@opstree.com | Opstree Solutions |
| Shubham Rathi | shubham.rathi@mygurukulam.co | MyGurukulam |

---

## License

This project is licensed under the [Apache 2.0 License](LICENSE).
