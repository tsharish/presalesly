import router from '@/router'
import axios from 'axios'
import BaseApiService from './BaseApiService'

export default class ApiService extends BaseApiService {
    api = axios.create()

    constructor(resource: string) {
        super(resource)

        this.api.interceptors.request.use(function (config) {
            let user = null
            let userInStorage = localStorage.getItem('user')
            if (userInStorage) {
                user = JSON.parse(userInStorage)
            }
            if (user && user.access_token) {
                config.headers = {
                    Authorization: `Bearer ${user.access_token}`
                }
            }
            return config
        }, function (error) {
            return Promise.reject(error)
        })

        this.api.interceptors.response.use(function (response) {
            return response
        }, function (error) {
            if (error.response) {
                if (error.response.status === 401) {
                    router.push({ name: 'login' })
                }
            }
            return Promise.reject(error)
        })
    }
}