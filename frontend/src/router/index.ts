import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Layout from '@/layouts/Layout.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/login',
            name: 'login',
            component: Login,
            meta: { guest: true }
        },
        {
            path: '/',
            component: Layout,
            meta: { requiresAuth: true },
            children: [
                {
                    path: '',
                    component: () => import('@/views/Home.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'home',
                    name: 'home',
                    component: () => import('@/views/Home.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'tasks',
                    name: 'tasks',
                    component: () => import('@/views/TaskList.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'accounts',
                    name: 'accounts',
                    component: () => import('@/views/AccountList.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'opportunities',
                    name: 'opportunities',
                    component: () => import('@/views/OpportunityList.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'pipeline',
                    name: 'pipeline',
                    component: () => import('@/views/Pipeline.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'opportunity/:id/',
                    name: 'opportunity',
                    component: () => import('@/views/Opportunity.vue'),
                    meta: { requiresAuth: true },
                    children: [
                        {
                            path: 'tasks',
                            component: () => import('@/components/OpportunityTasks.vue')
                        }
                    ]
                },
                {
                    path: 'answers',
                    name: 'answers',
                    component: () => import('@/views/AnswerLibrary.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'answer/add',
                    name: 'answerAdd',
                    component: () => import('@/views/AnswerNewEditForm.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'answer/:id',
                    name: 'answerEdit',
                    component: () => import('@/views/AnswerNewEditForm.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'answer/recommend',
                    name: 'answerRecommend',
                    component: () => import('@/views/AnswerRecommendation.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'admin/settings',
                    name: 'settings',
                    component: () => import('@/views/Settings.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'admin/users',
                    name: 'users',
                    component: () => import('@/views/UserList.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'admin/oppstages',
                    name: 'oppStages',
                    component: () => import('@/views/OppStageList.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'admin/industries',
                    name: 'industries',
                    component: () => import('@/views/IndustryList.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'admin/dataimport',
                    name: 'dataImport',
                    component: () => import('@/views/DataImport.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'admin/opptemplates',
                    name: 'oppTemplates',
                    component: () => import('@/views/OppTemplateList.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'admin/oppscoretrain',
                    name: 'oppScoreTrain',
                    component: () => import('@/views/OppScoreTrain.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'admin/oppscoresearch',
                    name: 'oppScoreSearch',
                    component: () => import('@/views/OppScoreSearch.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'admin/opptemplate/:id/',
                    name: 'oppTemplate',
                    component: () => import('@/views/OppTemplateEditForm.vue'),
                    meta: { requiresAuth: true },
                    children: [
                        {
                            path: 'tasks',
                            component: () => import('@/components/OppTemplateTasks.vue')
                        }
                    ]
                }
            ]
        }
    ]
})

router.beforeEach((to, from, next) => {
    const auth = useAuthStore()

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (auth.authenticated) {
            next()
            return
        }
        next('/login')
    } else {
        next()
    }
})

export default router
