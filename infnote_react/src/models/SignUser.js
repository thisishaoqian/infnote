import { APIClient } from '.'
import { Blockchain } from 'tools'

class SignUser {
    static getMembers() {
        return ['date_birthday', 'public_address', 'private_key', 'email', 'username', 'nickname', 'gender', 'location','bio','website','qq','wechat','weibo','facebook','twitter', 'password', 'code']
    }

    constructor(props) {
        SignUser.getMembers().forEach(name => this[name] = props[name])

        let blockchain = new Blockchain()
        this.public_address = blockchain.address
        this.private_key = blockchain.privateKey

        Object.seal(this)
    }

    signUp() {
        let data = {}
        SignUser.getMembers().forEach(name => data[name] = this[name])
        return APIClient.register(data)
    }
}

export default SignUser