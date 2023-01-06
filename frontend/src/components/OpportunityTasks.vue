<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { FilterMatchMode, FilterOperator } from 'primevue/api'
import { useToast } from 'primevue/usetoast'

import PrimeDataTable from '@/components/PrimeDataTable.vue'
import TaskService from '@/services/TaskService'
import OppTasksService from '@/services/OppTasksService'
import useDataTable from '@/composables/useDataTable'
import { useAuthStore } from '@/stores/auth'
import { useOpportunityStore } from '@/stores/opportunity'
import type { Task } from '@/types/Task'
import TaskNewEditDialog from '@/components/TaskNewEditDialog.vue'
import DeleteDialog from '@/components/DeleteDialog.vue'
import { priorities, taskStatuses } from '@/constants'
import useUserLoader from '@/composables/useUserLoader'

const route = useRoute()
const toast = useToast()
const authStore = useAuthStore()
const oppStore = useOpportunityStore()
const opportunityId = +route.params.id
const oppTasksService = new OppTasksService(opportunityId)
const { newEditDialog, deleteDialog, refreshTime, refresh,
    hideNewEditDialog, hideDeleteDialog } = useDataTable()
const filters = ref({
    'description': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'due_date': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
    'priority': { value: null, matchMode: FilterMatchMode.IN },
    'status': { value: null, matchMode: FilterMatchMode.IN },
    'owner_id': { value: null, matchMode: FilterMatchMode.EQUALS }
})
const sort = ref([{ field: "due_date", order: 1 }])
const { users, loadingUsers, loadUsers } = useUserLoader()
const task = ref<Task>({
    description: '',
    due_date: '',
    owner_id: 0,
    priority: 'Medium',
    status: 'Not Started',
    opportunity_id: 0,
    owner: undefined
})

onMounted(() => {
    refresh()
})

function reset() {
    task.value = {
        id: undefined,
        description: '',
        due_date: '',
        owner_id: 0,
        priority: 'Medium',
        completed_on: new Date(),
        status: 'Not Started',
        opportunity_id: 0,
        owner: undefined
    }
}

function openNewEditDialog() {
    reset()
    task.value.opportunity_id = opportunityId
    newEditDialog.value = true
}

function editRecord(recordToEdit: Task) {
    task.value = { ...recordToEdit }
    newEditDialog.value = true
}

function afterTaskSave() {
    reset()
    newEditDialog.value = false
    refresh()
    oppStore.getOpportunityDetails(opportunityId)
}

function confirmDeleteRecord(recordToDelete: Task) {
    task.value = recordToDelete
    deleteDialog.value = true
}

async function deleteSelectedRecords() {
    try {
        if (task.value.id !== undefined) {
            await TaskService.delete(task.value.id)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Task ${task.value.id} deleted`, life: 3000 })
        }
        deleteDialog.value = false
        reset()
        refresh()
        oppStore.getOpportunityDetails(opportunityId)
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error deleting task', life: 3000 })
    }
}

function editDeleteDisabled(task: Task) {
    return !(task.owner_id === authStore.user?.id
        || oppStore.opportunity.owner_id === authStore.user?.id
        || authStore.user?.role_id === 'ADMIN')
}

function getPriorityClass(priority: string) {
    const priorityClassMap: { [key: string]: string } = {
        "Low": "low",
        "Medium": "medium",
        "High": "high",
        "Very High": "very-high"
    }
    return priorityClassMap[priority]
}
</script>

<template>
    <PrimeDataTable :ApiService="oppTasksService" :initialFilters="filters" :initialSort="sort" :refresh="refreshTime"
        :showHeader="false" :showRefreshOnToolbar="true" @click-new="openNewEditDialog">
        <template #empty>
            No tasks found.
        </template>
        <Column field="description" header="Description" :sortable="true">
            <template #filter="{ filterModel }">
                <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                    placeholder="Search by Task Description" />
            </template>
        </Column>
        <Column field="due_date" header="Due Date" dataType="date" :sortable="true" style="min-width:10rem">
            <template #filter="{ filterModel }">
                <Calendar v-model="filterModel.value" dateFormat="mm/dd/yy" placeholder="mm/dd/yyyy" />
            </template>
        </Column>
        <Column field="priority" header="Priority" :sortable="true" :showFilterMatchModes="false"
            :filterMenuStyle="{ 'width': '15rem' }">
            <template #body="{ data }">
                <span class="priority-badge" :class="getPriorityClass(data.priority)">{{ data.priority }}</span>
            </template>
            <template #filter="{ filterModel }">
                <div class="mb-3">Select Task Priority</div>
                <MultiSelect v-model="filterModel.value" :options="priorities" optionLabel="description"
                    optionValue="id" placeholder="Any" class="p-column-filter"></MultiSelect>
            </template>
        </Column>
        <Column field="status" header="Status" :sortable="true" :showFilterMatchModes="false"
            :filterMenuStyle="{ 'width': '15rem' }">
            <template #filter="{ filterModel }">
                <div class="mb-3">Select Task Status</div>
                <MultiSelect v-model="filterModel.value" :options="taskStatuses" optionLabel="description"
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
        <Column :exportable="false" style="min-width:8rem">
            <template #body="{ data }">
                <Button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-warning mr-2"
                    @click="editRecord(data)" :disabled="editDeleteDisabled(data)" />
                <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger"
                    @click="confirmDeleteRecord(data)" :disabled="editDeleteDisabled(data)" />
            </template>
        </Column>
    </PrimeDataTable>
    <TaskNewEditDialog :taskNewEditDialog="newEditDialog" :task="task" @click-cancel="hideNewEditDialog"
        @click-save="afterTaskSave"></TaskNewEditDialog>

    <DeleteDialog :deleteDialog="deleteDialog" @click-no="hideDeleteDialog(reset)" @click-yes="deleteSelectedRecords">
    </DeleteDialog>
</template>

<style scoped>
.priority-badge {
    border-radius: 10px;
    padding: .25em .5rem;
    text-transform: uppercase;
    font-weight: 700;
    font-size: 12px;
    letter-spacing: .3px;
}

.priority-badge.low {
    background-color: #B3E5FC;
    color: #23547B;
}

.priority-badge.medium {
    background-color: #C8E6C9;
    color: #256029;
}

.priority-badge.high {
    background-color: #FFD8B2;
    color: #805B36;
}

.priority-badge.very-high {
    background-color: #FFCDD2;
    color: #C63737;
}
</style>