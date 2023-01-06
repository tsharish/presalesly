import CrudApiService from './CrudApiService'

class TaskService extends CrudApiService {
    constructor() {
        super('tasks')
    }

    getDashboard() {
        return this.api.get(this.getUrl() + 'dashboard/data')
    }
}

export default new TaskService()