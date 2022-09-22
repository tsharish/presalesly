<script setup lang="ts">
</script>

<template>
    <div class="grid">
        <div class="col-12 lg:col-6">
            <Card>
                <template #title>
                    Opportunity Stage
                </template>
                <template #content>
                    Represents the stages of an opportunity in the sales pipeline, such as Qualification.
                    If the CRM integration is enabled, this is updated automatically.
                </template>
                <template #footer>
                    <router-link :to="{ name: 'oppStages' }">Manage Opportunity Stages</router-link>
                </template>
            </Card>
        </div>
        <div class="col-12 lg:col-6">
            <Card>
                <template #title>
                    Industry
                </template>
                <template #content>
                    Represents the segment that a customer belongs to, such as Information Technology.
                    If the CRM integration is enabled, this is updated automatically.
                </template>
                <template #footer>
                    <router-link :to="{ name: 'industries' }">Manage Industries</router-link>
                </template>
            </Card>
        </div>
        <div class="col-12 lg:col-6">
            <Card>
                <template #title>
                    Data Import
                </template>
                <template #content>
                    The Data Import tool can be used to bulk import data.
                    Data must be uploaded in CSV (comma-separated values) format using the standard import templates.
                </template>
                <template #footer>
                    <router-link :to="{ name: 'dataImport' }">Import Data</router-link>
                </template>
            </Card>
        </div>
        <div class="col-12 lg:col-6">
            <Card>
                <template #title>
                    Opportunity Template
                </template>
                <template #content>
                    Opportunity Templates can be used to create a repeatable presales process to manage and execute
                    opportunities.
                </template>
                <template #footer>
                    <router-link :to="{ name: 'oppTemplates' }">Manage Opportunity Templates</router-link>
                </template>
            </Card>
        </div>
        <div class="col-12 lg:col-6">
            <Card>
                <template #title>
                    ML Workbench
                </template>
                <template #content>
                    The ML Workbench can be used to experiment with and create Machine Learning models for Opportunity
                    Scoring.
                </template>
                <template #footer>
                    <router-link :to="{ name: 'oppScoreTrain' }">Train Model</router-link> &nbsp;|&nbsp;
                    <router-link :to="{ name: 'oppScoreSearch' }">Search Model</router-link>
                </template>
            </Card>
        </div>
    </div>
</template>