// Copyright (c) 2022-present The Jigocoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef JIGOCOIN_POLICY_FEES_BLOCK_POLICY_ESTIMATOR_ARGS_H
#define JIGOCOIN_POLICY_FEES_BLOCK_POLICY_ESTIMATOR_ARGS_H

#include <util/fs.h>

class ArgsManager;

/** @return The fee estimates data file path. */
fs::path FeeestPath(const ArgsManager& argsman);

#endif // JIGOCOIN_POLICY_FEES_BLOCK_POLICY_ESTIMATOR_ARGS_H
