# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import filters as f

from iota_async import Address, BadApiResponse, ProposedTransaction, TransactionHash
from iota_async.commands import FilterCommand, RequestFilter
from iota_async.commands.core.check_consistency import CheckConsistencyCommand
from iota_async.commands.extended.send_transfer import SendTransferCommand
from iota_async.filters import Trytes

__all__ = [
    'PromoteTransactionCommand',
]


class PromoteTransactionCommand(FilterCommand):
    """
    Executes ``promoteTransaction`` extended API command.

    See :py:meth:`iota_async.api.Iota.promote_transaction` for more
    information.
    """
    command = 'promoteTransaction'

    def get_request_filter(self):
        return PromoteTransactionRequestFilter()

    def get_response_filter(self):
        pass

    async def _execute(self, request):
        depth = request['depth']  # type: int
        min_weight_magnitude = request['minWeightMagnitude']  # type: int
        transaction = request['transaction']  # type: TransactionHash

        cc_response = await CheckConsistencyCommand(self.adapter)(tails=[transaction])
        if cc_response['state'] is False:
            raise BadApiResponse(
                'Transaction {transaction} is not promotable. '
                'You should reattach first.'.format(transaction=transaction)
            )

        spam_transfer = ProposedTransaction(
            address=Address(b''),
            value=0,
        )

        return await SendTransferCommand(self.adapter)(
            seed=spam_transfer.address,
            depth=depth,
            transfers=[spam_transfer],
            minWeightMagnitude=min_weight_magnitude,
            reference=transaction,
        )


class PromoteTransactionRequestFilter(RequestFilter):
    def __init__(self):
        super(PromoteTransactionRequestFilter, self).__init__({
            'depth': f.Required | f.Type(int) | f.Min(1),
            'transaction': f.Required | Trytes(TransactionHash),

            # Loosely-validated; testnet nodes require a different value
            # than mainnet.
            'minWeightMagnitude': f.Required | f.Type(int) | f.Min(1),
        })
