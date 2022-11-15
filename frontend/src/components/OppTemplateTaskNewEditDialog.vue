<script setup lang="ts">
import { ref, watch } from 'vue'
import type { OppTemplateTask } from '@/types/OppTemplateTask'
import { priorities } from '@/constants'
import { useToast } from 'primevue/usetoast'
import OppTemplateTaskService from '@/services/OppTemplateTaskService'

const toast = useToast()
const props = defineProps<{
    taskNewEditDialog: boolean,
    oppTemplateTask: OppTemplateTask
}>()
const emit = defineEmits(['click-cancel', 'click-save'])
const taskNewEditDialog = ref(props.taskNewEditDialog)
const oppTemplateTask = ref(props.oppTemplateTask)

watch(() => props.taskNewEditDialog, (newVal) => {
    taskNewEditDialog.value = newVal
})

watch(() => props.oppTemplateTask, (newVal) => {
    oppTemplateTask.value = newVal
})

async function saveRecord(event: any) {
    try {
        if (oppTemplateTask.value.id) {     // Task must be updated
            await OppTemplateTaskService.update(oppTemplateTask.value.id, oppTemplateTask.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: `Task ${oppTemplateTask.value.id} updated`, life: 3000 })
        } else {                            // Task must be created
            await OppTemplateTaskService.create(oppTemplateTask.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Task created', life: 3000 })
        }
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error saving the record', life: 3000 })
    }
    emit('click-save', event)
}
</script>

<template>
    <Dialog v-model:visible="taskNewEditDialog" :style="{ width: '450px' }" header="Template Task Details" :modal="true"
        class="p-fluid" @update:visible="$emit('click-cancel', $event)">
        <div class="field">
            <label for="description">Description</label>
            <InputText id="description" v-model.trim="oppTemplateTask.description" autofocus />
        </div>
        <div class="field">
            <label for="dueDateOffset">Due Date Offset</label>
            <InputNumber id="dueDateOffset" v-model="oppTemplateTask.due_date_offset" suffix=" days" />
        </div>
        <div class="field">
            <label for="priority">Priority</label>
            <Dropdown id="priority" v-model="oppTemplateTask.priority" :options="priorities" optionLabel="description"
                optionValue="id" placeholder="Select a default priority" />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="$emit('click-cancel', $event)" />
            <Button label="Save" icon="pi pi-check" class="p-button-text" @click="saveRecord" />
        </template>
    </Dialog>
</template>