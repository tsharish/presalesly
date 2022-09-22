import { PrimeIcons } from 'primevue/api'

export const navigationMenu = [
    {
        label: 'Home',
        items: [{
            label: 'Dashboard', icon: PrimeIcons.HOME, to: '/home',
        },
        {
            label: 'Tasks', icon: PrimeIcons.CHECK_SQUARE, to: '/tasks',
        }]
    },
    {
        label: 'Accounts',
        items: [{
            label: 'List', icon: PrimeIcons.LIST, to: '/accounts',
        }]
    },
    {
        label: 'Opportunities',
        items: [{
            label: 'Pipeline', icon: PrimeIcons.MONEY_BILL, to: '/pipeline',
        },
        {
            label: 'List', icon: PrimeIcons.LIST, to: '/opportunities',
        }]
    },
    {
        label: 'Answers',
        items: [{
            label: 'Library', icon: PrimeIcons.BOOK, to: '/answers',
        },
        {
            label: 'Recommendation', icon: PrimeIcons.QUESTION_CIRCLE, to: '/answer/recommend',
        }]
    },
    {
        label: 'Admin',
        items: [{
            label: 'Settings', icon: PrimeIcons.COG, to: '/admin/settings',
        },
        {
            label: 'Users', icon: PrimeIcons.USERS, to: '/admin/users',
        }]
    },
]