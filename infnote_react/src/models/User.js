import { APIClient } from './Networking'

var __currentUser

class User {
    static getMembers() {
        return ['user_id','date_created','date_last_login','date_birthday','public_key','private_key','email','username','is_activated','is_confirmed','nickname','avatar','gender','location','bio','website','qq','wechat','weibo','facebook','twitter']
    }

    static current() {
        return __currentUser
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

    constructor(props) {
        User.getMembers().forEach(name => { this[name] = props[name] })

        Object.defineProperties(this, {
            user_id: { writable: false },
            date_created: { writable: false },
            date_last_login: { writable: false },
            is_activated: { writable: false },
            is_confirmed: { writable: false },
        })

        Object.seal(this)
    }
}


export default User