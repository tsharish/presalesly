<script setup lang="ts">
import { ref } from 'vue'
import type { Task } from '@/types/Task'
import { formatDate } from '@/composables/useUtils'

const props = defineProps<{
    task: Task
}>()
const emit = defineEmits<{
    (e: 'click-edit', task: Task): void
    (e: 'click-delete', task: Task): void
    (e: 'checkbox-clicked', task: Task): void
}>()
const checked = ref(props.task.status === 'Completed')

function checkboxClicked() {
    checked.value = !checked.value
    emit('checkbox-clicked', props.task)
}
</script>

<template>
    <div class="flex flex-row align-items-center border-top-1 surface-border py-1">
        <span class="mr-3">
            <Checkbox v-model="checked" :binary="true" @click="checkboxClicked"></Checkbox>
        </span>
        <span class="mr-3">
            {{ task.description }}
        </span>
        <span class="mr-2">
            <Tag icon="pi pi-calendar">
                {{ formatDate(new Date(Date.parse(task.due_date + 'T00:00:00'))) }}
            </Tag>
        </span>
        <span>
            <Button icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-warning"
                @click="$emit('click-edit', task)" />
            <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger"
                @click="$emit('click-delete', task)" />
        </span>
    </div>
</template>

<style lang="scss" scoped>
.p-tag {
    font-weight: normal;
    font-size: smaller;
}
</style>