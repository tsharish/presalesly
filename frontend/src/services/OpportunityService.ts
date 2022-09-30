import CrudApiService from './CrudApiService'

class OpportunityService extends CrudApiService {
    constructor() {
        super('opportunities')
    }

    getOpen(options: any) {
        return this.api.get(this.getUrl() + 'open', {
            params: { ...options },
        })
    }

    upload(data: any) {
        return this.api.post(this.getUrl() + 'upload', data)
    }
}

export default new OpportunityService()