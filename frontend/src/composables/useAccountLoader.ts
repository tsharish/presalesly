import { ref } from 'vue'
import AccountService from '@/services/AccountService'
import type { Account } from '@/types/Account'
import { useAuthStore } from '@/stores/auth'

export default () => {
    const accounts = ref<Account[]>([])
    const loadingAccounts = ref(false)

    async function loadAccounts() {
        const auth = useAuthStore()

        loadingAccounts.value = true
        try {
            const response = await AccountService.getAll({ lang_code: auth.loginLanguageCode })
            accounts.value = response.data.items
        } catch (error: any) {
            if (error.response.status === 404) {    // No records found
                accounts.value = []
            }
            console.log(error)      //TODO: Implement proper error handling
        }
        loadingAccounts.value = false
    }

    return { accounts, loadingAccounts, loadAccounts }
}