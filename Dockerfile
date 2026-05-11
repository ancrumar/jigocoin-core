FROM ubuntu:24.04

RUN apt update && apt install -y \
    libevent-dev \
    libboost-system-dev \
    libboost-filesystem-dev \
    libboost-test-dev \
    libboost-thread-dev \
    libsqlite3-dev \
    libminiupnpc-dev \
    libzmq3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY build/bin/jigocoind /usr/local/bin/
COPY build/bin/jigocoin-cli /usr/local/bin/

EXPOSE 21335

CMD ["jigocoind", "-datadir=/data", "-printtoconsole"]

