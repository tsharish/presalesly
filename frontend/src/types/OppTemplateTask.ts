export interface OppTemplateTask {
    id?: number,
    opp_template_id: number,
    description: string,
    due_date_offset: number,
    priority: string,
    is_required: boolean
}