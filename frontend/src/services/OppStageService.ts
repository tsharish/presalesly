import type { OppStage } from "@/types/OppStage"
import CrudApiService from "./CrudApiService"

class OppStageService extends CrudApiService {
    constructor() {
        super('opp_stages')
    }

    deleteAll(oppStages: OppStage[]) {
        return Promise.all(
            oppStages.map((oppStage) => {
                if (oppStage.id !== undefined) {
                    return this.delete(oppStage.id)
                }
            })
        )
    }
}

export default new OppStageService()