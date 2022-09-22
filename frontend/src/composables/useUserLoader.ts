import { ref } from 'vue'
import UserService from '@/services/UserService'
import type { User } from '@/types/User'

export default () => {
    const users = ref<User[]>([])
    const loadingUsers = ref(false)

    async function loadUsers() {
        loadingUsers.value = true
        try {
            const response = await UserService.getAll({})
            users.value = response.data.items
        } catch (error: any) {
            if (error.response.status === 404) {    // No records found
                users.value = []
            }
            console.log(error)      //TODO: Implement proper error handling
        }
        loadingUsers.value = false
    }

    return { users, loadingUsers, loadUsers }
}