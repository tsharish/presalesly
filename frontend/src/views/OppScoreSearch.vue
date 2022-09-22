<script setup lang="ts">
import { ref } from 'vue'
import OppScoreService from '@/services/OppScoreService'

const algorithm = ref('lightgbm')
const algorithms = ref([
    { code: 'lightgbm', name: 'LightGBM' },
    { code: 'catboost', name: 'Catboost' }
])
const scoring = ref('f1')
const scoringOptions = ref([
    { code: 'accuracy', name: 'Accuracy' },
    { code: 'f1', name: 'F1' },
    { code: 'precision', name: 'Precision' },
    { code: 'recall', name: 'Recall' }
])
const n_iterations = ref(50)
const n_estimators_lower = ref(200)
const n_estimators_upper = ref(1000)
const learning_rate_lower = ref(0.01)
const learning_rate_upper = ref(0.3)
const max_depth_lower = ref(2)
const max_depth_upper = ref(7)
const reg_lambda_lower = ref(1)
const reg_lambda_upper = ref(10)
const num_leaves_lower = ref(10)
const num_leaves_upper = ref(1000)
const min_data_in_leaf_lower = ref(10)
const min_data_in_leaf_upper = ref(200)
const setBestAsDefault = ref(false)
const loading = ref(false)
const results = ref({
    best_score: 0,
    best_params: {
        n_estimators: 0,
        learning_rate: 0,
        max_depth: 0,
        reg_lambda: 0,
        num_leaves: 0,
        min_data_in_leaf: 0
    }
})

async function search() {
    loading.value = true
    try {
        const response = await OppScoreService.search(
            {
                algorithm: algorithm.value,
                scoring: scoring.value,
                n_iterations: n_iterations.value,
                set_best_as_default: setBestAsDefault.value
            },
            {
                n_estimators_lower: n_estimators_lower.value,
                n_estimators_upper: n_estimators_upper.value,
                learning_rate_lower: learning_rate_lower.value,
                learning_rate_upper: learning_rate_upper.value,
                max_depth_lower: max_depth_lower.value,
                max_depth_upper: max_depth_upper.value,
                reg_lambda_lower: reg_lambda_lower.value,
                reg_lambda_upper: reg_lambda_upper.value,
                num_leaves_lower: num_leaves_lower.value,
                num_leaves_upper: num_leaves_upper.value,
                min_data_in_leaf_lower: min_data_in_leaf_lower.value,
                min_data_in_leaf_upper: min_data_in_leaf_upper.value
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
        <h4>Search Opportunity Score Model</h4>
        <div class="formgroup-inline">
            <div class="field pr-5">
                <label for="algorithm">ML Algorithm</label>
                <Dropdown v-model="algorithm" :options="algorithms" optionLabel="name" optionValue="code"
                    placeholder="Select an Algorithm" />
            </div>
            <div class="field pr-5">
                <label for="scoring">Scoring</label>
                <Dropdown v-model="scoring" :options="scoringOptions" optionLabel="name" optionValue="code"
                    placeholder="Select a scoring option" />
            </div>
            <div class="field pr-5">
                <label for="n_iterations">Number of Iterations</label>
                <InputNumber v-model="n_iterations" id="n_iterations"></InputNumber>
            </div>
        </div>

        <h5>Hyper-Parameters Range</h5>
        <div class="field grid">
            <label class="col-fixed" style="width:150px">n_estimators</label>
            <InputNumber v-model="n_estimators_lower" id="n_estimators_lower" class="mr-3"></InputNumber>
            <InputNumber v-model="n_estimators_upper" id="n_estimators_upper"></InputNumber>
        </div>
        <div class="field grid">
            <label class="col-fixed" style="width:150px">learning_rate</label>
            <InputNumber v-model="learning_rate_lower" id="learning_rate_lower" class="mr-3"></InputNumber>
            <InputNumber v-model="learning_rate_upper" id="learning_rate_upper"></InputNumber>
        </div>
        <div class="field grid">
            <label class="col-fixed" style="width:150px">max_depth</label>
            <InputNumber v-model="max_depth_lower" id="max_depth_lower" class="mr-3"></InputNumber>
            <InputNumber v-model="max_depth_upper" id="max_depth_upper"></InputNumber>
        </div>
        <div class="field grid">
            <label class="col-fixed" style="width:150px">reg_lambda</label>
            <InputNumber v-model="reg_lambda_lower" id="reg_lambda_lower" class="mr-3"></InputNumber>
            <InputNumber v-model="reg_lambda_upper" id="reg_lambda_upper"></InputNumber>
        </div>
        <div class="field grid">
            <label class="col-fixed" style="width:150px">num_leaves</label>
            <InputNumber v-model="num_leaves_lower" id="num_leaves_lower" class="mr-3"></InputNumber>
            <InputNumber v-model="num_leaves_upper" id="num_leaves_upper"></InputNumber>
        </div>
        <div class="field grid">
            <label class="col-fixed" style="width:150px">min_data_in_leaf</label>
            <InputNumber v-model="min_data_in_leaf_lower" id="min_data_in_leaf_lower" class="mr-3"></InputNumber>
            <InputNumber v-model="min_data_in_leaf_upper" id="min_data_in_leaf_upper"></InputNumber>
        </div>
        <div>
            <div class="field-checkbox pt-3">
                <Checkbox inputId="setBestAsDefault" v-model="setBestAsDefault" :binary="true" />
                <label for="setBestAsDefault">Set best as default model</label>
            </div>
            <Button label="Submit" :loading="loading" @click="search" />
        </div>
    </div>

    <div class="card">
        <h3>Results</h3>
        <div class="formgroup-inline">
            <div class="field">
                <label for="best_score">Best Score</label>
                <InputNumber v-model="results.best_score" readonly></InputNumber>
            </div>
        </div>
        <h5>Best Params</h5>
        <div class="formgroup-inline">
            <div class="field">
                <label for="n_estimators">n_estimators</label>
                <InputNumber v-model="results.best_params.n_estimators" readonly></InputNumber>
            </div>
            <div class="field">
                <label for="learning_rate">learning_rate</label>
                <InputNumber v-model="results.best_params.learning_rate" readonly></InputNumber>
            </div>
            <div class="field">
                <label for="max_depth">max_depth</label>
                <InputNumber v-model="results.best_params.max_depth" readonly></InputNumber>
            </div>
            <div class="field">
                <label for="reg_lambda">reg_lambda</label>
                <InputNumber v-model="results.best_params.reg_lambda" readonly></InputNumber>
            </div>
            <div class="field">
                <label for="num_leaves">num_leaves</label>
                <InputNumber v-model="results.best_params.num_leaves" readonly></InputNumber>
            </div>
            <div class="field">
                <label for="min_data_in_leaf">min_data_in_leaf</label>
                <InputNumber v-model="results.best_params.min_data_in_leaf" readonly></InputNumber>
            </div>
        </div>
    </div>
</template>