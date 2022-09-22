import CrudApiService from './CrudApiService'
import type { Question } from '@/types/Answer'

class AnswerService extends CrudApiService {
    constructor() {
        super('answer')
    }

    recommend(data: Question) {
        return this.api.post(this.getUrl() + 'recommend', data)
    }
}

export default new AnswerService()