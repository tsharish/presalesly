import { PrimeIcons } from 'primevue/api'

const adminMenu = [
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

const superMenu = [
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
    }
]

const profMenu = [
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
    }
]

const standardMenu = [
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
        label: 'Opportunities',
        items: [{
            label: 'Pipeline', icon: PrimeIcons.MONEY_BILL, to: '/pipeline',
        },
        {
            label: 'List', icon: PrimeIcons.LIST, to: '/opportunities',
        }]
    }
]

export function getMenu(roleId: string) {
    switch (roleId) {
        case 'ADMIN':
            return adminMenu
            break
        case 'SUPER':
            return superMenu
            break
        case 'PROF':
            return profMenu
            break
        case 'STANDARD':
            return standardMenu
            break
        default:
            return standardMenu
    }
}