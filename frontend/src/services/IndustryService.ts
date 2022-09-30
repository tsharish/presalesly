import type { Industry } from "@/types/Industry"
import CrudApiService from "./CrudApiService"

class IndustryService extends CrudApiService {
    constructor() {
        super('industries')
    }

    deleteAll(industries: Industry[]) {
        return Promise.all(
            industries.map((industry) => {
                if (industry.id !== undefined) {
                    return this.delete(industry.id)
                }
            })
        )
    }
}

export default new IndustryService()