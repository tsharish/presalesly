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

    getUserDashboard() {
        return this.api.get(this.getUrl() + 'dashboard/user')
    }

    getAdminDashboard() {
        return this.api.get(this.getUrl() + 'dashboard/admin')
    }
}

export default new OpportunityService()