// Copyright (c) 2011-present The Jigocoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef JIGOCOIN_QT_JIGOCOINADDRESSVALIDATOR_H
#define JIGOCOIN_QT_JIGOCOINADDRESSVALIDATOR_H

#include <QValidator>

/** Base58 entry widget validator, checks for valid characters and
 * removes some whitespace.
 */
class JigocoinAddressEntryValidator : public QValidator
{
    Q_OBJECT

public:
    explicit JigocoinAddressEntryValidator(QObject *parent);

    State validate(QString &input, int &pos) const override;
};

/** Jigocoin address widget validator, checks for a valid jigocoin address.
 */
class JigocoinAddressCheckValidator : public QValidator
{
    Q_OBJECT

public:
    explicit JigocoinAddressCheckValidator(QObject *parent);

    State validate(QString &input, int &pos) const override;
};

#endif // JIGOCOIN_QT_JIGOCOINADDRESSVALIDATOR_H
