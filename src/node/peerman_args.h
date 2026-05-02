// Copyright (c) 2023-present The Jigocoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or https://opensource.org/license/mit.

#ifndef JIGOCOIN_NODE_PEERMAN_ARGS_H
#define JIGOCOIN_NODE_PEERMAN_ARGS_H

#include <net_processing.h>

class ArgsManager;

namespace node {
void ApplyArgsManOptions(const ArgsManager& argsman, PeerManager::Options& options);
} // namespace node

#endif // JIGOCOIN_NODE_PEERMAN_ARGS_H
