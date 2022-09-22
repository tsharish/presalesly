<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useToast } from 'primevue/usetoast'
import { useOpportunityStore } from '@/stores/opportunity'
import OpportunityHeader from '@/components/OpportunityHeaderCard.vue'

const route = useRoute()
const router = useRouter()
const store = useOpportunityStore()
const toast = useToast()
const { opportunity } = storeToRefs(store)

const items = ref([
    { label: 'Tasks', icon: 'pi pi-check-square', to: 'tasks' },
    /* {label: 'Quals', icon: 'pi pi-check-square', to: 'quals'} */
])

onMounted(async () => {
    try {
        await store.getOpportunityDetails(+route.params.id)     //'+' converts string to numbers in JS
        router.push('tasks')    //This is needed to ensure that the Tasks tab is automatically loaded 
    } catch (error: any) {
        if (error.response.status === 404) {    // No records found
            toast.add({ severity: 'error', summary: 'Error', detail: 'No opportunity found', life: 3000 })
        }
    }
})
</script>

<template>
    <OpportunityHeader v-if="opportunity.id" :opportunity="opportunity" />
    <div class="card mt-3 py-1">
        <TabMenu :model="items" />
        <div class="pt-3">
            <router-view />
        </div>
    </div>
</template>