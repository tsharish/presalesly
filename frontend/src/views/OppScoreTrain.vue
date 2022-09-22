<script setup lang="ts">
import { ref } from 'vue'
import OppScoreService from '@/services/OppScoreService'

const algorithm = ref('lightgbm')
const algorithms = ref([
    { code: 'lightgbm', name: 'LightGBM' },
    { code: 'catboost', name: 'Catboost' }
])
const n_estimators = ref(200)
const learning_rate = ref(0.01)
const max_depth = ref(7)
const reg_lambda = ref(1)
const num_leaves = ref(10)
const min_data_in_leaf = ref(10)
const setAsDefault = ref(false)
const loading = ref(false)
const results = ref({
    accuracy: 0,
    f1: 0,
    precision: 0,
    recall: 0
})

async function train() {
    loading.value = true
    try {
        const response = await OppScoreService.train(
            {
                algorithm: algorithm.value,
                set_as_default: setAsDefault.value
            },
            {
                n_estimators: n_estimators.value,
                learning_rate: learning_rate.value,
                max_depth: max_depth.value,
                reg_lambda: reg_lambda.value,
                num_leaves: num_leaves.value,
                min_data_in_leaf: min_data_in_leaf.value
            }
        )
        results.value = response.data
    } catch (error: any) {
        console.log(error)
    }
    loading.value = false
}
</script>

<template>
    <div class="card">
        <h4>Train Opportunity Score Model</h4>
        <div class="field grid">
            <label for="algorithm" class="col-fixed">Select ML Algorithm</label>
            <div class="col">
                <Dropdown v-model="algorithm" :options="algorithms" optionLabel="name" optionValue="code"
                    placeholder="Select an Algorithm" />
            </div>
        </div>
        <h5>Hyper-Parameters</h5>
        <div class="formgrid grid">
            <div class="field col-12 md:col-4">
                <label for="n_estimators">n_estimators</label>
                <InputNumber v-model="n_estimators" class="w-full pr-5" id="n_estimators"></InputNumber>
            </div>
            <div class="field col-12 md:col-4">
                <label for="learning_rate">learning_rate</label>
                <InputNumber v-model="learning_rate" :maxFractionDigits="10" class="w-full pr-5" id="learning_rate">
                </InputNumber>
            </div>
            <div class="field col-12 md:col-4">
                <label for="max_depth">max_depth</label>
                <InputNumber v-model="max_depth" class="w-full pr-5" id="max_depth"></InputNumber>
            </div>
            <div class="field col-12 md:col-4">
                <label for="reg_lambda">reg_lambda</label>
                <InputNumber v-model="reg_lambda" class="w-full pr-5" id="reg_lambda"></InputNumber>
            </div>
            <div class="field col-12 md:col-4">
                <label for="num_leaves">num_leaves</label>
                <InputNumber v-model="num_leaves" class="w-full pr-5" id="num_leaves"></InputNumber>
            </div>
            <div class="field col-12 md:col-4">
                <label for="min_data_in_leaf">min_data_in_leaf</label>
                <InputNumber v-model="min_data_in_leaf" class="w-full pr-5" id="min_data_in_leaf"></InputNumber>
            </div>
        </div>
        <div class="mt-3">
            <div class="field-checkbox">
                <Checkbox inputId="setAsDefault" v-model="setAsDefault" :binary="true" />
                <label for="setAsDefault">Set as default model</label>
            </div>
            <Button label="Submit" :loading="loading" @click="train" />
        </div>
    </div>

    <div class="card">
        <h5>Results</h5>
        <div class="formgroup-inline">
            <div class="field">
                <label for="accuracy">Accuracy</label>
                <InputNumber v-model="results.accuracy" readonly></InputNumber>
            </div>
            <div class="field">
                <label for="f1">F1</label>
                <InputNumber v-model="results.f1" readonly></InputNumber>
            </div>
            <div class="field">
                <label for="precision">Precision</label>
                <InputNumber v-model="results.precision" readonly></InputNumber>
            </div>
            <div class="field">
                <label for="recall">Recall</label>
                <InputNumber v-model="results.recall" readonly></InputNumber>
            </div>
        </div>
    </div>
</template>