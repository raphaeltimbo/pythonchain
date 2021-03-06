from collections.abc import Sequence, Iterable

import Crypto
import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS


from pythonchain import base
from pythonchain import block
from pythonchain.runtime import registry




class Wallet(base.Base):
    public_key = base.ShortString()
    private_key = base.ShortString()

    def __init__(self, **kwargs):
        if not kwargs:
            kwargs.update(self.new_keys())
        super().__init__(**kwargs)

    def new_keys(self):
        private_key = ECC.generate(curve="P-256")
        public_key = private_key.public_key()

        response = {
            'private_key': private_key.export_key(format='DER').hex(),
            'public_key': public_key.export_key(format='DER').hex()
        }

        return response

    def balance(self, format=True):
        value = sum(output.amount for tr_id, index, output in block.BlockChain().unspent_outputs(filter=self.public_key))
        if format:
            return f"{value/block.TOKENMULTIPLIER:.02f}"
        return value
