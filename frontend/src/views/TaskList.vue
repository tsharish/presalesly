<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { FilterMatchMode, FilterOperator } from 'primevue/api'
import { useToast } from 'primevue/usetoast'

import PrimeDataTable from '@/components/PrimeDataTable.vue'
import TaskService from '@/services/TaskService'
import useDataTable from '@/composables/useDataTable'
import { capitalize } from '@/composables/useUtils'
import type { Task } from '@/types/Task'
import TaskNewEditDialog from '@/components/TaskNewEditDialog.vue'
import DeleteDialog from '@/components/DeleteDialog.vue'
import { priorities, taskStatuses } from '@/constants'

const toast = useToast()
const { deleteDialog, refreshTime, refresh, hideDeleteDialog } = useDataTable()
const filters = ref({
    'description': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'parent_type_id': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
    'parent_id': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    'due_date': { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
    'priority': { value: null, matchMode: FilterMatchMode.IN },
    'status': { value: null, matchMode: FilterMatchMode.IN }
})
const taskNewEditDialog = ref(false)
const task = ref<Task>({
    description: '',
    due_date: '',
    owner_id: 0,
    priority: 'Medium',
    status: 'Not Started',
    parent_type_id: '',
    parent_id: 0
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
        parent_type_id: '',
        parent_id: 0
    }
}

function editRecord(recordToEdit: Task) {
    task.value = { ...recordToEdit }
    taskNewEditDialog.value = true
}

function afterTaskSave() {
    taskNewEditDialog.value = false
    reset()
    refresh()
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
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error deleting the record', life: 3000 })
    }
}
</script>

<template>
    <div class="card">
        <PrimeDataTable :ApiService="TaskService" :initialFilters="filters" title="Manage Tasks" :refresh="refreshTime"
            :showToolbar="false">
            <Column field="description" header="Description" :sortable="true">
                <template #filter="{filterModel}">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Task Description" />
                </template>
            </Column>
            <Column field="parent_type_id" header="Parent Type" :sortable="true">
                <template #filter="{filterModel}">
                    <InputText type="text" v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by Parent Type" />
                </template>
                <template #body="slotProps">
                    {{ capitalize(slotProps.data.parent_type_id) }}
                </template>
            </Column>
            <Column field="parent_id" header="Parent ID" dataType="numeric" :sortable="true">
                <template #filter="{filterModel}">
                    <InputNumber v-model="filterModel.value" class="p-column-filter"
                        placeholder="Search by parent ID" />
                </template>
            </Column>
            <Column field="due_date" header="Due Date" dataType="date" :sortable="true" style="min-width:10rem">
                <template #filter="{filterModel}">
                    <Calendar v-model="filterModel.value" dateFormat="mm/dd/yy" placeholder="mm/dd/yyyy" />
                </template>
            </Column>
            <Column field="priority" header="Priority" :sortable="true" :showFilterMatchModes="false"
                :filterMenuStyle="{'width':'15rem'}">
                <template #filter="{filterModel}">
                    <div class="mb-3">Select Task Priority</div>
                    <MultiSelect v-model="filterModel.value" :options="priorities" optionLabel="description"
                        optionValue="id" placeholder="Any" class="p-column-filter"></MultiSelect>
                </template>
            </Column>
            <Column field="status" header="Status" :sortable="true" :showFilterMatchModes="false"
                :filterMenuStyle="{'width':'15rem'}">
                <template #filter="{filterModel}">
                    <div class="mb-3">Select Task Status</div>
                    <MultiSelect v-model="filterModel.value" :options="taskStatuses" optionLabel="description"
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

        <TaskNewEditDialog :taskNewEditDialog="taskNewEditDialog" :task="task" @click-cancel="taskNewEditDialog = false"
            @click-save="afterTaskSave"></TaskNewEditDialog>

        <DeleteDialog :deleteDialog="deleteDialog" @click-no="hideDeleteDialog(reset)"
            @click-yes="deleteSelectedRecords"></DeleteDialog>
    </div>
</template>