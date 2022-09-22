import axios from 'axios'
import BaseApiService from './BaseApiService'

class AuthService extends BaseApiService {
    constructor() {
        super('auth/login')
    }

    login(data: any) {
        return axios.post(this.getUrl(), data)
    }
}

export default new AuthService()