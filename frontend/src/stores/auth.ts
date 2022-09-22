import { defineStore } from 'pinia'
import AuthService from '@/services/AuthService'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        authenticated: false,
        loginLanguageCode: '', 
    }),
    getters: {},
    actions: {
        async login(username: string, password: string) {
            let formData = new FormData()
            formData.append('username', username)
            formData.append('password', password)

            try {
                const response = await AuthService.login(formData)
                if (response.data.access_token) {
                    localStorage.setItem('user', JSON.stringify(response.data))
                    this.authenticated = true
                }
            } catch (error: any) {
                this.authenticated = false
            }
        },
        logout() {
            localStorage.removeItem('user')
            this.authenticated = false
        }
    }
})