import ecdsa
import hashlib
import base58


class Key:
    def __init__(self, public_key: str, secret_key: str=None):
        """

        :param public_key: base58 encoded
        :param secret_key: base58 encoded
        """
        self.pk = base58.b58decode(public_key)[1:]
        if secret_key:
            self.sk = base58.b58decode(secret_key)

    def sign(self, data: bytes):
        if not self.sk:
            raise Exception('Secret key is not import yet.')
        key = ecdsa.SigningKey.from_string(self.sk, curve=ecdsa.NIST256p)
        return key.sign(data, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der)

    def verify(self, signature: str, data: str):
        key = ecdsa.VerifyingKey.from_string(self.pk, curve=ecdsa.NIST256p)
        return key.verify(base58.b58decode(signature),
                          data.encode('utf8'),
                          hashfunc=hashlib.sha256,
                          sigdecode=ecdsa.util.sigdecode_der)
