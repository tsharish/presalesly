import ApiService from './ApiService'

class OppScoreService extends ApiService {
    constructor() {
        super('opp_score')
    }

    train(params: any, data: any) {
        return this.api.post(this.getUrl() + 'train', data, { params: { ...params } })
    }

    search(params: any, data: any) {
        return this.api.post(this.getUrl() + 'search', data, { params: { ...params } })
    }
}

export default new OppScoreService()