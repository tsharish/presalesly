import type { UserSummary } from "./User"
import type { OpportunitySummary } from "./Opportunity"

export interface Task {
    id?: number,
    description: string,
    due_date: string,
    owner_id: number,
    priority: string,
    completed_on?: Date,
    status: string,
    opportunity_id: number,
    owner: UserSummary | undefined,
    opportunity?: OpportunitySummary
}