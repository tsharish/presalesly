import { ref } from 'vue'

export default () => {
    const newEditDialog = ref(false)
    const deleteDialog = ref(false)
    const refreshTime = ref(new Date().toUTCString())

    function refresh() {
        refreshTime.value = new Date().toUTCString()
    }

    function openNewEditDialog(reset: Function) {
        reset()
        newEditDialog.value = true
    }

    function hideNewEditDialog(reset: Function) {
        newEditDialog.value = false
        reset()
    }

    function hideDeleteDialog(reset: Function) {
        deleteDialog.value = false
        reset()
    }

    function exportCSV() {
        // dataTableRef.value.exportCSV()
    }

    return {
        newEditDialog, deleteDialog, refreshTime,
        refresh, openNewEditDialog, hideNewEditDialog, hideDeleteDialog, exportCSV
    }
}