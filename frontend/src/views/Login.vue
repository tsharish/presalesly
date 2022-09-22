<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { languages } from '@/constants'

const router = useRouter()  //Need to use useRouter to access router since there is no 'this'
const auth = useAuthStore()
const email = ref('')
const password = ref('')
const languageCode = ref('EN')
const message = ref('')

async function login() {
    if (email.value.trim() === '' || password.value.trim() === '') {
        message.value = 'Email and Password are required fields'
    } else {
        await auth.login(email.value, password.value)

        if (auth.authenticated) {
            auth.loginLanguageCode = languageCode.value
            password.value = ''
            message.value = ''
            router.push({ name: 'home' })
        } else {
            password.value = ''
            message.value = 'Login error - Try again'
        }
    }
}
</script>

<template>
    <div class="flex flex-column justify-content-center align-items-center" style="min-height: 90vh">
        <div class="card p-5 w-full lg:w-3">
            <img alt="Presalely logo" src="@/assets/logo.png" class="w-full mb-3" />
            <InputText id="email" type="text" v-model="email" placeholder="Email" class="w-full mb-3"
                @keyup.enter="login" />
            <InputText id="password" type="password" v-model="password" placeholder="Password" class="w-full mb-3"
                @keyup.enter="login" />
            <Dropdown id="languageCode" v-model="languageCode" :options="languages" optionLabel="description"
                optionValue="code" class="w-full mb-3" />
            <Button label="Log on" icon="pi pi-user" class="w-full" @click="login"></Button>
            <Message severity="error" v-if="message" :closable="false">{{ message }}</Message>
        </div>
    </div>
</template>