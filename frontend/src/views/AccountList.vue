<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { FilterMatchMode, FilterOperator } from 'primevue/api'
import { useToast } from 'primevue/usetoast'

import PrimeDataTable from '@/components/PrimeDataTable.vue'
import AccountService from '@/services/AccountService'
import useDataTable from '@/composables/useDataTable'
import { formatCurrency } from '@/composables/useUtils'
import { useAuthStore } from '@/stores/auth'
import type { Account } from '@/types/Account'
import type { Industry } from '@/types/Industry'
import IndustryService from '@/services/IndustryService'
import DeleteDialog from '@/components/DeleteDialog.vue'
import { countries, currencies } from '@/constants'

const auth = useAuthStore()
const toast = useToast()
const { newEditDialog, deleteDialog, refreshTime, refresh,
    openNewEditDialog, hideNewEditDialog, hideDeleteDialog } = useDataTable()
const filters = ref({
    'id': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    'name': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'country_code': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'annual_revenue': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    'number_of_employees': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    'industry.id': { value: null, matchMode: FilterMatchMode.IN }
})
const account = ref<Account>({
    name: '',
    country_code: ''
})
const industries = ref<Industry[]>([])

onMounted(async () => {
    refresh()
    const response = await IndustryService.getAll({ lang_code: auth.loginLanguageCode })
    industries.value = response.data.items
})

function reset() {
    account.value = {
        id: undefined,
        external_id: '',
        source_url: undefined,
        name: '',
        annual_revenue: undefined,
        annual_revenue_curr_code: '',
        number_of_employees: undefined,
        country_code: '',
        street: '',
        address_line_2: '',
        address_line_3: '',
        city: '',
        state: '',
        postal_code: '',
        fax: '',
        email: '',
        phone: '',
        website: undefined,
        industry: undefined,
        industry_id: undefined
    }
}

function editRecord(recordToEdit: Account) {
    account.value = { ...recordToEdit }
    account.value.industry_id = recordToEdit.industry?.id
    newEditDialog.value = true
}

async function saveRecord() {
    //Setting to undefined since empty strings will fail backend validation
    account.value.annual_revenue_curr_code = account.value.annual_revenue_curr_code === '' ? undefined : account.value.annual_revenue_curr_code
    account.value.source_url = account.value.source_url === '' ? undefined : account.value.source_url
    account.value.email = account.value.email === '' ? undefined : account.value.email
    try {
        if (account.value.id) {    // Record must be edited
            await AccountService.update(account.value.id, account.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Account ${account.value.id} updated`, life: 3000 })
        }
        else {                      // Record must be created
            await AccountService.create(account.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Account created', life: 3000 })
        }
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error saving the record', life: 3000 })
    }
    newEditDialog.value = false
    reset()
    refresh()
}

function confirmDeleteRecord(recordToDelete: Account) {
    account.value = recordToDelete
    deleteDialog.value = true
}

async function deleteSelectedRecords() {
    try {
        if (account.value.id !== undefined) {
            await AccountService.delete(account.value.id)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Account ${account.value.id} deleted`, life: 3000 })
        }
        deleteDialog.value = false
        reset()
        refresh()
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error deleting account', life: 3000 })
    }
}
</script>

<template>
    <div class="card">
        <PrimeDataTable :ApiService="AccountService" :initialFilters="filters" title="Manage Accounts"
            :refresh="refreshTime" @click-new="openNewEditDialog(reset)">
            <Column field="id" header="ID" dataType="numeric" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputNumber v-model="filterModel.value" class="p-column-filter" placeholder="Search by ID" />
                </template>
            </Column>
            <Column field="name" header="Account Name" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Account Name" />
                </template>
            </Column>
            <Column field="country_code" header="Country" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Country" />
                </template>
            </Column>
            <Column field="annual_revenue" header="Annual Revenue" dataType="numeric" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputNumber v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Annual Revenue" />
                </template>
                <template #body="slotProps">
                    {{ formatCurrency(slotProps.data.annual_revenue, slotProps.data.annual_revenue_curr_code) }}
                </template>
            </Column>
            <Column field="number_of_employees" header="# of Employees" dataType="numeric" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputNumber v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by # of Employees" />
                </template>
            </Column>
            <Column field="industry.description" filterField="industry.id" header="Industry" :sortable="true"
                :showFilterMatchModes="false" :filterMenuStyle="{ 'width': '15rem' }">
                <template #filter="{ filterModel }">
                    <div class="mb-3">Select Industry</div>
                    <MultiSelect v-model="filterModel.value" :options="industries" optionLabel="description"
                        optionValue="id" placeholder="Any" class="p-column-filter"></MultiSelect>
                </template>
            </Column>
            <Column :exportable="false" style="min-width:8rem">
                <template #body="slotProps">
                    <Button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-warning mr-2"
                        @click="editRecord(slotProps.data)" />
                    <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger"
                        @click="confirmDeleteRecord(slotProps.data)" />
                </template>
            </Column>
        </PrimeDataTable>

        <Dialog v-model:visible="newEditDialog" :style="{ width: '450px' }" header="Account Details" :modal="true"
            class="p-fluid">
            <div class="field">
                <label for="externalID">External ID</label>
                <InputText id="externalID" v-model.trim="account.external_id" autofocus />
            </div>
            <div class="field">
                <label for="accountName">Account Name</label>
                <InputText id="accountName" v-model.trim="account.name" />
            </div>
            <div class="field">
                <label for="street">Street</label>
                <InputText id="street" v-model.trim="account.street" />
            </div>
            <div class="field">
                <label for="city">City</label>
                <InputText id="city" v-model.trim="account.city" />
            </div>
            <div class="field">
                <label for="state">State</label>
                <InputText id="state" v-model.trim="account.state" />
            </div>
            <div class="field">
                <label for="postalCode">Postal Code</label>
                <InputText id="postalCode" v-model.trim="account.postal_code" />
            </div>
            <div class="field">
                <label for="countryCode">Country</label>
                <Dropdown id="countryCode" v-model="account.country_code" :options="countries" optionLabel="name"
                    optionValue="code" placeholder="Select a Country" />
            </div>
            <div class="form-grid grid">
                <div class="field col-fixed" style="width:200px">
                    <label for="annualRevenue">Annual Revenue</label>
                    <InputNumber id="annualRevenue" v-model="account.annual_revenue" mode="decimal"
                        :minFractionDigits="2" :maxFractionDigits="2" />
                </div>
                <div class="field col-fixed" style="width:200px">
                    <label for="currencyCode">Currency</label>
                    <Dropdown id="currencyCode" v-model="account.annual_revenue_curr_code" :options="currencies"
                        optionLabel="name" optionValue="code" />
                </div>
            </div>
            <div class="field">
                <label for="numberOfEmployees">Number of Employees</label>
                <InputNumber id="numberOfEmployees" v-model="account.number_of_employees" />
            </div>
            <div class="field">
                <label for="email">Email</label>
                <InputText id="email" v-model.trim="account.email" />
            </div>
            <div class="field">
                <label for="phone">Phone Number</label>
                <InputText id="phone" v-model.trim="account.phone" />
            </div>
            <div class="field">
                <label for="website">Website</label>
                <InputText id="website" v-model.trim="account.website" />
            </div>
            <div class="field">
                <label for="industry">Industry</label>
                <Dropdown id="industry" v-model="account.industry_id" :options="industries" optionLabel="description"
                    optionValue="id" placeholder="Select an Industry" />
            </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="hideNewEditDialog(reset)" />
                <Button label="Save" icon="pi pi-check" class="p-button-text" @click="saveRecord" />
            </template>
        </Dialog>

        <DeleteDialog :deleteDialog="deleteDialog" @click-no="hideDeleteDialog(reset)"
            @click-yes="deleteSelectedRecords"></DeleteDialog>
    </div>
</template>