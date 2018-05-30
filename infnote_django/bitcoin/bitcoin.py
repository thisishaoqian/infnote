import requests
import json
from codecs import decode


class BitcoinRPC:
    url = 'http://13.94.56.21:8962'
    auth = ('rpcuser', '111111')
    headers = {'Content-Type': 'application/json'}
    jsonrpc = {'jsonrpc': '2.0', 'id': 'flask'}

    def create_request(self, json_object):
        return requests.post(self.url, headers=self.headers, auth=self.auth, json={**self.jsonrpc, **json_object})

    def get_blockchain_height(self):
        r = self.create_request({'method': 'getblockchaininfo'})
        return r.json()['result']['blocks']

    def get_block_hash(self, height):
        r = self.create_request({'method': 'getblockhash', 'params': [int(height)]})
        return r.json()['result']

    def get_transactions_by_block_hash(self, hashcode):
        r = self.create_request({'method': 'getblock', 'params': [hashcode]})
        return r.json()['result']['tx']

    def get_transaction_by_hash(self, hashcode):
        r = self.create_request({'method': 'gettransaction', 'params': [hashcode]})
        return r.json()

    def get_raw_transaction_by_hash(self, hashcode):
        r = self.create_request({'method': 'getrawtransaction', 'params': [hashcode, True]})
        return r.json()

    def list_unspent(self):
        r = self.create_request({
            'method': 'listunspent',
            'params': {
                'addresses': ['1A6csP8jrpyruyW4a9tX9Nonv4R8AviB1y']}
        })
        return r.json()['result']

    def send_raw_transaction(self, hexstring: str):
        r = self.create_request({'method': 'sendrawtransaction', 'params': [hexstring]})
        return r.json()['result']

    def decode_raw_transaction(self, hexstring: str):
        r = self.create_request({'method': 'decoderawtransaction', 'params': [hexstring]})
        return r.json()['result']


class RawPost:
    def __init__(self, rpc_instance: BitcoinRPC, transaction_id: str, height: int):
        self.rpc = rpc_instance
        self.id = transaction_id
        self.author = self.__get_author()
        self.time = 0
        self.raw_content = self.__get_raw_content()
        self.content = self.__get_content()
        self.confirmations = 0
        self.json = self.__get_json()
        self.json['post_id'] = self.id
        self.json['user_id'] = self.author
        self.json['output_time'] = self.time
        self.json['confirmed'] = True
        self.json['height'] = height

    def __get_raw_content(self):
        t = self.rpc.get_raw_transaction_by_hash(self.id)
        self.time = t['result']['time']
        return t['result']['vout'][0]['scriptPubKey']['asm']

    def __get_author(self):
        t = self.rpc.get_transaction_by_hash(self.id)
        return t['result']['details'][1]['address']

    def __get_content(self):
        if 'OP_RETURN' not in self.raw_content:
            raise self.Error('Transaction does not contain real content.')
        hex_str = self.raw_content.lstrip('OP_RETURN ')
        return decode(hex_str, 'hex').decode('utf-8')

    def __get_json(self):
        return json.loads(self.content)

    class Error(Exception):
        pass


class RawPostFactory:

    def __init__(self, rpc_instance: BitcoinRPC):
        self.rpc = rpc_instance
        self.height = 1

    def get_posts(self, height=1) -> list:
        self.height = self.rpc.get_blockchain_height()
        if height < 1 or height > self.height:
            return []

        posts = []
        position = height
        while position <= self.height:
            position += 1

            try:
                hashcode = self.rpc.get_block_hash(position - 1)
                tids = self.rpc.get_transactions_by_block_hash(hashcode)
            except TypeError:
                continue

            if len(tids) < 2:
                continue

            for tid in tids:
                try:
                    p = RawPost(self.rpc, tid, position - 1)
                    p.confirmations = self.height - position + 1
                    posts.append(p)
                except (IndexError, TypeError, RawPost.Error, json.JSONDecodeError):
                    continue

        return posts
