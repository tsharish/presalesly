<script setup lang="ts">
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import type { Question, AnswerRecommendation } from '@/types/Answer'
import { copyToClipboard } from '@/composables/useUtils'
import AnswerService from '@/services/AnswerService'

const toast = useToast()
const question = ref<Question>({
    query: '',
    language_code: 'EN'
})
const recommendations = ref<AnswerRecommendation[]>([])

async function getRecommendations() {
    if (question.value.query.trim() === '') {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Invalid question', life: 3000 })
    } else {
        try {
            const response = await AnswerService.recommend(question.value)
            recommendations.value = response.data
        } catch (error: any) {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Error getting recommendations', life: 3000 })
        }
    }
}

function copy(textToCopy: string) {
    copyToClipboard(textToCopy)
    toast.add({ severity: 'success', summary: 'Copied', detail: 'Answer copied to clipboard', life: 3000 })
}
</script>

<template>
    <div class="card p-fluid">
        <h5>Answer Recommendation</h5>
        <div class="field">
            <label for="question">Question</label>
            <Textarea id="question" v-model="question.query" :autoResize="true" rows="3" cols="30" />
        </div>
        <Button label="Get Answers" icon="pi pi-save" class="w-11rem mb-2" @click="getRecommendations" />
        <div class="max-w-max">
            <Panel class="mt-3" v-for="(recommendation, index) in recommendations" :key="recommendation.answer.id"
                :toggleable="true" :collapsed="index !== 0">
                <template #header>
                    {{ recommendation.answer.question }}
                </template>
                <template #icons>
                    <button class="p-panel-header-icon p-link mr-2" @click="copy(recommendation.answer.answer)">
                        <span class="pi pi-copy"></span>
                    </button>
                </template>
                <div class="flex flex-row justify-content-between align-items-center">
                    <div class="flex flex-grow-1 mr-3">
                        {{ recommendation.answer.answer }}
                    </div>
                    <div class="flex flex-none">
                        <Knob v-model="recommendation.score" :strokeWidth="10" :size="70" readonly></Knob>
                    </div>
                </div>
            </Panel>
        </div>
    </div>
</template>