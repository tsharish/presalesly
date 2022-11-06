import { ref } from 'vue'
import UserService from '@/services/UserService'
import type { UserSummary } from '@/types/User'

export default () => {
    const users = ref<UserSummary[]>([])
    const loadingUsers = ref(false)

    async function loadUsers(event: any) {
        loadingUsers.value = true
        try {
            let filterParams: string | undefined = ''

            if (event !== undefined && event.query !== undefined) {
                // Function being invoked from AutoComplete
                filterParams = JSON.stringify([{ field: 'full_name', operator: 'contains', value: event.query.toLowerCase() }])
            } else if (event !== undefined && event.value !== undefined) {
                // Function being invoked from Dropdown with a filter
                filterParams = JSON.stringify([{ field: 'full_name', operator: 'contains', value: event.value.toLowerCase() }])
            } else {
                // Function being invoked from Dropdown when the overlay is shown
                filterParams = undefined
            }

            const response = await UserService.getAll({ filter: filterParams })
            users.value = response.data.items
        } catch (error: any) {
            if (error.response.status === 404) {    // No records found
                users.value = []
            }
            console.log(error)
        }
        loadingUsers.value = false
    }
    return { users, loadingUsers, loadUsers }
}