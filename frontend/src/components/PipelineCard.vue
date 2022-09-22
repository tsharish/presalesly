<script setup lang="ts">
import { computed } from 'vue'
import type { OpportunityDetails } from '@/types/Opportunity'
import { formatCurrency } from '@/composables/useUtils'

const props = defineProps<{
    opportunity: OpportunityDetails
}>()

const aiScore = computed(() => {
    return props.opportunity.ai_score === null ? 0 : props.opportunity.ai_score
})
</script>

<template>
    <div class="col-12 lg:col-6 xl:col-4">
        <router-link :to="{ name: 'opportunity', params: { id: opportunity.id }}">
            <div class="card p-3 card-text-color">
                <div class="flex justify-content-between">
                    <div class="flex flex-grow-1 flex-column mr-5">
                        <div>
                            <p class="text-xl font-bold mb-0">{{ opportunity.name }}</p>
                            <p>Account: {{ opportunity.account.name }}</p>
                            <p>
                                Stage:
                                <span class="text-pink-600 font-bold">
                                    {{ opportunity.stage.description?.toUpperCase() }}
                                </span>
                            </p>
                        </div>
                        <div class="flex justify-content-between mt-3">
                            <div>
                                <p class="text-lg">
                                    {{ formatCurrency(opportunity.expected_amount,
                                    opportunity.expected_amount_curr_code) }}
                                </p>
                            </div>
                            <div>
                                <p class="text-lg">
                                    {{ opportunity.close_date }}
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="flex flex-none flex-column">
                        <div class="flex justify-content-center">AI Score</div>
                        <div class="flex justify-content-center">
                            <Knob v-model="aiScore" :strokeWidth="10" :size="80" readonly></Knob>
                        </div>
                    </div>
                </div>
                <div class="flex justify-content-between mt-3">
                    <div>
                        Not Started: <Tag severity="info" rounded>{{ opportunity.not_started_task_count }}</Tag>
                    </div>
                    <div>
                        In Progress: <Tag severity="warning" rounded>{{ opportunity.in_progress_task_count }}</Tag>
                    </div>
                    <div>
                        Completed: <Tag severity="success" rounded>{{ opportunity.completed_task_count }}</Tag>
                    </div>
                </div>
            </div>
        </router-link>
    </div>
</template>

<style lang="scss" scoped>
.p-tag {
    font-size: small
}

.card-text-color {
    color: var(--text-color);
}
</style>