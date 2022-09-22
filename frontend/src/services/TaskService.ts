import CrudApiService from './CrudApiService'

class TaskService extends CrudApiService {
    constructor() {
        super('task')
    }

    getByOpportunity(id: number) {
        return this.api.get(this.getUrl() + 'opportunity/' + id.toString())
    }
}

export default new TaskService()