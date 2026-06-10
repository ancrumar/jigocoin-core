# Jigocoin Network Topology

## Overview

The Jigocoin network is composed of multiple independently operated nodes providing consensus, mining, relay and infrastructure services.

The objective of the topology is to maximize resilience, redundancy and decentralization while maintaining operational simplicity.

## Public Relay Layer

### Node 21 (Google Cloud)

Role:

* Public relay node
* External connectivity
* Peer discovery support

Host:

34.10.226.240

Characteristics:

* No mining wallet
* Public-facing connectivity
* Infrastructure relay service

## Core Infrastructure

### HPBlanco

Primary infrastructure node.

Services:

* Node 1
* Node 2 (Docker)
* Node 3 (Docker)
* Block Explorer
* Redmine
* MariaDB
* Monitoring services

Functions:

* Consensus participation
* Mining
* Infrastructure hosting
* Network monitoring

### ASUS

Secondary infrastructure node.

Services:

* Node 11
* Node 12 (Docker)
* Node 13 (Docker)

Functions:

* Consensus participation
* Mining
* Redundant network presence

### HHCloud

External infrastructure node.

Services:

* Dedicated RPC node
* Mining services

Functions:

* Independent network participation
* External connectivity
* Additional mining capacity

## Active Mining Nodes

Current mining infrastructure includes:

* HPBlanco (Node 1)
* ASUS (Node 11)
* HHCloud

Mining is distributed across multiple physical locations to improve resilience and network continuity.

## Consensus Monitoring

Consensus health is monitored through independent node comparison.

Monitoring objectives:

* Detect chain divergence
* Detect synchronization failures
* Verify block propagation
* Verify peer connectivity

## Design Principles

The topology follows the principles of:

### Seiryoku Zenyo

Efficient use of computing, storage and network resources.

### Jita Kyoei

Mutual cooperation between infrastructure operators for the benefit of the network as a whole.

## Future Direction

Future network growth should prioritize:

* Additional independent node operators
* Geographic distribution
* Increased mining decentralization
* Redundant public relay infrastructure
* Improved monitoring and observability
