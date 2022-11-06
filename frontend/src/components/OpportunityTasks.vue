<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import type { Task } from '@/types/Task'
import { useOpportunityStore } from '@/stores/opportunity'
import TaskService from '@/services/TaskService'
import TaskItem from '@/components/OpportunityTaskItem.vue'
import TaskNewEditDialog from '@/components/TaskNewEditDialog.vue'

const route = useRoute()
const store = useOpportunityStore()
const toast = useToast()
const opportunityId = +route.params.id
const message = ref(false)
const taskNewEditDialog = ref(false)
const tasks = ref<Task[]>([])
const task = ref<Task>({
    description: '',
    due_date: '',
    owner_id: 0,
    priority: 'Medium',
    status: 'Not Started',
    parent_type_id: 'opportunity',
    parent_id: 0,
    owner: undefined
})

onMounted(() => {
    refresh()
})

async function refresh() {
    try {
        const response = await TaskService.getByOpportunity(opportunityId)
        tasks.value = response.data
        message.value = false
    } catch (error: any) {
        if (error.response.status === 404) {
            tasks.value = []
            message.value = true
        }
    }
}

function reset() {
    task.value = {
        id: undefined,
        description: '',
        due_date: '',
        owner_id: 0,
        priority: 'Medium',
        completed_on: new Date(),
        status: 'Not Started',
        parent_type_id: 'opportunity',
        parent_id: 0,
        owner: undefined
    }
}

function openTaskNewEditDialog() {
    task.value.parent_id = opportunityId
    taskNewEditDialog.value = true
}

function cancelTaskNewEditDialog() {
    reset()
    taskNewEditDialog.value = false
}

function afterTaskSave() {
    reset()
    taskNewEditDialog.value = false
    refresh()
    store.getOpportunityDetails(opportunityId)
}

function editTask(taskToEdit: Task) {
    task.value = { ...taskToEdit }
    taskNewEditDialog.value = true
}

async function deleteTask(task: Task) {
    try {
        if (task.id) {
            await TaskService.delete(task.id)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Task ${task.id} deleted`, life: 3000 })
            reset()
            refresh()
            store.getOpportunityDetails(opportunityId)
        }
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error deleting task', life: 3000 })
    }
}

async function changeTaskStatus(task: Task) {
    if (task.status != 'Completed') {
        task.status = 'Completed'
    } else {
        task.status = 'In Progress'
    }

    try {
        if (task.id) {
            await TaskService.update(task.id, task)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Task ${task.id} status updated`, life: 3000 })
        }
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: `Error updating task status`, life: 3000 })
    }
    store.getOpportunityDetails(opportunityId)
}
</script>

<template>
    <TaskNewEditDialog :taskNewEditDialog="taskNewEditDialog" :task="task" @click-cancel="cancelTaskNewEditDialog"
        @click-save="afterTaskSave"></TaskNewEditDialog>
    <p class="mt-3" v-if="message">No tasks found</p>
    <Button label="Add a task" icon="pi pi-plus" class="p-button-sm p-button-success p-button-text"
        @click="openTaskNewEditDialog" />
    <TaskItem v-for="task in tasks" :task="task" :key="task.id" @click-edit="editTask" @click-delete="deleteTask"
        @checkbox-clicked="changeTaskStatus" />
</template>