<script setup lang="ts">
import { computed } from 'vue'
import type { OpportunityDetails } from '@/types/Opportunity'
import { formatCurrency } from '@/composables/useUtils'

const props = defineProps<{
    opportunity: OpportunityDetails
}>()

const aiScore = computed(() => {
    return props.opportunity?.ai_score === null ? 0 : props.opportunity?.ai_score
})
</script>

<template>
    <div class="card p-3">
        <div class="flex justify-content-between align-items-center">
            <div class="flex flex-grow-1 flex-column mr-5 md:mr-8">
                <div>
                    <p class="text-2xl font-bold mb-0">{{ opportunity?.name }}</p>
                    <p>Account: {{ opportunity?.account.name }}</p>
                </div>
                <div class="flex justify-content-between mt-3">
                    <div>
                        <p class="text-sm mb-0">Stage</p>
                        <p class="text-xl mt-0">
                            {{ opportunity?.stage.description }}
                        </p>
                    </div>
                    <div>
                        <p class="text-sm mb-0">Expected Amount</p>
                        <p class="text-xl mt-0">
                            {{ formatCurrency(opportunity?.expected_amount, opportunity?.expected_amount_curr_code) }}
                        </p>
                    </div>
                    <div>
                        <p class="text-sm mb-0">Probability</p>
                        <p class="text-xl mt-0">
                            {{ opportunity?.probability_percent }}%
                        </p>
                    </div>
                    <div>
                        <p class="text-sm mb-0">Close Date</p>
                        <p class="text-xl mt-0">
                            {{ opportunity?.close_date }}
                        </p>
                    </div>
                    <div class="hidden md:block">
                        <p class="text-sm mb-0">Owner</p>
                        <p class="text-xl mt-0">
                            {{ opportunity?.owner.full_name }}
                        </p>
                    </div>
                </div>
                <div class="flex justify-content-between mt-3">
                    <div>
                        Not Started Tasks: <Tag severity="info" rounded>{{ opportunity?.not_started_task_count }}</Tag>
                    </div>
                    <div>
                        In Progress Tasks: <Tag severity="warning" rounded>{{ opportunity?.in_progress_task_count }}
                        </Tag>
                    </div>
                    <div>
                        Completed Tasks: <Tag severity="success" rounded>{{ opportunity?.completed_task_count }}</Tag>
                    </div>
                </div>
            </div>
            <div class="flex flex-none flex-column">
                <div class="flex justify-content-center">AI Score</div>
                <div class="flex justify-content-center">
                    <Knob v-model="aiScore" :strokeWidth="10" readonly></Knob>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.p-tag {
    font-size: small
}
</style>