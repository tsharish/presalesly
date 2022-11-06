<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { FilterMatchMode, FilterOperator } from 'primevue/api'
import { useToast } from 'primevue/usetoast'

import PrimeDataTable from '@/components/PrimeDataTable.vue'
import OpportunityService from '@/services/OpportunityService'
import useDataTable from '@/composables/useDataTable'
import { formatCurrency, calculateDateWithOffset } from '@/composables/useUtils'
import { useAuthStore } from '@/stores/auth'
import type { Opportunity, OpportunityDetails } from '@/types/Opportunity'
import type { OppStage } from '@/types/OppStage'
import type { OppTemplate } from '@/types/OppTemplate'
import OppStageService from '@/services/OppStageService'
import DeleteDialog from '@/components/DeleteDialog.vue'
import { currencies, oppStatuses } from '@/constants'
import useUserLoader from '@/composables/useUserLoader'
import useAccountLoader from '@/composables/useAccountLoader'
import OppTemplateService from '@/services/OppTemplateService'

const auth = useAuthStore()
const toast = useToast()
const { newEditDialog, deleteDialog, refreshTime, refresh,
    openNewEditDialog, hideNewEditDialog, hideDeleteDialog } = useDataTable()
const filters = ref({
    'id': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    'name': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'account.name': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'expected_amount': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    'stage_id': { value: null, matchMode: FilterMatchMode.IN },
    'close_date': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
    'status': { value: null, matchMode: FilterMatchMode.IN },
    'owner_id': { value: null, matchMode: FilterMatchMode.EQUALS }
})
const { users, loadingUsers, loadUsers } = useUserLoader()
const { accounts, loadAccounts } = useAccountLoader()
const opportunity = ref<Opportunity>({
    name: '',
    expected_amount: 0,
    expected_amount_curr_code: 'USD',
    start_date: '',
    close_date: '',
    probability: 0,
    owner_id: 0,
    account_id: 0,
    stage_id: 0,
    owner: undefined,
    account: undefined
})
const startDate = ref(new Date())
const closeDate = ref(new Date())
const oppStages = ref<OppStage[]>([])
const oppTemplates = ref<OppTemplate[]>([])

onMounted(async () => {
    refresh()

    //Stages and Templates are only loaded initially since they are not expected to change frequently
    try {
        const response = await OppStageService.getAll({ lang_code: auth.loginLanguageCode })
        oppStages.value = response.data.items
    } catch (error: any) {
        if (error.response.status === 404) {    // No records found
            oppStages.value = []
        }
    }

    try {
        const response = await OppTemplateService.getAll({})
        oppTemplates.value = response.data.items
    } catch (error: any) {
        if (error.response.status === 404) {    // No records found
            oppTemplates.value = []
        }
    }
})

function updateProbabilityPercent() {
    // This function updates the probability percent field in the NewEdit dialog based on the selected stage
    const stage_probability = oppStages.value.find(oppStage => oppStage.id === opportunity.value.stage_id)?.default_probability
    opportunity.value.probability_percent = stage_probability !== undefined ? stage_probability * 100 : 0
}

function reset() {
    opportunity.value = {
        id: undefined,
        external_id: '',
        name: '',
        expected_amount: 0,
        expected_amount_curr_code: 'USD',
        start_date: '',
        close_date: '',
        probability: 0,
        probability_percent: 0,
        owner_id: 0,
        account_id: 0,
        stage_id: 0,
        opp_template_id: undefined,
        owner: undefined,
        account: undefined
    }
    startDate.value = new Date()
    closeDate.value = new Date()
}

function editRecord(recordToEdit: OpportunityDetails) {
    opportunity.value = { ...recordToEdit }
    startDate.value = calculateDateWithOffset(recordToEdit.start_date)
    closeDate.value = calculateDateWithOffset(recordToEdit.close_date)
    newEditDialog.value = true
}

async function saveRecord() {
    opportunity.value.start_date = startDate.value.getFullYear() + '-' + (startDate.value.getMonth() + 1) + '-' + startDate.value.getDate()
    opportunity.value.close_date = closeDate.value.getFullYear() + '-' + (closeDate.value.getMonth() + 1) + '-' + closeDate.value.getDate()
    if (opportunity.value.account) { opportunity.value.account_id = opportunity.value.account.id }
    if (opportunity.value.owner) { opportunity.value.owner_id = opportunity.value.owner.id }
    if (opportunity.value.probability_percent) { opportunity.value.probability = opportunity.value.probability_percent / 100 }

    try {
        if (opportunity.value.id) {    // Record must be edited
            await OpportunityService.update(opportunity.value.id, opportunity.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Opportunity ${opportunity.value.id} updated`, life: 3000 })
        }
        else {                      // Record must be created
            await OpportunityService.create(opportunity.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Opportunity created', life: 3000 })
        }
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error saving the record', life: 3000 })
    }
    newEditDialog.value = false
    reset()
    refresh()
}

function confirmDeleteRecord(recordToDelete: Opportunity) {
    opportunity.value = recordToDelete
    deleteDialog.value = true
}

async function deleteSelectedRecords() {
    try {
        if (opportunity.value.id !== undefined) {
            await OpportunityService.delete(opportunity.value.id)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Opportunity ${opportunity.value.id} deleted`, life: 3000 })
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
        <PrimeDataTable :ApiService="OpportunityService" :initialFilters="filters" title="Manage Opportunities"
            :refresh="refreshTime" @click-new="openNewEditDialog(reset)">
            <Column field="name" header="Opportunity Name" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Opportunity Name" />
                </template>
            </Column>
            <Column field="account.name" header="Account Name" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Account Name" />
                </template>
            </Column>
            <Column field="expected_amount" header="Expected Amount" dataType="numeric" :sortable="true">
                <template #filter="{ filterModel }">
                    <InputNumber v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Expected Amount" />
                </template>
                <template #body="slotProps">
                    {{ formatCurrency(slotProps.data.expected_amount, slotProps.data.expected_amount_curr_code) }}
                </template>
            </Column>
            <Column field="stage.description" sortField="stage_id" filterField="stage_id" header="Stage"
                :sortable="true" :showFilterMatchModes="false" :filterMenuStyle="{ 'width': '15rem' }">
                <template #filter="{ filterModel }">
                    <div class="mb-3">Select Opportunity Stage</div>
                    <MultiSelect v-model="filterModel.value" :options="oppStages" optionLabel="description"
                        optionValue="id" placeholder="Any" class="p-column-filter"></MultiSelect>
                </template>
            </Column>
            <Column field="close_date" header="Close Date" dataType="date" :sortable="true" style="min-width:10rem">
                <template #body="{ data }">
                    {{ data.close_date }}
                </template>
                <template #filter="{ filterModel }">
                    <Calendar v-model="filterModel.value" dateFormat="mm/dd/yy" placeholder="mm/dd/yyyy" />
                </template>
            </Column>
            <Column field="status" header="Status" :sortable="true" :showFilterMatchModes="false"
                :filterMenuStyle="{ 'width': '15rem' }">
                <template #filter="{ filterModel }">
                    <div class="mb-3">Select Opportunity Status</div>
                    <MultiSelect v-model="filterModel.value" :options="oppStatuses" optionLabel="description"
                        optionValue="id" placeholder="Any" class="p-column-filter"></MultiSelect>
                </template>
            </Column>
            <Column field="owner.full_name" filterField="owner_id" header="Owner" :showFilterMatchModes="false"
                :filterMenuStyle="{ 'width': '15rem' }">
                <template #filter="{ filterModel }">
                    <div class="mb-3">Select Owner</div>
                    <Dropdown v-model="filterModel.value" :options="users" optionLabel="full_name" optionValue="id"
                        placeholder="Any" :filter="true" @filter="loadUsers" @show="loadUsers" :loading="loadingUsers">
                    </Dropdown>
                </template>
            </Column>
            <Column :exportable="false" style="min-width:8rem; float: center">
                <template #body="slotProps">
                    <Button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-warning mr-1"
                        @click="editRecord(slotProps.data)" />
                    <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger"
                        @click="confirmDeleteRecord(slotProps.data)" />
                </template>
            </Column>
        </PrimeDataTable>

        <Dialog v-model:visible="newEditDialog" :style="{ width: '450px' }" header="Opportunity Details" :modal="true"
            class="p-fluid">
            <div class="field">
                <label for="externalID">External ID</label>
                <InputText id="externalID" v-model.trim="opportunity.external_id" autofocus />
            </div>
            <div class="field">
                <label for="opportunityName">Opportunity Name</label>
                <InputText id="opportunityName" v-model.trim="opportunity.name" />
            </div>
            <div class="form-grid grid">
                <div class="field col-fixed" style="width:200px">
                    <label for="expectedAmount">Expected Amount</label>
                    <InputNumber id="expectedAmount" v-model="opportunity.expected_amount" mode="decimal"
                        :minFractionDigits="2" />
                </div>
                <div class="field col-fixed" style="width:200px">
                    <label for="currencyCode">Currency</label>
                    <Dropdown id="currencyCode" v-model="opportunity.expected_amount_curr_code" :options="currencies"
                        optionLabel="name" optionValue="code" />
                </div>
            </div>
            <div class="form-grid grid">
                <div class="field col">
                    <label for="startDate">Start Date</label>
                    <Calendar id="startDate" v-model="startDate" :showIcon="true" />
                </div>
                <div class="field col">
                    <label for="closeDate">Close Date</label>
                    <Calendar id="closeDate" v-model="closeDate" :showIcon="true" />
                </div>
            </div>
            <div class="field">
                <label for="probability">Probability</label>
                <InputNumber id="probability" v-model="opportunity.probability_percent" mode="decimal"
                    :minFractionDigits="2" suffix="%" />
            </div>
            <div class="field">
                <label for="account">Account</label>
                <AutoComplete v-model="opportunity.account" :suggestions="accounts" @complete="loadAccounts($event)"
                    :dropdown="true" optionLabel="name" forceSelection></AutoComplete>
            </div>
            <div class="field">
                <label for="owner">Owner</label>
                <AutoComplete v-model="opportunity.owner" :suggestions="users" @complete="loadUsers($event)"
                    :dropdown="true" optionLabel="full_name" forceSelection></AutoComplete>
            </div>
            <div class="field">
                <label for="stage">Stage</label>
                <Dropdown id="stage" v-model="opportunity.stage_id" :options="oppStages" optionLabel="description"
                    optionValue="id" @change="updateProbabilityPercent" placeholder="Select a Stage" />
            </div>
            <div class="field" v-if="opportunity.id === undefined">
                <label for="template">Template</label>
                <Dropdown id="template" v-model="opportunity.opp_template_id" :options="oppTemplates"
                    optionLabel="description" optionValue="id" placeholder="Select a Template" />
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