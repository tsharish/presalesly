<script setup lang="ts">
import type { OppTemplateTask } from '@/types/OppTemplateTask'

const props = defineProps<{
    task: OppTemplateTask
}>()
const emit = defineEmits<{
    (e: 'click-edit', task: OppTemplateTask): void
    (e: 'click-delete', task: OppTemplateTask): void
}>()
</script>

<template>
    <div class="flex flex-row align-items-center border-top-1 surface-border py-1">
        <span class="mr-3">
            {{ task.description }}
        </span>
        <span class="mr-2">
            <Tag icon="pi pi-calendar">
                + {{ task.due_date_offset }} days
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
    font-size: small;
}
</style>