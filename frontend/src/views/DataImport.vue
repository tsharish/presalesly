<script setup lang="ts">
import { useToast } from 'primevue/usetoast'
import AccountService from '@/services/AccountService'
import OpportunityService from '@/services/OpportunityService'

const toast = useToast()

async function uploadData(event: any, object: string) {
    let formData = new FormData()
    formData.append('upload_file', event.files[0])
    try {
        switch (object) {
            case 'account':
                await AccountService.upload(formData)
                break
            case 'opportunity':
                await OpportunityService.upload(formData)
                break
        }
        toast.add({ severity: 'info', summary: 'Success', detail: 'File uploaded successfully', life: 3000 })
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'File upload failed. Please validate the data and structure of the file.', life: 3000 })
    }
}
</script>

<template>
    <div class="grid">
        <div class="col-12 lg:col-6">
            <Card>
                <template #title>
                    Import Accounts
                </template>
                <template #content>
                    <FileUpload name="accounts[]" :customUpload="true" @uploader="uploadData($event, 'account')"
                        accept=".csv">
                        <template #empty>
                            <p>Drag and drop file here to upload accounts.</p>
                        </template>
                    </FileUpload>
                </template>
            </Card>
        </div>
        <div class="col-12 lg:col-6">
            <Card>
                <template #title>
                    Import Opportunities
                </template>
                <template #content>
                    <FileUpload name="opportunities[]" :customUpload="true"
                        @uploader="uploadData($event, 'opportunity')" accept=".csv">
                        <template #empty>
                            <p>Drag and drop file here to upload opportunities.</p>
                        </template>
                    </FileUpload>
                </template>
            </Card>
        </div>
    </div>
</template>