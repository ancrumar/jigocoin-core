# Jigocoin Core

Jigocoin is a decentralized peer-to-peer digital currency derived from Bitcoin Core.

This repository contains the reference implementation of the Jigocoin protocol.

Jigocoin allows users to send payments directly to each other without relying on a central authority.

---

# 🚀 Build Jigocoin from Source

## System Requirements

Recommended:

* Linux (Ubuntu 22.04+ or Debian 12+)
* 4 GB RAM minimum
* 20+ GB disk space

---

## Install Dependencies (Ubuntu / Debian)

```bash
sudo apt update

sudo apt install -y \
  build-essential \
  cmake \
  pkg-config \
  libevent-dev \
  libboost-dev \
  libboost-system-dev \
  libboost-filesystem-dev \
  libboost-test-dev \
  libsqlite3-dev
```

---

## Clone Repository

```bash
git clone https://github.com/ancrumar/jigocoin-core.git

cd jigocoin-core
```

---

## Build Jigocoin

```bash
mkdir build

cd build

cmake .. -DENABLE_IPC=OFF

make -j$(nproc)
```

After compilation, binaries will be located in:

```text
build/bin/jigocoind
build/bin/jigocoin-cli
build/bin/jigocoin-wallet
build/bin/jigocoin-util
build/bin/jigocoin-tx
```

---

# 🧱 Run a Jigocoin Node

## Create Data Directory

```bash
mkdir ~/.jigocoin
```

---

## Create Configuration File

```bash
nano ~/.jigocoin/jigocoin.conf
```

Example configuration:

```ini
server=1
daemon=1

rpcuser=jigouser
rpcpassword=strongpassword

rpcport=30462
port=19335

# Primary seed node
addnode=34.10.226.240:19335
```

---

## Start Node

```bash
./build/bin/jigocoind \
  -datadir=$HOME/.jigocoin \
  -daemon
```

---

## Verify Node Status

Check blockchain:

```bash
./build/bin/jigocoin-cli \
  -datadir=$HOME/.jigocoin \
  getblockchaininfo
```

Check peers:

```bash
./build/bin/jigocoin-cli \
  -datadir=$HOME/.jigocoin \
  getpeerinfo
```

---

# 🌐 Network Parameters

## Mainnet

| Parameter     | Value                   |
| ------------- | ----------------------- |
| Network       | mainnet                 |
| P2P Port      | **19335**               |
| RPC Port      | **30462**               |
| Bech32 Prefix | **jgc**                 |
| Message Start | **0x4a 0x47 0x43 0x31** |

---

# 🌱 Seed Nodes

The following public node is available for initial synchronization:

```ini
addnode=34.10.226.240:19335
```

More seed nodes will be added as the network expands.

---

# 💼 Wallet Usage

Create a wallet:

```bash
jigocoin-cli createwallet "wallet01"
```

Generate a new address:

```bash
jigocoin-cli getnewaddress
```

Backup wallet:

```bash
jigocoin-cli backupwallet backup.dat
```

---

# 🛠 Troubleshooting

## Node does not connect to peers

Run:

```bash
jigocoin-cli getpeerinfo
```

If no peers appear:

Check:

* Port **19335** is open
* Firewall allows incoming connections
* Seed node reachable
* Internet connection active

---

## Node connects but does not synchronize (stuck at block 0)

If peers appear in `getpeerinfo` but the node remains stuck at **block 0**, the cause is usually **P2P transport version incompatibility**.

Modern Bitcoin-derived nodes may attempt to use **P2P V2 transport**, while Jigocoin currently requires **V1 transport**.

Add this line to your configuration file:

```ini
v2transport=0
```

Example:

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

After adding this option, restart the node.

This resolves the most common synchronization failure in new installations.


---

## RPC connection problems

Verify:

```ini
rpcport=30462
```

File:

```text
~/.jigocoin/jigocoin.conf
```

---

## Port already in use

Change RPC port:

```ini
rpcport=30463
```

---

# 🔐 Security Recommendations

Always:

* Backup wallets regularly
* Use strong RPC credentials
* Protect wallet files
* Do not expose RPC port publicly

---

# 🧪 Development Notes

Jigocoin Core is based on Bitcoin Core.

Changes from upstream Bitcoin Core are progressively applied to create an independent network implementation.

---

# 📜 License

Jigocoin Core is released under the terms of the MIT License.

See:

COPYING

This software is based on Bitcoin Core.

---

# 📚 Additional Documentation

For advanced networking details, see:

- `doc/jigocoin-networking.md`
- `doc/jigocoin-seed-node.md`
