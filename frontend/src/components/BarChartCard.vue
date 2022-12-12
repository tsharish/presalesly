<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps({
    title: {
        type: String,
        required: true
    },
    labels: {
        type: Array,
        required: true
    },
    label: {
        type: String,
        required: true
    },
    data: {
        type: Array,
        required: true
    },
    to: {
        type: Object,
        required: true
    }
})

const labels = ref(props.labels)
const chartData = ref(props.data)

watch(() => props.labels, (newVal) => {
    labels.value = newVal
})

watch(() => props.data, (newVal) => {
    chartData.value = newVal
})

const data = ref({
    labels: labels,
    datasets: [
        {
            label: props.label,
            data: chartData,
            backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 159, 64, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(153, 102, 255, 0.5)',
                'rgba(255, 205, 86, 0.5)',
                'rgba(201, 203, 207, 0.5)'
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
                'rgb(255, 205, 86)',
                'rgb(201, 203, 207)'
            ],
            borderWidth: 1
        }
    ]
})

const options = ref({
    maintainAspectRatio: false
})
</script>

<template>
    <div class="col-12 md:col-6">
        <div class="p-card shadow-2 pb-3 mx-2">
            <router-link :to="to">
                <span class="block text-600 font-medium pt-3 px-3 pb-2 chart-link">{{ title }}</span>
            </router-link>
            <Chart type="bar" :data="data" :options="options" :height="200" class="px-3" />
        </div>
    </div>
</template>

<style lang="scss" scoped>
.chart-link:hover {
    background-color: var(--surface-ground);
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}
</style>