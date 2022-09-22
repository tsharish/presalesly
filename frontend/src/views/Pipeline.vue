<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import type { OpportunityDetails } from '@/types/Opportunity'
import PipelineCard from '@/components/PipelineCard.vue'
import OpportunityService from '@/services/OpportunityService'

const auth = useAuthStore()
const opportunities = ref<OpportunityDetails[]>([])

onMounted(async () => {
    try {
        const response = await OpportunityService.getOpen({ lang_code: auth.loginLanguageCode })
        opportunities.value = response.data.items
    } catch (error: any) {
        if (error.response.status === 404) {    // No records found
            opportunities.value = []
        }
    }
})
</script>

<template>
    <div class="grid">
        <PipelineCard v-for="opportunity in opportunities" :opportunity="opportunity" :key="opportunity.id" />
    </div>
</template>