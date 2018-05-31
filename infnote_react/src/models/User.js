import { Store, APIClient } from '.'
import { changeUser } from './actions'

var __currentUser
var __placeholder

class User {
    static getMembers() {
        return ['user_id','date_created','date_last_login','date_birthday','public_key','private_key','email','username','is_activated','is_confirmed','nickname','avatar','gender','location','bio','website','qq','wechat','weibo','facebook','twitter']
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
                APIClient.removeToken()
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

        Object.seal(this)
    }

    static placeholder() {
        if (!__placeholder) {
            __placeholder = new User({ nickname: 'Login' })
        }
        return __placeholder
    }
}


export default User