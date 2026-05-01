# Jigocoin Build Instructions / Instrucciones de Compilación de Jigocoin

---

# Overview / Descripción General

**EN**

This document explains how to build Jigocoin from source code.

It includes dependency installation, compilation steps, and verification procedures.

**ES (España)**

Este documento explica cómo compilar Jigocoin desde el código fuente.

Incluye la instalación de dependencias, pasos de compilación y verificación.

---

# Supported Platforms / Plataformas Soportadas

**EN**

Primary supported platform:

Linux (Ubuntu recommended)

Other platforms may be supported but are not officially documented here.

**ES**

Plataforma principal soportada:

Linux (Ubuntu recomendado)

Otras plataformas pueden funcionar, pero no están documentadas oficialmente aquí.

---

# System Requirements / Requisitos del Sistema

**EN**

Minimum requirements:

* CPU: 2 cores
* RAM: 4 GB
* Storage: 20 GB free space
* OS: Ubuntu 22.04 or later

Recommended:

* CPU: 4+ cores
* RAM: 8 GB+
* Storage: SSD recommended

**ES**

Requisitos mínimos:

* CPU: 2 núcleos
* RAM: 4 GB
* Almacenamiento: 20 GB libres
* SO: Ubuntu 22.04 o posterior

Recomendado:

* CPU: 4+ núcleos
* RAM: 8 GB o más
* Almacenamiento: SSD recomendado

---

# Install Dependencies / Instalar Dependencias

Run:

```bash
sudo apt update
sudo apt install -y \
build-essential \
libtool \
autotools-dev \
automake \
pkg-config \
bison \
flex \
libevent-dev \
libboost-dev \
libboost-system-dev \
libboost-filesystem-dev \
libboost-thread-dev \
libsqlite3-dev \
libminiupnpc-dev \
libnatpmp-dev \
libzmq3-dev \
libssl-dev
```

---

# Clone Repository / Clonar Repositorio

```bash
git clone https://github.com/YOUR_USERNAME/jigocoin.git
cd jigocoin
```

Replace:

YOUR_USERNAME

with the actual repository owner.

---

# Build Jigocoin / Compilar Jigocoin

```bash
./autogen.sh
./configure
make -j$(nproc)
```

Compilation may take several minutes.

---

# Verify Build / Verificar Compilación

Check binary:

```bash
./src/bitcoind --version
```

Expected output:

Jigocoin version X.X.X

---

# Optional: Install System-wide

```bash
sudo make install
```

This installs binaries globally.

---

# Running Jigocoin / Ejecutar Jigocoin

Start node:

```bash
bitcoind -daemon
```

Stop node:

```bash
bitcoin-cli stop
```

---

# Data Directory / Directorio de Datos

Default location:

Linux:

```bash
~/.jigocoin/
```

Configuration file:

```bash
~/.jigocoin/jigocoin.conf
```

---

# Example Configuration / Ejemplo de Configuración

```ini
server=1
daemon=1

rpcuser=jigocoin
rpcpassword=strongpassword

port=19335
rpcport=19332

txindex=1
fallbackfee=0.0001
```

---

# Build Troubleshooting / Resolución de Problemas

**EN**

If compilation fails:

Check missing dependencies:

```bash
sudo apt update
sudo apt upgrade
```

Then rebuild:

```bash
make clean
./configure
make -j$(nproc)
```

**ES**

Si la compilación falla:

Verifica dependencias:

```bash
sudo apt update
sudo apt upgrade
```

Después recompila:

```bash
make clean
./configure
make -j$(nproc)
```

---

# Notes / Notas

**EN**

Always build from trusted source code.

Verify repository integrity before compiling.

**ES**

Compila siempre desde código fuente confiable.

Verifica la integridad del repositorio antes de compilar.

---

# Summary / Resumen

Build Steps:

1. Install dependencies
2. Clone repository
3. Run autogen
4. Configure
5. Compile
6. Verify binary

This process creates a working Jigocoin node ready to run.

Este proceso crea un nodo Jigocoin funcional listo para ejecutarse.
