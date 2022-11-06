import { ref } from 'vue'
import AccountService from '@/services/AccountService'
import type { AccountSummary } from '@/types/Account'

export default () => {
    const accounts = ref<AccountSummary[]>([])
    const loadingAccounts = ref(false)

    async function loadAccounts(event: any) {
        loadingAccounts.value = true
        try {
            const filterParams = JSON.stringify([{ field: 'name', operator: 'contains', value: event.query.toLowerCase() }])
            const response = await AccountService.getAll({ filter: filterParams })
            accounts.value = response.data.items
        } catch (error: any) {
            if (error.response.status === 404) {    // No records found
                accounts.value = []
            }
            console.log(error)
        }
        loadingAccounts.value = false
    }

    return { accounts, loadingAccounts, loadAccounts }
}