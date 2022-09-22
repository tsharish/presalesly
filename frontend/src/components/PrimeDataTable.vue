<script setup lang="ts">
import { onMounted, ref, toRef, watch, type Ref } from 'vue'
import type { DataTablePageEvent } from 'primevue/datatable'
import CrudApiService from '@/services/CrudApiService'
import { createFilterSpec, createSortSpec } from '@/composables/useUtils'
import { useAuthStore } from '@/stores/auth'
import useDataTable from '@/composables/useDataTable'

const props = defineProps({
    ApiService: {
        type: CrudApiService,
        required: true
    },
    rows: {
        type: Number,
        default: 10
    },
    initialFilters: {
        type: Object,
        required: true
    },
    dataKey: {
        type: String,
        default: "id"
    },
    title: {
        type: String,
        required: true
    },
    refresh: {
        type: String,
        required: true
    },
    showToolbar: {
        type: Boolean,
        default: true
    },
    showNewButton: {
        type: Boolean,
        default: true
    },
    showExportButton: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['click-new'])

const auth = useAuthStore()
const { exportCSV } = useDataTable()
const records: Ref<any[]> = ref([])
const dt = ref()
const loading = ref(false)
const totalRecords = ref(0)
const filters = ref(props.initialFilters)
const lazyParams: Ref<any> = ref({
    page: 1,
    size: 10,
    sort: null,
    filter: createFilterSpec(filters.value),
    lang_code: auth.loginLanguageCode
})

const refresh = toRef(props, "refresh")
watch(refresh, (val) => {
    loadLazyData()
})

onMounted(() => {
    loadLazyData()
})

async function loadLazyData() {
    loading.value = true
    try {
        const response = await props.ApiService.getAll(lazyParams.value)
        records.value = response.data.items
        totalRecords.value = response.data.total
    } catch (error: any) {
        if (error.response.status === 404) {    // No records found
            records.value = []
            totalRecords.value = 0
        }
    }
    loading.value = false
}

function onPage(event: DataTablePageEvent) {
    lazyParams.value.page = event.page + 1
    lazyParams.value.size = event.rows
    loadLazyData()
}

function onSort(event: any) {
    lazyParams.value.sort = createSortSpec(event.multiSortMeta)
    loadLazyData()
}

function onFilter() {
    lazyParams.value.filter = createFilterSpec(filters.value)
    loadLazyData()
}
</script>

<template>
    <Toolbar class="mb-2 py-2" v-if="showToolbar">
        <template #start>
            <Button label="New" icon="pi pi-plus" class="p-button-success mr-2" v-if="showNewButton"
                @click="$emit('click-new', $event)" />
        </template>
        <template #end>
            <Button label="Export" icon="pi pi-external-link" v-if="showExportButton" @click="exportCSV" />
        </template>
    </Toolbar>

    <DataTable class="p-datatable-sm" :value="records" :lazy="true" :paginator="true" :rows="rows"
        v-model:filters="filters" ref="dt" dataKey="dataKey" :totalRecords="totalRecords" :loading="loading"
        @page="onPage($event)" @sort="onSort($event)" @filter="onFilter" filterDisplay="menu"
        paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
        :rowsPerPageOptions="[10, 20, 50]" :alwaysShowPaginator="false" responsiveLayout="scroll"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} records" sortMode="multiple"
        removableSort>
        <template #header>
            <div class="table-header flex flex-column md:flex-row md:justify-content-between">
                <h5 class="mb-2 md:m-0 md:align-self-center">{{ title }}</h5>
                <span class="p-input-icon-left">
                    <Button @click="loadLazyData" class="p-button-text p-button-rounded" icon="pi pi-refresh" />
                </span>
            </div>
        </template>
        <template #empty>
            No records found.
        </template>
        <slot></slot>
    </DataTable>
</template>

<style lang="scss" scoped>
.table-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    @media screen and (max-width: 960px) {
        align-items: start;
    }
}

@media screen and (max-width: 960px) {
    ::v-deep(.p-toolbar) {
        flex-wrap: wrap;

        .p-button {
            margin-bottom: 0.25rem;
        }
    }
}
</style>