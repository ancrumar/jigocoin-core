#!/usr/bin/env python3

import subprocess
import json
import sys
import os

# ==========================================
# CONFIGURACIÓN
# ==========================================

CLI = "nodo1"
WALLET = "miner01"

MINING_ADDRESS = "jgc1qhunsrpechm7uudqn0c352yqaj0v78we2n7acw0"

DATE = "2026-04-24"

# Mensaje definitivo compacto

MESSAGE = (
    "JGC-0001 mine-node2 bad addr "
    "jgc1qet...nj9l6v "
    "fixed 2026-04-24 burn"
)

# ==========================================
# VALIDAR TAMAÑO
# ==========================================

if len(MESSAGE) > 80:
    print("❌ ERROR: mensaje demasiado largo")
    sys.exit(1)

HEX_MESSAGE = MESSAGE.encode().hex()

# ==========================================
# FUNCION EJECUCION
# ==========================================

def run(cmd):

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        print("❌ ERROR ejecutando:")
        print(" ".join(cmd))
        print(result.stderr)

        sys.exit(1)

    return result.stdout.strip()

# ==========================================
# MAIN
# ==========================================

print("\n=== JIGOCOIN INCIDENT RECORDER ===\n")

print("📜 Mensaje:")
print(MESSAGE)
print()

# Crear TX con OP_RETURN

raw_tx = run([
    CLI,
    "-rpcwallet=" + WALLET,
    "createrawtransaction",
    "[]",
    f'{{"data":"{HEX_MESSAGE}"}}'
])

print("✔ Raw TX creada")

# Añadir fondos automáticamente

funded = run([
    CLI,
    "-rpcwallet=" + WALLET,
    "fundrawtransaction",
    raw_tx
])

funded_json = json.loads(funded)

funded_hex = funded_json["hex"]

print("✔ TX financiada")

# Firmar

signed = run([
    CLI,
    "-rpcwallet=" + WALLET,
    "signrawtransactionwithwallet",
    funded_hex
])

signed_json = json.loads(signed)

if not signed_json["complete"]:
    print("❌ ERROR: firma incompleta")
    sys.exit(1)

signed_hex = signed_json["hex"]

print("✔ TX firmada")

# Enviar

txid = run([
    CLI,
    "sendrawtransaction",
    signed_hex
])

print(f"📡 TX enviada: {txid}")

# Minar bloque

run([
    CLI,
    "-rpcwallet=" + WALLET,
    "generatetoaddress",
    "1",
    MINING_ADDRESS
])

print("⛏️ Bloque minado")

# ==========================================
# LOG LOCAL
# ==========================================

docs_path = "/home/ancrumar/jigocoin/docs"

os.makedirs(docs_path, exist_ok=True)

log_file = os.path.join(
    docs_path,
    "incident_log.txt"
)

log_line = (
    f"{DATE} | "
    f"JGC-0001 | "
    f"TXID {txid}\n"
)

with open(log_file, "a") as f:
    f.write(log_line)

print(f"📄 Log guardado: {log_file}")

print("\n=== INCIDENTE REGISTRADO ===\n")
