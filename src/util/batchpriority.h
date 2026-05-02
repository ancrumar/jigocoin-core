// Copyright (c) 2023-present The Jigocoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef JIGOCOIN_UTIL_BATCHPRIORITY_H
#define JIGOCOIN_UTIL_BATCHPRIORITY_H

/**
 * On platforms that support it, tell the kernel the calling thread is
 * CPU-intensive and non-interactive. See SCHED_BATCH in sched(7) for details.
 *
 */
void ScheduleBatchPriority();

#endif // JIGOCOIN_UTIL_BATCHPRIORITY_H
