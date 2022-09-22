<script setup lang="ts">
import type { Answer } from '@/types/Answer'

const props = defineProps<{
    answer: Answer
}>()
</script>

<template>
    <div class="col-12 lg:col-6 xl:col-4">
        <router-link :to="{ name: 'answerEdit', params: { id: answer.id }}">
            <div class="card pt-4 p-3 card-text-color">
                <div class="flex flex-column">
                    <div class="p-2 question-bg-color">
                        <p>{{ answer.question }}</p>
                    </div>
                    <div class="p-2 mt-2">
                        <p>{{ answer.answer }}</p>
                    </div>
                </div>
            </div>
        </router-link>
    </div>
</template>

<style lang="scss" scoped>
.card-text-color {
    color: var(--text-color);
}

.question-bg-color {
    color: var(--primary-color-text);
    background-color: var(--primary-color);
}
</style>