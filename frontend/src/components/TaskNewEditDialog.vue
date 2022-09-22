<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import type { Task } from '@/types/Task'
import { priorities, taskStatuses } from '@/constants'
import { useToast } from 'primevue/usetoast'
import { calculateDateWithOffset } from '@/composables/useUtils'
import useUserLoader from '@/composables/useUserLoader'
import TaskService from '@/services/TaskService'

const toast = useToast()
const { users, loadingUsers, loadUsers } = useUserLoader()
const props = defineProps<{
    taskNewEditDialog: boolean,
    task: Task
}>()
const emit = defineEmits(['click-cancel', 'click-save'])
const dueDate = ref(new Date())

onMounted(async () => {
    loadUsers()
})

watch(
    () => props.task.due_date,
    (newValue) => {
        dueDate.value = calculateDateWithOffset(newValue)
    })

async function saveRecord(event: any) {
    props.task.due_date = dueDate.value.getFullYear() + '-' + (dueDate.value.getMonth() + 1) + '-' + dueDate.value.getDate()
    try {
        if (props.task.id) {    // Task must be updated
            await TaskService.update(props.task.id, props.task)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Task ${props.task.id} updated`, life: 3000 })
        } else {                // Task must be created
            await TaskService.create(props.task)
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Task created', life: 3000 })
        }
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error saving the record', life: 3000 })
    }
    emit('click-save', event)
}
</script>

<template>
    <Dialog v-model:visible="taskNewEditDialog" :style="{width: '450px'}" header="Task Details" :modal="true"
        class="p-fluid" @update:visible="$emit('click-cancel', $event)">
        <div class="field">
            <label for="description">Description</label>
            <InputText id="description" v-model.trim="task.description" autofocus />
        </div>
        <div class="field">
            <label for="dueDate">Due Date</label>
            <Calendar id="dueDate" v-model="dueDate" :showIcon="true" />
        </div>
        <div class="field">
            <label for="owner">Owner</label>
            <Dropdown id="owner" v-model="task.owner_id" :options="users" optionLabel="full_name" optionValue="id"
                :loading="loadingUsers" showClear placeholder="Select an Owner" @show="loadUsers" />
        </div>
        <div class="field">
            <label for="priority">Priority</label>
            <Dropdown id="priority" v-model="task.priority" :options="priorities" optionLabel="description"
                optionValue="id" placeholder="Select a Priority" />
        </div>
        <div class="field">
            <label for="status">Status</label>
            <Dropdown id="status" v-model="task.status" :options="taskStatuses" optionLabel="description"
                optionValue="id" placeholder="Select a Status" />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="$emit('click-cancel', $event)" />
            <Button label="Save" icon="pi pi-check" class="p-button-text" @click="saveRecord" />
        </template>
    </Dialog>
</template>