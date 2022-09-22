import type { Description } from "./Common"

export interface Industry {
    id?: number,
    external_id?: string,
    descriptions: Description[],
    description?: string
}

export interface IndustrySummary {
    id: number,
    description?: string
}