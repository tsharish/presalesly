import CrudApiService from "./CrudApiService"

class OppTemplateTaskService extends CrudApiService {
    constructor() {
        super('opp_template_task')
    }

    getByOppTemplate(id: number) {
        return this.api.get(this.getUrl() + 'opp_template/' + id.toString())
    }
}

export default new OppTemplateTaskService()