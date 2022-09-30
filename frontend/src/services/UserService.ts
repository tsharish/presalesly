import CrudApiService from "./CrudApiService"

class UserService extends CrudApiService {
    constructor() {
        super('users')
    }
}

export default new UserService()