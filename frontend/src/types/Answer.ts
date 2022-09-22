export interface Answer {
    id?: number,
    language_code: string,
    question: string,
    answer: string,
    owner_id: number,
    is_active: boolean
}

export interface Question {
    query: string,
    language_code?: string
}

export interface AnswerRecommendation {
    answer: Answer,
    score: number
}