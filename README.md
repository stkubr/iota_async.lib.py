=====
PyOTA (Asynchronous)
=====
This is an **asynchronous fork** of the official Python library [https://github.com/iotaledger/iota.lib.py] for the IOTA Core.
Uses standard Python 3.6 library `asyncio` module and `requests-async` wrapper.

Some tests are failing, because mock classes and tests are still in **sync** mode.

Expect dragons, tell me if seen: Discord **stkubr#1936**

=====
Usage
=====

```python
from iota_async import Address, ProposedTransaction, TryteString, Tag, Iota
import asyncio

async def send_transaction():
    while True:
        api = Iota('https://nodes.thetangle.org:443', 'TESTSEED')
        addr = Address('EQSAUZXULTTYZCLNJNTXQTQHOMOFZERHTCGTXOLTVAHKSA9OGAZDEKECURBRIXIJWNPFCQIOVFVVXJVD9')
        res = await api.send_transfer(
                    depth=3,
                    transfers=[ProposedTransaction(address=addr, value=0,
                                                   tag=Tag('TESTTAG'), message=TryteString.from_string('test message'))]
                )
        print(res['bundle'][0].as_json_compatible())
        await asyncio.sleep(0.1)

async def get_hashes():
    while True:
        api = Iota('https://nodes.thetangle.org:443', 'TESTSEED')
        addr = Address('EQSAUZXULTTYZCLNJNTXQTQHOMOFZERHTCGTXOLTVAHKSA9OGAZDEKECURBRIXIJWNPFCQIOVFVVXJVD9')
        res = await api.find_transactions(addresses=[addr])
        print(len(res['hashes']))
        await asyncio.sleep(0.1)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(send_transaction(), get_hashes()))
loop.close()
```
