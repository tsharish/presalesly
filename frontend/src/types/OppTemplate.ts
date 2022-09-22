import type { OppTemplateTask } from "./OppTemplateTask"

export interface OppTemplate {
    id?: number,
    description: string,
    opp_template_tasks: OppTemplateTask[]
}