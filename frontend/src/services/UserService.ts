import CrudApiService from "./CrudApiService"

class UserService extends CrudApiService {
    constructor() {
        super('user')
    }
}

export default new UserService()