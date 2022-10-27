export interface User {
    id?: number,
    email: string,
    first_name?: string,
    last_name?: string,
    full_name?: string,
    employee_id?: string,
    language_code?: string,
    role_id: string,
    password?: string
}

export interface UserSummary {
    id: number,
    email: string,
    first_name?: string,
    last_name?: string,
    full_name?: string,
    employee_id?: string
}

export interface UserDetail {
    id: number,
    email: string,
    first_name?: string,
    last_name?: string,
    full_name?: string,
    employee_id?: string,
    role_id: string,
    language_code: string
}