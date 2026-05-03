# Jigocoin Networking Guide

This document describes the networking requirements and compatibility details specific to Jigocoin.

---

# P2P Transport Compatibility (V1 vs V2)

## Current Requirement

Jigocoin currently requires **P2P Transport V1** compatibility.

Modern Bitcoin-derived software supports **P2P V2 transport (BIP324)**, which may be enabled automatically.

If V2 transport is used while peers only support V1, nodes may connect but **fail to synchronize**.

---

## Required Configuration

Add this line to:

```text
~/.jigocoin/jigocoin.conf
```

```ini
v2transport=0
```

Restart the node after modifying the configuration.

---

## Symptoms of V2 Incompatibility

Typical symptoms include:

* Peers appear in:

```bash
jigocoin-cli getpeerinfo
```

But:

```bash
jigocoin-cli getblockchaininfo
```

Shows:

```text
blocks = 0
```

Or:

```text
"version": 0
"transport_protocol_type": "detecting"
```

---

# Network Ports

## Mainnet

| Service | Port      |
| ------- | --------- |
| P2P     | **19335** |
| RPC     | **30462** |

---

# Seed Nodes

Current public seed:

```ini
addnode=34.10.226.240:19335
```

Additional seeds will be added as the network expands.

---

# Example Node Configuration

```ini
server=1
daemon=1

rpcuser=jigouser
rpcpassword=strongpassword

rpcport=30462
port=19335

v2transport=0

addnode=34.10.226.240:19335
```

---

# Firewall Configuration

Ensure the P2P port is open:

```bash
sudo ufw allow 19335/tcp
```

Verify:

```bash
sudo ufw status
```

---

# Multiple Node Setup

If running multiple nodes on the same machine, use different ports:

```ini
port=19337
rpcport=30463
```

---

# Summary

To ensure correct network operation:

✔ Use correct P2P port
✔ Add at least one seed node
✔ Disable V2 transport
✔ Verify firewall configuration
✔ Confirm peers are syncing
