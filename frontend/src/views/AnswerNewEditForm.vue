<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Answer } from '@/types/Answer'
import { useToast } from 'primevue/usetoast'
import AnswerService from '@/services/AnswerService'
import useUserLoader from '@/composables/useUserLoader'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const message = ref('')
const answerId = ref(0)
const answer = ref<Answer>({
    language_code: 'EN',
    question: '',
    answer: '',
    owner_id: 0,
    is_active: true,
    owner: undefined
})
const { users, loadUsers } = useUserLoader()

if (route.params.id === undefined) {
    message.value = 'Add Answer Entry'
} else {
    answerId.value = +route.params.id
    message.value = 'Edit Answer Entry'
}

onMounted(async () => {
    if (route.params.id !== undefined) {
        try {
            const response = await AnswerService.get(answerId.value)
            answer.value = response.data
        } catch (error: any) {
            if (error.response.status === 404) {    // No records found
                toast.add({ severity: 'error', summary: 'Error', detail: 'No answer entry found', life: 3000 })
            }
        }
    }
})

async function saveAnswer() {
    if (answer.value.owner) { answer.value.owner_id = answer.value.owner.id }

    if (route.params.id === undefined) {
        // Answer entry needs to be added
        try {
            await AnswerService.create(answer.value)
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Answer Entry created', life: 3000 })
        } catch (error: any) {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Error creating Answer Entry', life: 3000 })
        }
        router.push({ name: 'answers' })
    } else {
        // Answer entry needs to be updated 
        try {
            if (answer.value.id !== undefined) {
                await AnswerService.update(answer.value.id, answer.value)
                toast.add({ severity: 'success', summary: 'Successful', detail: `Answer Entry ${answer.value.id} updated`, life: 3000 })
            }
        } catch (error: any) {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Error updating Answer Entry', life: 3000 })
        }
    }
}
</script>

<template>
    <div class="card p-fluid">
        <h5>{{ message }}</h5>
        <div class="field">
            <label for="question">Question</label>
            <Textarea id="question" v-model="answer.question" :autoResize="true" rows="3" cols="30" />
        </div>
        <div class="field">
            <label for="answer">Answer</label>
            <Textarea id="answer" v-model="answer.answer" :autoResize="true" rows="3" cols="30" />
        </div>
        <div class="field">
            <label for="owner">Owner</label>
            <AutoComplete v-model="answer.owner" :suggestions="users" @complete="loadUsers($event)" :dropdown="true"
                optionLabel="full_name" forceSelection></AutoComplete>
        </div>
        <div class="flex justify-content-end mt-5">
            <Button label="Cancel" icon="pi pi-times" class="p-button-text w-7rem mr-3"
                @click="router.push({ name: 'answers' })" />
            <Button label="Save" icon="pi pi-check" class="p-button-text w-7rem" @click="saveAnswer" />
        </div>
    </div>
</template>