/* global Buffer */

import { crypto, script, ECPair, TransactionBuilder } from 'bitcoinjs-lib'
import OPS from 'bitcoin-ops'
import bigi from 'bigi'

const SERVER_ADDRESS = '1A6csP8jrpyruyW4a9tX9Nonv4R8AviB1y'


class Blockchain {
    constructor(privateKey=null) {
        if (!privateKey)
            this.generateKeyPair()
        else {
            this.keyPair = ECPair.fromWIF(privateKey)
        }
    }
    
    get keyPair() {
        return this._keyPair
    }
    set keyPair(value) {
        this._keyPair = value
        if (value instanceof ECPair) {
            this.address = this.keyPair.getAddress()
            this.privateKey = this.keyPair.toWIF()
        }
    }

    generateKeyPair(userstr) {
        let hash = crypto.sha256(Buffer.from(userstr + this.randomString() + 'infnote.com'))
        let d = bigi.fromBuffer(hash)
        this.keyPair = new ECPair(d)
    }

    // money = txid
    generateTransaction(content, coins, fee, isInfo=false) {
        let opData = Buffer.from(JSON.stringify(content))
        let builder = new TransactionBuilder()
        var data = this.encode(opData, isInfo)
        builder.setVersion(2)

        let amount = 0
        coins.forEach(coin => {
            builder.addInput(coin.txid, coin.vout)
            amount += coin.value
        })

        builder.addOutput(data, 0)
        
        if (isInfo) {
            builder.addOutput(SERVER_ADDRESS, fee * 2)
            builder.addOutput(this.address, amount - fee * 3)
        } else {
            builder.addOutput(this.address, amount - fee)
        }

        builder.sign(0, this.keyPair)
        return builder.build().toHex()
    }

    encode(data, isInfo=false) {
        if (isInfo) {
            return script.compile([OPS.OP_NOP8, data])  // OP_INFO = OP_NOP8 = 183
        }
        return script.compile([OPS.OP_RETURN, data])
    }

    randomString() {
        let text = ''
        let possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        
        for (let i = 0; i < 20; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length))
        
        return text
    }
}

export default Blockchain