<p align="center">
  <img src="assets/logo/jigocoin-logo.png" width="220">
</p>

<h1 align="center">Jigocoin</h1>

<p align="center">
Digital currency inspired by the principles of Judo:
<strong>Seiryoku Zenyo</strong> (Maximum Efficient Use of Energy)
and
<strong>Jita Kyoei</strong> (Mutual Welfare and Benefit).
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/ancrumar/jigocoin-core?display_name=tag" alt="Release">
  <img src="https://img.shields.io/github/license/ancrumar/jigocoin-core" alt="License">
</p>

---

# Jigocoin Core

Jigocoin is a decentralized peer-to-peer digital currency operating on its own blockchain and consensus network.

This repository contains the reference implementation of the Jigocoin protocol.

Jigocoin enables users to transfer value directly between participants without requiring a central authority, while promoting efficiency, resilience and mutual benefit.

---

## Philosophy

Jigocoin is inspired by the two foundational principles established by Jigoro Kano, founder of Judo:

## Visual Identity

The Jigocoin logo is inspired by the history, philosophy and symbolism of Judo.

The letter **J** represents:

- Jigocoin
- Judo
- Professor Jigoro Kano

The black color symbolizes the **Kuro Obi** (black belt), representing the journey from learning to mastery.

The two bars symbolize the knot of the black belt and the two founding principles of Judo:

- Seiryoku Zenyo
- Jita Kyoei

The green and red background reflects the traditional colors of classical Judo competition tatami.

For a complete explanation see:

[Logo Meaning](assets/branding/logo-meaning.md)

### Seiryoku Zenyo (精力善用)

**Maximum Efficient Use of Energy**

Resources should be used intelligently and efficiently to achieve the greatest possible benefit with the least waste.

### Jita Kyoei (自他共栄)

**Mutual Welfare and Benefit**

Individual success and collective success are interconnected. A healthy network benefits all participants.

These principles guide both the technical design and the long-term governance of the project.

---

## Project Documentation

| Document | Description |
|-----------|-------------|
| `docs/whitepaper.md` | Technical and economic overview |
| `docs/philosophy.md` | Philosophical foundations |
| `GOVERNANCE.md` | Governance framework |
| `ROADMAP.md` | Development roadmap |
| `NETWORK-TOPOLOGY.md` | Current network topology |
| `INCIDENTS.md` | Incident registry and lessons learned |
| `SECURITY.md` | Security policy |

---

## Network Parameters

| Parameter | Value |
|------------|--------|
| Name | Jigocoin |
| Symbol | JGC |
| Consensus | Proof of Work |
| Blockchain | Independent |
| Bech32 Prefix | jgc |
| Reference Client | Jigocoin Core |

For detailed technical parameters see:

- `docs/network-parameters.md`
- `docs/chain-identity.md`
- `docs/monetary-policy.md`

---

## Current Status

### Stable Release

**v31.99.1 – Identity Cleanup Baseline**

This release establishes the first stable baseline of Jigocoin with:

- Independent project identity.
- Governance framework.
- Public roadmap.
- Incident management process.
- Network topology documentation.
- Project philosophy and whitepaper.
- Reorganization of inherited upstream documentation.

This release introduces **no consensus changes**, **no monetary policy changes** and **no blockchain migration requirements**.

---

## Building From Source

### Linux

See:

- `docs/build-instructions.md`

### Node Deployment

See:

- `docs/node-setup.md`

---

## Repository Structure

```text
assets/                 Branding assets and logos
docs/                   Project documentation
doc/upstream/           Archived upstream Bitcoin Core documentation
src/                    Reference implementation
test/                   Test suite
```

## Governance

Project governance is documented in:

```text
GOVERNANCE.md
```

Development priorities are documented in:

```text
ROADMAP.md
```

Operational incidents are recorded in:

```text
INCIDENTS.md
```

---

## Network Infrastructure

The current network architecture and node topology are documented in:

```text
NETWORK-TOPOLOGY.md
```

This document is updated as the network evolves.

---

## Security

To report a vulnerability, please consult:

```text
SECURITY.md
```

Please do not disclose security vulnerabilities publicly before responsible disclosure procedures have been followed.

---

## License

Jigocoin Core is released under the MIT License.

See:

```text
COPYING
```

for the full license text.

---

## Acknowledgements

Jigocoin is built upon open-source technologies and benefits from the work of countless contributors in the broader cryptocurrency ecosystem.

Historical upstream Bitcoin Core documentation has been preserved under:

```text
doc/upstream/
```

to maintain technical traceability while allowing Jigocoin to develop its own independent identity.
