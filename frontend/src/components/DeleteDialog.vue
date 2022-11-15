<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{ deleteDialog: boolean }>()
const emit = defineEmits(['click-no', 'click-yes'])
const deleteDialog = ref(props.deleteDialog)

watch(() => props.deleteDialog, (newVal) => {
    deleteDialog.value = newVal
})
</script>

<template>
    <Dialog v-model:visible="deleteDialog" :style="{ width: '450px' }" header="Confirm Delete" :modal="true"
        @update:visible="$emit('click-no', $event)">
        <!-- Without the @update:visible event handler above, the dialog is not visible the next time 
        the user clicks the Delete icon (https://forum.primefaces.org/viewtopic.php?t=65452) -->
        <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
            <span>Are you sure you want to delete the selected record(s)?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="$emit('click-no', $event)" />
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="$emit('click-yes', $event)" />
        </template>
    </Dialog>
</template>

<style lang="scss" scoped>
.confirmation-content {
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>