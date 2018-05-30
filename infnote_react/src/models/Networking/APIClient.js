import axios from 'axios'


class APIClient {
    constructor() {
        this.client = axios.create({
            baseURL: 'http://localhost:8000/',
        })
        this.client.defaults.headers.common['Content-Type'] = 'application/json'
    }

    authorize(email, password) {
        return this.client.post('/api-token-auth/', {
            email: email,
            password: password,
        }).then(response => {
            this.client.defaults.headers.common['Authorization'] = 'JWT ' + response.data.token
            return this.client.get('/user/')
        })
    }
}

export default new APIClient()
