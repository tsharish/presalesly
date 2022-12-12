<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
    title: {
        type: String,
        required: true
    },
    subtitle: {
        type: String,
        required: false
    },
    value: {
        type: String,
        required: true
    },
    icon: {
        type: String,
        default: "chart-line"
    },
    color: {
        type: String,
        default: "blue"
    },
    to: {
        type: Object,
        required: true
    }
})

const bgColor = computed(() => "bg-" + props.color + "-100")
const iconClass = computed(() => "pi pi-" + props.icon + " text-" + props.color + "-500")
</script>

<template>
    <div class="col-12 md:col-6 lg:col-3">
        <router-link :to="to">
            <div class="p-card shadow-2 p-3 mx-2">
                <div class="flex flex-column">
                    <div>
                        <span class="block text-600 font-medium">{{ title }}</span>
                        <span class="block text-400 text-sm">{{ subtitle !== undefined ? subtitle : "&nbsp;" }}</span>
                    </div>
                    <div class="flex align-items-center justify-content-between mt-2">
                        <div class="text-gray-600 font-medium text-4xl">{{ value }}</div>
                        <div class="flex align-items-center justify-content-center border-round" :class="bgColor"
                            style="width:2.5rem;height:2.5rem">
                            <i :class="iconClass" class="pi text-xl"></i>
                        </div>
                    </div>
                </div>
            </div>
        </router-link>
    </div>
</template>