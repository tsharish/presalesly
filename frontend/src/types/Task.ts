export interface Task {
    id?: number,
    description: string,
    due_date: string,
    owner_id: number,
    priority: string,
    completed_on?: Date,
    status: string,
    parent_type_id: string,
    parent_id: number
}