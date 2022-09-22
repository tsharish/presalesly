<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import type { OppTemplateTask } from '@/types/OppTemplateTask'
import OppTemplateTaskService from '@/services/OppTemplateTaskService'
import TaskItem from '@/components/OppTemplateTaskItem.vue'
import TaskNewEditDialog from '@/components/OppTemplateTaskNewEditDialog.vue'

const route = useRoute()
const toast = useToast()
const oppTemplateId = +route.params.id
const message = ref(false)
const taskNewEditDialog = ref(false)
const oppTemplateTasks = ref<OppTemplateTask[]>()
const oppTemplateTask = ref<OppTemplateTask>({
    opp_template_id: 0,
    description: '',
    due_date_offset: 0,
    priority: 'Medium',
    is_required: false
})

onMounted(() => {
    refresh()
})

async function refresh() {
    try {
        const response = await OppTemplateTaskService.getByOppTemplate(oppTemplateId)
        oppTemplateTasks.value = response.data
        message.value = false
    } catch (error: any) {
        if (error.response.status === 404) {
            oppTemplateTasks.value = []
            message.value = true
        }
    }
}

function reset() {
    oppTemplateTask.value = {
        opp_template_id: 0,
        description: '',
        due_date_offset: 0,
        priority: 'Medium',
        is_required: false
    }
}

function openTaskNewEditDialog() {
    oppTemplateTask.value.opp_template_id = oppTemplateId
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
}

function editTask(taskToEdit: OppTemplateTask) {
    oppTemplateTask.value = { ...taskToEdit }
    taskNewEditDialog.value = true
}

async function deleteTask(task: OppTemplateTask) {
    try {
        if (task.id) {
            await OppTemplateTaskService.delete(task.id)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Task ${task.id} deleted`, life: 3000 })
            reset()
            refresh()
        }
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: `Error deleting task`, life: 3000 })
    }
}
</script>

<template>
    <TaskNewEditDialog :taskNewEditDialog="taskNewEditDialog" :oppTemplateTask="oppTemplateTask"
        @click-cancel="cancelTaskNewEditDialog" @click-save="afterTaskSave"></TaskNewEditDialog>
    <p class="mt-3" v-if="message">No tasks found</p>
    <Button label="Add a task" icon="pi pi-plus" class="p-button-sm p-button-success p-button-text"
        @click="openTaskNewEditDialog" />
    <TaskItem v-for="task in oppTemplateTasks" :task="task" :key="task.id" @click-edit="editTask"
        @click-delete="deleteTask" />
</template>