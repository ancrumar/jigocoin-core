# Jigocoin Address Format / Formato de Direcciones de Jigocoin

---

# Overview / Descripción General

**EN**

This document defines the address formats used in the Jigocoin network.

Modern Jigocoin wallets use Bech32 addresses as the standard format.

**ES (España)**

Este documento define los formatos de direcciones utilizados en la red Jigocoin.

Las wallets modernas de Jigocoin utilizan direcciones Bech32 como formato estándar.

---

# Recommended Address Format (Primary)

## Bech32 (SegWit)

**Mainnet HRP:**

jgc

**Example:**

jgc1qx283denmtnl3cjyu6uwaj4yw0e9r67nf96gx68

**EN**

Bech32 addresses are the recommended standard.

They reduce transaction size and improve error detection.

**ES**

Las direcciones Bech32 son el estándar recomendado.

Reducen el tamaño de las transacciones y mejoran la detección de errores.

---

# Legacy Address Support

## P2PKH (Legacy)

Decimal Prefix:

0

Typical Format:

1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

**EN**

Legacy addresses are supported for compatibility but are not recommended.

**ES**

Las direcciones legacy se mantienen por compatibilidad, pero no se recomiendan.

---

## P2SH

Decimal Prefix:

5

Typical Format:

3xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

---

# Private Key Format (WIF)

Decimal Prefix:

128

Typical Prefix:

5 / K / L

---

# Test Networks

## Testnet

Bech32:

tjgc

---

## Signet

Bech32:

sjgc

---

## Regtest

Bech32:

bcrt

---

# Address Encoding

Supported Types:

P2WPKH
P2PKH
P2SH

Encodings:

Bech32
Base58Check

---

# Address Recommendation

**Official Jigocoin address format:**

Bech32

Prefix:

jgc1

**Example:**

jgc1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

---

# Summary / Resumen

Primary Address Format:

Bech32 (SegWit)

Mainnet Prefix:

jgc

Recommended Usage:

Bech32 only

Legacy Support:

Yes (not recommended)
