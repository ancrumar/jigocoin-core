# Jigocoin Node Setup / Configuración de Nodos Jigocoin

---

# Overview / Descripción General

**EN**

This document explains how to configure and run Jigocoin nodes.

It includes basic configuration, peer connection, and multi-node setup examples.

**ES (España)**

Este documento explica cómo configurar y ejecutar nodos Jigocoin.

Incluye configuración básica, conexión entre nodos y ejemplos de redes con múltiples nodos.

---

# Basic Node Setup / Configuración Básica

## Create Data Directory

```bash
mkdir -p ~/.jigocoin
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

listen=1

port=19335
rpcport=19332

rpcuser=jigocoin
rpcpassword=strongpassword

txindex=1

fallbackfee=0.0001
```

---

# Start Node / Iniciar Nodo

```bash
bitcoind -daemon
```

Check status:

```bash
bitcoin-cli getblockcount
```

---

# Stop Node / Detener Nodo

```bash
bitcoin-cli stop
```

---

# Peer Connections / Conexión entre Nodos

Nodes can connect manually using:

```bash
bitcoin-cli addnode IP_ADDRESS:19335 add
```

Example:

```bash
bitcoin-cli addnode 192.168.1.10:19335 add
```

---

# Multi-Node Local Network Example

**EN**

This example shows a simple 2-node local network.

**ES**

Este ejemplo muestra una red local simple de 2 nodos.

---

## Node 1 Configuration

```ini
port=19335
rpcport=19332

rpcuser=node1
rpcpassword=password1

listen=1
server=1
daemon=1
```

---

## Node 2 Configuration

```ini
port=19336
rpcport=19333

rpcuser=node2
rpcpassword=password2

listen=1
server=1
daemon=1

addnode=127.0.0.1:19335
```

---

# Docker Node Example

**EN**

Example command to run a Jigocoin node using Docker.

**ES**

Ejemplo de ejecución de un nodo Jigocoin usando Docker.

```bash
docker run -d \
--name jigocoin-node \
-p 19335:19335 \
-p 19332:19332 \
-v jigocoin-data:/data \
jigocoin-node
```

---

# Node Synchronization / Sincronización del Nodo

Check synchronization status:

```bash
bitcoin-cli getblockchaininfo
```

Look for:

```text
"blocks"
"headers"
```

When both values match, the node is synchronized.

---

# Node Networking / Red de Nodos

Check connected peers:

```bash
bitcoin-cli getpeerinfo
```

Check connection count:

```bash
bitcoin-cli getconnectioncount
```

---

# Recommended Settings / Configuración Recomendada

```ini
txindex=1
fallbackfee=0.0001

maxconnections=40

listen=1
server=1
daemon=1
```

---

# Firewall Configuration / Configuración de Firewall

Allow Jigocoin port:

```bash
sudo ufw allow 19335/tcp
```

Reload firewall:

```bash
sudo ufw reload
```

---

# Node Health Checks / Verificación del Nodo

Check block height:

```bash
bitcoin-cli getblockcount
```

Check mempool:

```bash
bitcoin-cli getmempoolinfo
```

Check mining status:

```bash
bitcoin-cli getmininginfo
```

---

# Backup Recommendations / Recomendaciones de Copia de Seguridad

Backup wallet:

```bash
bitcoin-cli backupwallet backup.dat
```

Store backups:

* Offline
* Multiple locations

---

# Summary / Resumen

Node setup includes:

1. Create configuration
2. Start node
3. Connect peers
4. Sync blockchain
5. Monitor node

This allows Jigocoin to operate as a decentralized network.

Esto permite que Jigocoin funcione como una red descentralizada.
