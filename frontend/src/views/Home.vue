<script setup lang="ts">
import { ref, computed, onMounted, type Ref } from 'vue'
import KPI from '@/components/KPICard.vue'
import BarChart from '@/components/BarChartCard.vue'
import { useAuthStore } from '@/stores/auth'
import TaskService from '@/services/TaskService'
import OpportunityService from '@/services/OpportunityService'

const auth = useAuthStore()
const isAdmin = computed(() => {
    return auth.user?.role_id == "ADMIN" || auth.user?.role_id == "SUPER"
})
const tasksDueToday = ref(0)
const tasksDue7Days = ref(0)
const overdueTasks = ref(0)
const completedTasks7Days = ref(0)
const myOpenOpps = ref(0)
const myOppsWonThisMonth = ref(0)
const myOppsWonThisQuarter = ref(0)
const myAvgTimeToClose = ref(0)
const allOpenOpps = ref(0)
const allOppsWonThisMonth = ref(0)
const allOppsWonThisQuarter = ref(0)
const allAvgTimeToClose = ref(0)
const pipelineLabels = ref([])
const pipelineData = ref([])

onMounted(async () => {
    try {
        const response = await TaskService.getDashboard()
        tasksDueToday.value = response.data.due_today
        tasksDue7Days.value = response.data.due_in_7_days
        overdueTasks.value = response.data.overdue
        completedTasks7Days.value = response.data.completed_last_7_days
    } catch (error: any) {
        console.log(error)
    }

    try {
        const response = await OpportunityService.getUserDashboard()
        myOpenOpps.value = response.data.open_opportunities
        myOppsWonThisMonth.value = response.data.won_opp_current_month
        myOppsWonThisQuarter.value = response.data.won_opp_current_quarter
        const _myAvgTimeToClose = response.data.average_time_to_close
        myAvgTimeToClose.value = Math.round(_myAvgTimeToClose * 100) / 100
    } catch (error: any) {
        console.log(error)
    }

    if (isAdmin.value) {
        try {
            const response = await OpportunityService.getAdminDashboard()
            allOpenOpps.value = response.data.open_opportunities
            allOppsWonThisMonth.value = response.data.won_opp_current_month
            allOppsWonThisQuarter.value = response.data.won_opp_current_quarter
            const _allAvgTimeToClose = response.data.average_time_to_close
            allAvgTimeToClose.value = Math.round(_allAvgTimeToClose * 100) / 100
            pipelineLabels.value = response.data.pipeline.stages
            pipelineData.value = response.data.pipeline.expected_amount
        } catch (error: any) {
            console.log(error)
        }
    }
})
</script>

<template>
    <div class="surface-ground px-3 pb-2 pt-2">
        <h5 class="text-gray-700">My Tasks</h5>
        <div class="grid">
            <KPI title="Tasks Due" subtitle="Today" :value="tasksDueToday.toString()" icon="bell"
                :to="{ name: 'tasks' }">
            </KPI>
            <KPI title="Tasks Due" subtitle="Next 7 days" :value="tasksDue7Days.toString()" icon="bell"
                :to="{ name: 'tasks' }">
            </KPI>
            <KPI title="Overdue Tasks" :value="overdueTasks.toString()" icon="exclamation-triangle" color="red"
                :to="{ name: 'tasks' }"></KPI>
            <KPI title="Completed Tasks" subtitle="Last 7 days" :value="completedTasks7Days.toString()"
                icon="check-square" color="green" :to="{ name: 'tasks' }">
            </KPI>
        </div>
    </div>
    <div class="surface-ground px-3 pb-2 pt-2">
        <h5 class="text-gray-700">My Opportunities</h5>
        <div class="grid">
            <KPI title="Open Opportunities" :value="myOpenOpps.toString()" icon="dollar" color="orange"
                :to="{ name: 'pipeline' }">
            </KPI>
            <KPI title="Opportunities Won" subtitle="This Month" :value="myOppsWonThisMonth.toString()" icon="dollar"
                color="green" :to="{ name: 'opportunities' }">
            </KPI>
            <KPI title="Opportunities Won" subtitle="This Quarter" :value="myOppsWonThisQuarter.toString()"
                icon="dollar" color="green" :to="{ name: 'opportunities' }">
            </KPI>
            <KPI title="Average Time To Close" :value="myAvgTimeToClose.toString()" icon="dollar" color="purple"
                :to="{ name: 'opportunities' }">
            </KPI>
        </div>
    </div>
    <div class="surface-ground px-3 pt-2" v-if="isAdmin">
        <h5 class="text-gray-700">All Opportunities</h5>
        <div class="grid">
            <KPI title="Open Opportunities" :value="allOpenOpps.toString()" icon="dollar" color="orange"
                :to="{ name: 'pipeline' }">
            </KPI>
            <KPI title="Opportunities Won" subtitle="This Month" :value="allOppsWonThisMonth.toString()" icon="dollar"
                color="green" :to="{ name: 'opportunities' }">
            </KPI>
            <KPI title="Opportunities Won" subtitle="This Quarter" :value="allOppsWonThisQuarter.toString()"
                icon="dollar" color="green" :to="{ name: 'opportunities' }">
            </KPI>
            <KPI title="Average Time To Close" :value="allAvgTimeToClose.toString()" icon="dollar" color="purple"
                :to="{ name: 'opportunities' }">
            </KPI>
            <BarChart title="Pipeline" :labels="pipelineLabels" label="Expected Amount" :data="pipelineData"
                :to="{ name: 'pipeline' }">
            </BarChart>
        </div>
    </div>
</template>