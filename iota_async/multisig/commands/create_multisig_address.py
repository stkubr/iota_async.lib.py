# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from typing import List

import filters as f

from iota_async.commands import FilterCommand, RequestFilter
from iota_async.crypto.types import Digest
from iota_async.filters import Trytes
from iota_async.multisig.crypto.addresses import MultisigAddressBuilder

__all__ = [
    'CreateMultisigAddressCommand',
]


class CreateMultisigAddressCommand(FilterCommand):
    """
    Implements `create_multisig_address` multisig command.

    References:

    - :py:meth:`iota_async.multisig.api.MultisigIota.create_multisig_address`
    """
    command = 'createMultisigAddress'

    def get_request_filter(self):
        return CreateMultisigAddressRequestFilter()

    def get_response_filter(self):
        pass

    def _execute(self, request):
        digests = request['digests']  # type: List[Digest]

        builder = MultisigAddressBuilder()

        for d in digests:
            builder.add_digest(d)

        return {
            'address': builder.get_address(),
        }


class CreateMultisigAddressRequestFilter(RequestFilter):
    def __init__(self):
        super(CreateMultisigAddressRequestFilter, self).__init__({
            'digests':
                f.Required | f.Array | f.FilterRepeater(
                    f.Required | Trytes(Digest),
                ),
        })
