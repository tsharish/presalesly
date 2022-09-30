import CrudApiService from './CrudApiService'
import type { Question } from '@/types/Answer'

class AnswerService extends CrudApiService {
    constructor() {
        super('answers')
    }

    recommend(data: Question) {
        return this.api.post(this.getUrl() + 'recommend', data)
    }
}

export default new AnswerService()