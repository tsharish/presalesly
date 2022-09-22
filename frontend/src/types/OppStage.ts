import type { Description } from "./Common"

export interface OppStage {
    id?: number,
    external_id?: string,
    default_probability: number,
    sort_order: number,
    opp_status: string,
    descriptions: Description[],
    description?: string,
    default_probability_percent?: number
}

export interface OppStageSummary {
    id: number,
    description?: string
}