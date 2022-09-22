<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { Answer } from '@/types/Answer'
import AnswerLibraryCard from '@/components/AnswerLibraryCard.vue'
import AnswerService from '@/services/AnswerService'

const router = useRouter()
const answers = ref<Answer[]>([])

onMounted(async () => {
    try {
        const response = await AnswerService.getAll({})
        answers.value = response.data.items
    } catch (error: any) {
        if (error.response.status === 404) {    // No records found
            answers.value = []
        }
    }
})
</script>

<template>
    <div class="mb-3">
        <Button label="Add an Answer Entry" icon="pi pi-plus" class="p-button-outlined"
            @click="router.push({ name: 'answerAdd' })" />
    </div>
    <div class="grid">
        <AnswerLibraryCard v-for="answer in answers" :answer="answer" :key="answer.id" />
    </div>
</template>