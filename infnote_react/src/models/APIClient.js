import axios from 'axios'
import Cookies from 'universal-cookie'

import { API_HOST } from 'config'


class APIClient {
    constructor() {
        this.client = axios.create({
            baseURL: API_HOST,
        })
        this.client.defaults.headers.common['Content-Type'] = 'application/json'
        this.cookies = new Cookies()

        const token = this.loadToken()
        if (token) {
            this.client.defaults.headers.common['Authorization'] = token
        }
    }

    clearToken() {
        this.cookies.remove('token')
    }

    loadToken() {
        return this.cookies.get('token')
    }

    authorize(email, password) {
        return this.client.post('/api-token-auth/', {
            email: email,
            password: password,
        }).then(response => {
            const token = 'JWT ' + response.data.token
            this.cookies.set('token', token, { path: '/', maxAge: 60 * 60 * 24 * 30 })
            this.client.defaults.headers.common['Authorization'] = token
            return this.client.get('/user/')
        })
    }

    user() {
        if (this.loadToken()) {
            return this.client.get('/user/')
        }
        return null
    }

    posts(category = '/', page = 1) {
        let url = '/post/list/?category=' + category + '&page=' + page
        return this.client.get(url)
    }

    retreivePost(id) {
        return this.client.get('/post/' + id)
    }

    retreiveReplies(id, page = 1) {
        return this.client.get('/post/' + id + '/replies/?page=' + page)
    }

    sendPost(post) {
        return this.client.post('/post/', post)
    }

    categories() {
        return this.client.get('/category/list/')
    }

}

export default new APIClient()
