<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { FilterMatchMode, FilterOperator } from 'primevue/api'
import { useToast } from 'primevue/usetoast'

import PrimeDataTable from '@/components/PrimeDataTable.vue'
import { useAuthStore } from '@/stores/auth'
import type { OppStage } from '@/types/OppStage'
import { getDescriptionIndex } from '@/composables/useUtils'
import OppStageService from '@/services/OppStageService'
import useDataTable from '@/composables/useDataTable'
import DeleteDialog from '@/components/DeleteDialog.vue'
import { oppStatuses } from '@/constants'

const auth = useAuthStore()
const toast = useToast()
const { newEditDialog, deleteDialog, refreshTime, refresh,
    openNewEditDialog, hideNewEditDialog, hideDeleteDialog } = useDataTable()
const filters = ref({
    'external_id': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'default_probability_percent': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    'sort_order': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    'opp_status': { value: null, matchMode: FilterMatchMode.IN },
    'description': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] }
})
const oppStage = ref<OppStage>({
    default_probability: 0,
    sort_order: 0,
    opp_status: '',
    descriptions: []
})

onMounted(() => {
    refresh()
})

function reset() {
    oppStage.value = {
        id: undefined,
        external_id: '',
        default_probability: 0,
        sort_order: 0,
        opp_status: '',
        descriptions: [],
        description: '',
        default_probability_percent: 0
    }
}

function editRecord(recordToEdit: OppStage) {
    oppStage.value = { ...recordToEdit }
    newEditDialog.value = true
}

async function saveRecord() {
    if (oppStage.value.default_probability_percent !== undefined) {
        oppStage.value.default_probability = oppStage.value.default_probability_percent / 100
    }
    try {
        if (oppStage.value.id) {    // Record must be edited
            const index = getDescriptionIndex(oppStage.value.descriptions, auth.loginLanguageCode)
            if (index !== -1) {     // The description in the language already exists and must be edited
                oppStage.value.descriptions[index].description = oppStage.value.description
            } else {                // The description in the language does not exist and must be added
                oppStage.value.descriptions?.push({
                    language_code: auth.loginLanguageCode,
                    description: oppStage.value.description
                })
            }
            await OppStageService.update(oppStage.value.id, oppStage.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Opportunity Stage ${oppStage.value.id} updated`, life: 3000 })
        }
        else {                      // Record must be created
            oppStage.value.descriptions?.push({
                language_code: auth.loginLanguageCode,
                description: oppStage.value.description
            })
            await OppStageService.create(oppStage.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Opportunity Stage created', life: 3000 })
        }
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error saving the record', life: 3000 })
    }
    newEditDialog.value = false
    reset()
    refresh()
}

function confirmDeleteRecord(recordToDelete: OppStage) {
    oppStage.value = recordToDelete
    deleteDialog.value = true
}

async function deleteSelectedRecords() {
    try {
        if (oppStage.value.id !== undefined) {  //Only one record must be deleted
            await OppStageService.delete(oppStage.value.id)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Opportunity Stage ${oppStage.value.id} deleted`, life: 3000 })
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
        <PrimeDataTable :ApiService="OppStageService" :initialFilters="filters" title="Manage Opportunity Stages"
            :refresh="refreshTime" @click-new="openNewEditDialog(reset)">
            <Column field="external_id" header="External ID" :sortable="true">
                <template #filter="{filterModel}">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by External ID" />
                </template>
            </Column>
            <Column field="description" header="Description" :sortable="true">
                <template #filter="{filterModel}">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Description" />
                </template>
            </Column>
            <Column field="default_probability_percent" header="Default Probability" dataType="numeric"
                :sortable="true">
                <template #filter="{filterModel}">
                    <InputNumber v-model="filterModel.value" class="p-column-filter" suffix="%" />
                </template>
                <template #body="slotProps">
                    {{ slotProps.data.default_probability_percent }}%
                </template>
            </Column>
            <Column field="sort_order" header="Sort Order" dataType="numeric" :sortable="true">
                <template #filter="{filterModel}">
                    <InputNumber v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Sort Order" />
                </template>
            </Column>
            <Column field="opp_status" header="Opportunity Status" :sortable="true" :showFilterMatchModes="false"
                :filterMenuStyle="{'width':'15rem'}">
                <template #filter="{filterModel}">
                    <div class="mb-3">Select Opportunity Status</div>
                    <MultiSelect v-model="filterModel.value" :options="oppStatuses" optionLabel="description"
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

        <Dialog v-model:visible="newEditDialog" :style="{width: '450px'}" header="Opportunity Stage Details"
            :modal="true" class="p-fluid">
            <div class="field">
                <label for="externalID">External ID</label>
                <InputText id="externalID" v-model.trim="oppStage.external_id" autofocus />
            </div>
            <div class="field">
                <label for="description">Description</label>
                <InputText id="description" v-model.trim="oppStage.description" />
            </div>
            <div class="field">
                <label for="defaultProbability">Default Probability</label>
                <InputNumber id="defaultProbability" v-model="oppStage.default_probability_percent" suffix="%" :min="0"
                    :max="100" />
            </div>
            <div class="field">
                <label for="sortOrder">Sort Order</label>
                <InputNumber id="sortOrder" v-model="oppStage.sort_order" integeronly />
            </div>
            <div class="field">
                <label for="oppStatus">Opportunity Status</label>
                <Dropdown id="oppStatus" v-model="oppStage.opp_status" :options="oppStatuses" optionLabel="description"
                    optionValue="id" placeholder="Select an Opportunity Status" />
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