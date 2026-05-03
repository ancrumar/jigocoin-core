# Jigocoin Seed Node Setup (Docker)

This guide describes how to deploy a Jigocoin seed node using Docker.

Seed nodes are critical infrastructure components that allow new nodes to discover peers and join the network.

---

# Seed Node Role

A seed node:

* Accepts inbound P2P connections
* Remains online continuously
* Provides peer discovery for new nodes
* Helps bootstrap network connectivity

Seed nodes should:

✔ Run 24/7
✔ Have a static public IP
✔ Have open P2P ports

---

# Network Requirements

## Required Ports

| Service | Port      |
| ------- | --------- |
| P2P     | **19335** |

Open firewall:

```bash
sudo ufw allow 19335/tcp
```

Verify:

```bash
sudo ufw status
```

---

# Directory Structure

Example:

```text
/home/user/node8/
 ├── bitcoin.conf
 ├── blocks/
 ├── chainstate/
 └── wallets/
```

---

# Example Configuration File

Create:

```bash
nano ~/node8/bitcoin.conf
```

Example:

```ini
server=1
listen=1

rpcuser=jigocoin
rpcpassword=jigocoinpass

port=19335
rpcport=30462

txindex=1

# Required for network compatibility
v2transport=0

# Known nodes
addnode=34.10.226.240:19335
```

---

# Docker Deployment

## Run Seed Node Container

Example:

```bash
docker run -d \
  --name jigocoin-node8 \
  -v ~/node8:/data \
  -p 19335:19335 \
  jigocoin-node \
  /opt/jigocoin/build/bin/jigocoind \
    -conf=/data/bitcoin.conf \
    -datadir=/data \
    -printtoconsole
```

---

# Verify Seed Operation

Check container:

```bash
docker ps
```

Check logs:

```bash
docker logs jigocoin-node8
```

Check peers:

```bash
docker exec jigocoin-node8 \
  /opt/jigocoin/build/bin/jigocoin-cli \
  -conf=/data/bitcoin.conf \
  getpeerinfo
```

Expected:

```text
Multiple connected peers
```

---

# Testing Connectivity

From another node:

```bash
nc -vz 34.10.226.240 19335
```

Expected:

```text
Connection succeeded
```

---

# Adding Seed to Client Nodes

Client configuration:

```ini
addnode=34.10.226.240:19335
v2transport=0
```

---

# Best Practices

Recommended:

✔ Static public IP
✔ Reliable internet connection
✔ SSD storage
✔ Automatic restart policy
✔ Monitoring enabled

---

# Optional: Docker Restart Policy

Enable auto-restart:

```bash
docker update --restart unless-stopped jigocoin-node8
```

---

# Multiple Seed Nodes

For redundancy, deploy additional seeds on separate servers.

Example:

```ini
addnode=34.10.226.240:19335
addnode=81.xxx.xxx.xxx:19335
addnode=91.xxx.xxx.xxx:19335
```

Multiple seeds improve network resilience.

---

# Security Recommendations

Recommended:

✔ Use firewall rules
✔ Restrict RPC access
✔ Avoid exposing RPC port publicly
✔ Monitor logs regularly

---

# Summary

A proper seed node:

✔ Runs in Docker
✔ Has open P2P port
✔ Uses V1 transport
✔ Remains online continuously
✔ Accepts inbound connections

Seed nodes are critical for network growth and reliability.
