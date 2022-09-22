import CrudApiService from './CrudApiService'

class AccountService extends CrudApiService {
    constructor() {
        super('account')
    }

    upload(data: any) {
        return this.api.post(this.getUrl() + 'upload', data)
    }
}

export default new AccountService()