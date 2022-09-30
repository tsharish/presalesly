import type { OppTemplate } from '@/types/OppTemplate'
import CrudApiService from "./CrudApiService"

class OppTemplateService extends CrudApiService {
    constructor() {
        super('opp_templates')
    }

    deleteAll(oppTemplates: OppTemplate[]) {
        return Promise.all(
            oppTemplates.map((oppTemplate) => {
                if (oppTemplate.id !== undefined) {
                    return this.delete(oppTemplate.id)
                }
            })
        )
    }
}

export default new OppTemplateService()