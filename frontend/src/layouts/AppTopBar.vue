<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const emit = defineEmits(['menu-toggle', 'topbar-menu-toggle'])

function onMenuToggle(event: any) {
	emit('menu-toggle', event)
}

function onTopbarMenuToggle(event: any) {
	emit('topbar-menu-toggle', event)
}

function logout() {
	auth.logout()
	router.push('/login')
}
</script>

<template>
	<div class="layout-topbar">
		<button class="p-link layout-menu-button layout-topbar-button" @click="onMenuToggle">
			<i class="pi pi-bars"></i>
		</button>

		<button class="p-link layout-topbar-menu-button layout-topbar-button" v-styleclass="{
			selector: '@next', enterClass: 'hidden', enterActiveClass: 'scalein',
			leaveToClass: 'hidden', leaveActiveClass: 'fadeout', hideOnOutsideClick: true
		}">
			<i class="pi pi-ellipsis-v"></i>
		</button>
		<ul class="layout-topbar-menu hidden lg:flex origin-top">
			<li>
				<button class="p-link layout-topbar-button">
					<i class="pi pi-bell"></i>
					<span>Notifications</span>
				</button>
			</li>
			<li>
				<button class="p-link layout-topbar-button">
					<i class="pi pi-cog"></i>
					<span>Settings</span>
				</button>
			</li>
			<li>
				<button class="p-link layout-topbar-button" @click="logout">
					<i class="pi pi-power-off"></i>
					<span>Logout</span>
				</button>
			</li>
		</ul>
	</div>
</template>