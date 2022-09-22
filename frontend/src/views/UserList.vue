<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { FilterMatchMode, FilterOperator } from 'primevue/api'
import { useToast } from 'primevue/usetoast'

import PrimeDataTable from '@/components/PrimeDataTable.vue'
import type { User } from '@/types/User'
import { roles } from '@/constants'
import UserService from '@/services/UserService'
import useDataTable from '@/composables/useDataTable'
import DeleteDialog from '@/components/DeleteDialog.vue'

const toast = useToast()
const { newEditDialog, deleteDialog, refreshTime, refresh,
    openNewEditDialog, hideNewEditDialog, hideDeleteDialog } = useDataTable()
const filters = ref({
    'id': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    'first_name': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'last_name': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'email': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'employee_id': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'role_id': { value: null, matchMode: FilterMatchMode.IN }
})
const user = ref<User>({
    email: '',
    role_id: ''
})

onMounted(() => {
    refresh()
})

function reset() {
    user.value = {
        id: undefined,
        email: '',
        first_name: '',
        last_name: '',
        employee_id: '',
        role_id: '',
        password: ''
    }
}

function editRecord(recordToEdit: User) {
    user.value = { ...recordToEdit }
    newEditDialog.value = true
}

async function saveRecord() {
    try {
        if (user.value.id) {    // Record must be edited
            await UserService.update(user.value.id, user.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: `User ${user.value.id} updated`, life: 3000 })
        }
        else {                  // Record must be created
            await UserService.create(user.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: 'User created', life: 3000 })
        }
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error saving the record', life: 3000 })
    }
    newEditDialog.value = false
    reset()
    refresh()
}

function confirmDeleteRecord(recordToDelete: User) {
    user.value = recordToDelete
    deleteDialog.value = true
}

async function deleteSelectedRecords() {
    try {
        if (user.value.id !== undefined) {
            await UserService.delete(user.value.id)
            toast.add({ severity: 'success', summary: 'Successful', detail: `User ${user.value.id} deleted`, life: 3000 })
        }
        deleteDialog.value = false
        reset()
        refresh()
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error deleting the record', life: 3000 })
    }
}
</script>

<template>
    <div class="card">
        <PrimeDataTable :ApiService="UserService" :initialFilters="filters" title="Manage Users" :refresh="refreshTime"
            @click-new="openNewEditDialog(reset)">
            <Column field="id" header="ID" dataType="numeric" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputNumber v-model="filterModel.value" class="p-column-filter" placeholder="Search by ID" />
                </template>
            </Column>
            <Column field="first_name" header="First Name" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by First Name" />
                </template>
            </Column>
            <Column field="last_name" header="Last Name" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Last Name" />
                </template>
            </Column>
            <Column field="email" header="Email" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Email" />
                </template>
            </Column>
            <Column field="employee_id" header="Employee ID" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Employee ID" />
                </template>
            </Column>
            <Column field="role_id" header="Role" :sortable="true" :showFilterMatchModes="false"
                :filterMenuStyle="{ 'width': '15rem' }">
                <template #filter="{ filterModel }">
                    <div class="mb-3">Select Role</div>
                    <MultiSelect v-model="filterModel.value" :options="roles" optionLabel="description" optionValue="id"
                        placeholder="Any" class="p-column-filter"></MultiSelect>
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

        <Dialog v-model:visible="newEditDialog" :style="{ width: '450px' }" header="User Details" :modal="true"
            class="p-fluid">
            <div class="field">
                <label for="firstName">First Name</label>
                <InputText id="firstName" v-model.trim="user.first_name" autofocus />
            </div>
            <div class="field">
                <label for="lastName">Last Name</label>
                <InputText id="lastName" v-model.trim="user.last_name" />
            </div>
            <div class="field">
                <label for="email">Email</label>
                <InputText id="email" v-model.trim="user.email" />
            </div>
            <div class="field">
                <label for="password">Initial Password</label>
                <InputText id="password" v-model.trim="user.password" />
            </div>
            <div class="field">
                <label for="employeeID">Employee ID</label>
                <InputText id="employeeID" v-model.trim="user.employee_id" />
            </div>
            <div class="field">
                <label for="roleID">Role</label>
                <Dropdown id="roleID" v-model="user.role_id" :options="roles" optionLabel="description" optionValue="id"
                    placeholder="Select a Role" />
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