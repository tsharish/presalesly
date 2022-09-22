<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { FilterMatchMode, FilterOperator } from 'primevue/api'
import { useToast } from 'primevue/usetoast'

import PrimeDataTable from '@/components/PrimeDataTable.vue'
import type { OppTemplate } from '@/types/OppTemplate'
import OppTemplateService from '@/services/OppTemplateService'
import useDataTable from '@/composables/useDataTable'
import DeleteDialog from '@/components/DeleteDialog.vue'

const router = useRouter()
const toast = useToast()
const { newEditDialog, deleteDialog, refreshTime, refresh,
    openNewEditDialog, hideNewEditDialog, hideDeleteDialog } = useDataTable()
const filters = ref({
    'id': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    'description': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
})
const oppTemplate = ref<OppTemplate>({
    description: '',
    opp_template_tasks: []
})

onMounted(() => {
    refresh()
})

function reset() {
    oppTemplate.value = {
        id: undefined,
        description: '',
        opp_template_tasks: []
    }
}

async function saveRecord() {
    try {
        const response = await OppTemplateService.create(oppTemplate.value)
        toast.add({ severity: 'success', summary: 'Successful', detail: 'Opportunity Template created', life: 3000 })
        router.push({ name: 'oppTemplate', params: { id: response.data.id } })
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error saving the record', life: 3000 })
    }
}

function confirmDeleteRecord(recordToDelete: OppTemplate) {
    oppTemplate.value = recordToDelete
    deleteDialog.value = true
}

async function deleteSelectedRecords() {
    try {
        if (oppTemplate.value.id !== undefined) {  //Only one record must be deleted
            await OppTemplateService.delete(oppTemplate.value.id)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Opportunity Stage ${oppTemplate.value.id} deleted`, life: 3000 })
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
        <PrimeDataTable :ApiService="OppTemplateService" :initialFilters="filters" title="Manage Opportunity Templates"
            :refresh="refreshTime" @click-new="openNewEditDialog(reset)">
            <Column field="id" header="ID" dataType="numeric" :sortable="true">
                <template #filter="{filterModel}">
                    <InputNumber v-model="filterModel.value" class="p-column-filter" placeholder="Search by ID" />
                </template>
            </Column>
            <Column field="description" header="Description" :sortable="true">
                <template #filter="{filterModel}">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Description" />
                </template>
            </Column>
            <Column :exportable="false" style="min-width:8rem">
                <template #body="slotProps">
                    <Button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-warning mr-2"
                        @click="router.push({ name: 'oppTemplate', params: { id: slotProps.data.id } })" />
                    <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger"
                        @click="confirmDeleteRecord(slotProps.data)" />
                </template>
            </Column>
        </PrimeDataTable>

        <Dialog v-model:visible="newEditDialog" :style="{width: '450px'}" header="New Opportunity Template"
            :modal="true" class="p-fluid">
            <div class="field">
                <label for="description">Description</label>
                <InputText id="description" v-model.trim="oppTemplate.description" />
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