import CrudApiService from './CrudApiService'

class TaskService extends CrudApiService {
    constructor() {
        super('tasks')
    }

    getByOpportunity(id: number) {
        return this.api.get(this.getUrl() + 'opportunity/' + id.toString())
    }

    getDashboard() {
        return this.api.get(this.getUrl() + 'dashboard/data')
    }
}

export default new TaskService()