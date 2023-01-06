import CrudApiService from './CrudApiService'

export default class OppTasksService extends CrudApiService {
    constructor(opportunityId: number) {
        super('tasks/opportunity/' + opportunityId)
    }
}