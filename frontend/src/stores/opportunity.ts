import { defineStore } from "pinia"
import OpportunityService from "@/services/OpportunityService"
import type { OpportunityDetails } from "@/types/Opportunity"

export const useOpportunityStore = defineStore('opportunity', {
    state: () => ({
        opportunity: {} as OpportunityDetails
    }),
    getters: {},
    actions: {
        async getOpportunityDetails(opportunityId: number) {
            const response = await OpportunityService.get(opportunityId)
            this.opportunity = response.data
        }
    }
})