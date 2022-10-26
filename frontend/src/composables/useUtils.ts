import type { Description } from '@/types/Common'

const fieldMap = new Map([
    ['industry.id', 'industry_id']
])

export function getDescription(descriptions: Description[], languageCode: string) {
    //Takes an array of descriptions and returns the description based on the language code passed
    return descriptions.find(description => description.language_code === languageCode)?.description
}

export function getDescriptionIndex(descriptions: Description[], languageCode: string) {
    //Takes an array of descriptions and returns the index of the description that matches the language code passed
    return descriptions.findIndex(description => description.language_code === languageCode)
}

export function capitalize(s: string) {
    //Capitalizes the first letter of a string
    if (typeof s !== 'string') {
        return ''
    }
    return s.charAt(0).toUpperCase() + s.slice(1)
}

export function formatCurrency(amount: number, currencyCode: string) {
    //Returns formatted currency
    if (amount) {
        return amount.toLocaleString(undefined, { style: 'currency', currency: currencyCode })
    }
    return
}

export function calculateDateWithOffset(date: string | Date) {
    //Returns date adjusted for time zone. Date string must be in the YYYY-MM-DD fomat.
    //Refer to https://www.ursahealth.com/new-insights/dates-and-timezones-in-javascript for the code below for dates
    const offset = new Date().getTimezoneOffset() * 60 * 1000
    if (date instanceof Date) {
        const dateString = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()
        return new Date(new Date(dateString).getTime() + offset)
    } else {
        if (date !== '') {
            return new Date(new Date(date).getTime() + offset)
        } else {
            return new Date()
        }
    }
}

export function formatDate(date: Date) {
    //Returns formatted date
    return date.toLocaleDateString(undefined, {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
    })
}

export async function copyToClipboard(text: string) {
    //Copies the text to the user's clipboard
    await navigator.clipboard.writeText(text)
}

function createFilter(key: string, constraint: { matchMode: any; value: any }) {
    let filter: any = {}

    // Replace the key if it exists in the field mapping
    const _key = fieldMap.get(key)
    if (_key !== undefined) {
        key = _key
    }

    // If key is a compound word, split it into model and field
    if (key.indexOf('.') === -1) {
        filter.field = key
    } else {
        filter.model = key.split('.')[0]
        filter.field = key.split('.')[1]
    }

    filter.operator = constraint.matchMode
    filter.value = constraint.value

    return filter
}

export function createFilterSpec(filters: any) {
    /*
    Takes the PrimeVue filters object and returns a list of filters
    that conforms to the backend specification.
    */
    const filterSpec: any[] = []

    Object.keys(filters).forEach((key, index) => {
        if (filters[key].hasOwnProperty('value')) {
            if (filters[key].value !== null) {
                filterSpec.push(createFilter(key, filters[key]))
            }
        } else {
            if (filters[key].operator === 'and') {
                filters[key].constraints.forEach((constraint: { matchMode: any; value: any }) => {
                    if (constraint.value !== null) {
                        filterSpec.push(createFilter(key, constraint))
                    }
                })
            } else if (filters[key].operator === 'or') {
                const orConstraints: { field: string; operator: any; value: any }[] = []
                filters[key].constraints.forEach((constraint: { matchMode: any; value: any }) => {
                    if (constraint.value !== null) {
                        orConstraints.push(createFilter(key, constraint))
                    }
                })
                filterSpec.push({
                    or: orConstraints
                })
            }
        }
    })

    return JSON.stringify(filterSpec)
}

export function createSortSpec(sorts: { field: string; order: number }[]) {
    /*
    Takes the PrimeVue sort object and returns a list of sorts
    that conforms to the backend specification.
    */
    const sortSpec: any[] = []

    for (const sort of sorts) {
        // Replace the field if it exists in the field mapping
        const _key = fieldMap.get(sort.field)
        if (_key !== undefined) {
            sort.field = _key
        }

        if (sort.field.indexOf('.') === -1) {
            sortSpec.push({
                field: sort.field,
                order: sort.order
            })
        } else {
            sortSpec.push({
                model: sort.field.split('.')[0],
                field: sort.field.split('.')[1],
                order: sort.order
            })
        }
    }

    return JSON.stringify(sortSpec)
}