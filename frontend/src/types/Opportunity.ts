import type { AccountSummary } from "./Account"
import type { OppStageSummary } from "./OppStage"
import type { UserSummary } from "./User"

// To use for creating and editing an opportunity
export interface Opportunity {
    id?: number,
    external_id?: string,
    name: string,
    expected_amount: number,
    expected_amount_curr_code: string,
    start_date: string | Date,
    close_date: string | Date,
    probability: number,
    probability_percent?: number,
    owner_id: number,
    account_id: number,
    stage_id: number,
    opp_template_id?: number,
    owner: UserSummary | undefined,
    account: AccountSummary | undefined
}

// To use for reading opportunity details
export interface OpportunityDetails {
    id: number,
    external_id?: string,
    name: string,
    expected_amount: number,
    expected_amount_curr_code: string,
    start_date: string | Date,
    close_date: string | Date,
    probability: number,
    probability_percent?: number,
    owner_id: number,
    account_id: number,
    stage_id: number,
    owner: UserSummary,
    account: AccountSummary,
    stage: OppStageSummary,
    opp_template_id?: number,
    status: string,
    ai_score: number,
    weighted_amount: number,
    age: number,
    days_remaining: number,
    close_month: number,
    close_quarter: number,
    close_year: number,
    not_started_task_count: number,
    in_progress_task_count: number,
    completed_task_count: number
}