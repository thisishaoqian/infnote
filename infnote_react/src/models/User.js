import { Store, APIClient } from '.'
import { changeUser } from './actions'
import { Blockchain } from 'tools'

var __currentUser
var __placeholder

class User {
    static getMembers() {
        return ['user_id', 'public_address', 'date_created', 'date_last_login', 'private_key', 'is_activated', 'is_confirmed', 'topics', 'replies', 'likes'].concat(this.getSaveableKeys())
    }

    static getSaveableKeys() {
        return ['date_birthday', 'email', 'username', 'nickname', 'avatar', 'gender', 'location', 'bio', 'website', 'qq', 'wechat', 'weibo', 'facebook', 'twitter']
    }

    static current() {
        return __currentUser ? __currentUser : this.placeholder()
    }

    static login(email, password) {
        return APIClient
            .authorize(email, password)
            .then(response => {
                const user = new User(response.data)
                __currentUser = user
                return user
            })
    }

    static logout() {
        APIClient.clearToken()
        __currentUser = null
        Store.dispatch(changeUser(this.current()))
    }

    static recover() {
        if (__currentUser) return true

        const promise = APIClient.user()
        if (promise) {
            promise.then(response => {
                const user = new User(response.data)
                __currentUser = user
                Store.dispatch(changeUser(user))
                return user
            }).catch(error => {
                console.log(error)
                APIClient.clearToken()
            })
            return true
        }

        return false
    }

    constructor(props) {
        User.getMembers().forEach(name => this[name] = props[name])

        Object.defineProperties(this, {
            user_id: { writable: false },
            date_created: { writable: false },
            date_last_login: { writable: false },
            is_activated: { writable: false },
            is_confirmed: { writable: false },
        })

        if (this.private_key) {
            this.blockchain = new Blockchain(this.private_key)
        } else {
            this.blockchain = new Blockchain()
        }

        Object.seal(this)
    }

    static placeholder() {
        if (!__placeholder) {
            __placeholder = new User({ nickname: 'Login' })
        }
        return __placeholder
    }

    getGender() {
        if (this.gender < 0 || this.gender > 2) return 'Unknown'
        return ['Unknown', 'Male', 'Female'][this.gender]
    }

    submit() {
        let data = {}
        User.getSaveableKeys().forEach(item => data[item] = this[item])
        return APIClient.coins(1e5 * 3).then(response => {
            return APIClient
                .sendUserinfo({
                    data: User.current().blockchain.generateTransaction(data, response.data.coins, response.data.fee, true)
                })
                .then(response => new User(response.data))
        })
    }
}


export default User