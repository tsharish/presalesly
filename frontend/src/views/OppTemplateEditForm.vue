<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import type { OppTemplate } from '@/types/OppTemplate'
import OppTemplateService from '@/services/OppTemplateService'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const oppTemplate = ref<OppTemplate>({
    description: '',
    opp_template_tasks: []
})
const oppTemplateId = +route.params.id
const items = ref([
    { label: 'Tasks', icon: 'pi pi-check-square', to: 'tasks' },
    /* {label: 'Quals', icon: 'pi pi-check-square', to: 'quals'} */
])

onMounted(async () => {
    try {
        const response = await OppTemplateService.get(oppTemplateId)
        oppTemplate.value = response.data
        router.push('tasks')    //This is needed to ensure that the Tasks tab is automatically loaded 
    } catch (error: any) {
        if (error.response.status === 404) {    // No records found
            toast.add({ severity: 'error', summary: 'Error', detail: 'No opportunity templates found', life: 3000 })
        }
    }
})

async function saveRecord() {
    try {
        await OppTemplateService.update(oppTemplateId, oppTemplate.value)
        toast.add({ severity: 'success', summary: 'Successful', detail: 'Opportunity template changes saved', life: 3000 })
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error saving changes', life: 3000 })
    }
}
</script>

<template>
    <div class="card p-fluid" style="width: 50%; min-width: 450px;">
        <h5>Opportunity Template</h5>
        <div class="field">
            <label for="description">Description</label>
            <InputText id="description" v-model.trim="oppTemplate.description" />
        </div>
        <div class="flex justify-content-end mt-3">
            <Button label="Save" icon="pi pi-check" class="p-button-text w-7rem" @click="saveRecord" />
        </div>
    </div>
    <div class="card mt-3 py-1">
        <TabMenu :model="items" />
        <div class="pt-3">
            <router-view />
        </div>
    </div>
</template>