# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from typing import Optional

import filters as f

from iota_async.commands import FilterCommand, RequestFilter
from iota_async.crypto.types import Seed
from iota_async.filters import SecurityLevel, Trytes
from iota_async.multisig.commands.get_private_keys import GetPrivateKeysCommand

__all__ = [
    'GetDigestsCommand',
]


class GetDigestsCommand(FilterCommand):
    """
    Implements `getDigests` multisig API command.

    References:

    - :py:meth:`iota_async.multisig.api.MultisigIota.get_digests`
    """
    command = 'getDigests'

    def get_request_filter(self):
        return GetDigestsRequestFilter()

    def get_response_filter(self):
        pass

    def _execute(self, request):
        count = request['count']  # type: Optional[int]
        index = request['index']  # type: int
        seed = request['seed']  # type: Seed
        security_level = request['securityLevel']  # type: int

        gpk_result = GetPrivateKeysCommand(self.adapter)(
            seed=seed,
            count=count,
            index=index,
            securityLevel=security_level,
        )

        return {
            'digests': [key.get_digest() for key in gpk_result['keys']],
        }


class GetDigestsRequestFilter(RequestFilter):
    def __init__(self):
        super(GetDigestsRequestFilter, self).__init__(
            {
                # Optional Parameters
                'count': f.Type(int) | f.Min(1) | f.Optional(default=1),
                'index': f.Type(int) | f.Min(0) | f.Optional(default=0),
                'securityLevel': SecurityLevel,

                # Required Parameters
                'seed': f.Required | Trytes(Seed),
            },

            allow_missing_keys={
                'count',
                'index',
                'securityLevel',
            },
        )
