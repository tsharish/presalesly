<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { FilterMatchMode, FilterOperator } from 'primevue/api'
import { useToast } from 'primevue/usetoast'

import PrimeDataTable from '@/components/PrimeDataTable.vue'
import { useAuthStore } from '@/stores/auth'
import type { Industry } from '@/types/Industry'
import { getDescriptionIndex } from '@/composables/useUtils'
import IndustryService from '@/services/IndustryService'
import useDataTable from '@/composables/useDataTable'
import DeleteDialog from '@/components/DeleteDialog.vue'

const auth = useAuthStore()
const toast = useToast()
const { newEditDialog, deleteDialog, refreshTime, refresh,
    openNewEditDialog, hideNewEditDialog, hideDeleteDialog } = useDataTable()
const filters = ref({
    'external_id': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'description': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] }
})
const industry = ref<Industry>({
    descriptions: []
})

onMounted(() => {
    refresh()
})

function reset() {
    industry.value = {
        id: undefined,
        external_id: '',
        descriptions: [],
        description: ''
    }
}

function editRecord(recordToEdit: Industry) {
    industry.value = { ...recordToEdit }
    newEditDialog.value = true
}

async function saveRecord() {
    try {
        if (industry.value.id) {    // Record must be edited
            const index = getDescriptionIndex(industry.value.descriptions, auth.loginLanguageCode)
            if (index !== -1) {     // The description in the language already exists and must be edited
                industry.value.descriptions[index].description = industry.value.description
            } else {                // The description in the language does not exist and must be added
                industry.value.descriptions?.push({
                    language_code: auth.loginLanguageCode,
                    description: industry.value.description
                })
            }
            await IndustryService.update(industry.value.id, industry.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Industry ${industry.value.id} updated`, life: 3000 })
        }
        else {                      // Record must be created
            industry.value.descriptions?.push({
                language_code: auth.loginLanguageCode,
                description: industry.value.description
            })
            await IndustryService.create(industry.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Industry created', life: 3000 })
        }
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error saving the record', life: 3000 })
    }
    newEditDialog.value = false
    reset()
    refresh()
}

function confirmDeleteRecord(recordToDelete: Industry) {
    industry.value = recordToDelete
    deleteDialog.value = true
}

async function deleteSelectedRecords() {
    try {
        if (industry.value.id !== undefined) {  //Only one record must be deleted
            await IndustryService.delete(industry.value.id)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Industry ${industry.value.id} deleted`, life: 3000 })
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
        <PrimeDataTable :ApiService="IndustryService" :initialFilters="filters" title="Manage Industries"
            :refresh="refreshTime" @click-new="openNewEditDialog(reset)">
            <Column field="external_id" header="External ID" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by External ID" />
                </template>
            </Column>
            <Column field="description" header="Description" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Description" />
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

        <Dialog v-model:visible="newEditDialog" :style="{ width: '450px' }" header="Industry Details" :modal="true"
            class="p-fluid">
            <div class="field">
                <label for="externalID">External ID</label>
                <InputText id="externalID" v-model.trim="industry.external_id" autofocus />
            </div>
            <div class="field">
                <label for="description">Description</label>
                <InputText id="description" v-model.trim="industry.description" />
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