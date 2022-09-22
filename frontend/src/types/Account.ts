import type { IndustrySummary } from "./Industry"

export interface Account {
    id?: number,
    external_id?: string,
    source_url?: string,
    name: string,
    annual_revenue?: number,
    annual_revenue_curr_code?: string,
    number_of_employees?: number,
    country_code: string,
    street?: string,
    address_line_2?: string,
    address_line_3?: string,
    city?: string,
    state?: string,
    postal_code?: string,
    fax?: string,
    email?: string,
    phone?: string,
    website?: string,
    industry?: IndustrySummary,
    industry_id?: number
}

export interface AccountSummary {
    id: number,
    name: string
}