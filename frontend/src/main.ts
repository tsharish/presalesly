import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import router from '@/router'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import StyleClass from 'primevue/styleclass'
import Ripple from 'primevue/ripple'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import InputNumber from 'primevue/inputnumber'
import Calendar from 'primevue/calendar'
import Dropdown from 'primevue/dropdown'
import Toolbar from 'primevue/toolbar'
import Toast from 'primevue/toast'
import Card from 'primevue/card'
import MultiSelect from 'primevue/multiselect'
import FileUpload from 'primevue/fileupload'
import Knob from 'primevue/knob'
import Tag from 'primevue/tag'
import TabMenu from 'primevue/tabmenu'
import Checkbox from 'primevue/checkbox'
import Textarea from 'primevue/textarea'
import Panel from 'primevue/panel'
import AutoComplete from 'primevue/autocomplete'
import Chart from 'primevue/chart'

import 'primevue/resources/themes/tailwind-light/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'
import 'primeflex/primeflex.css'
import '@/assets/styles/layout.scss'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue)
app.use(ToastService)

app.directive('styleclass', StyleClass)
app.directive('ripple', Ripple)

app.component('Button', Button)
app.component('InputText', InputText)
app.component('Message', Message)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Dialog', Dialog)
app.component('InputNumber', InputNumber)
app.component('Calendar', Calendar)
app.component('Dropdown', Dropdown)
app.component('Toolbar', Toolbar)
app.component('Toast', Toast)
app.component('Card', Card)
app.component('MultiSelect', MultiSelect)
app.component('FileUpload', FileUpload)
app.component('Knob', Knob)
app.component('Tag', Tag)
app.component('TabMenu', TabMenu)
app.component('Checkbox', Checkbox)
app.component('Textarea', Textarea)
app.component('Panel', Panel)
app.component('AutoComplete', AutoComplete)
app.component('Chart', Chart)

app.mount('#app')
