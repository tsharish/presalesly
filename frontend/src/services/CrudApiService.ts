import ApiService from './ApiService'

export default class CrudApiService extends ApiService {

    getAll(options: any) {
        return this.api.get(this.getUrl(), {
            params: { ...options },
        })
    }

    get(id: number) {
        return this.api.get(this.getUrl() + id.toString())
    }

    create(data: any) {
        return this.api.post(this.getUrl(), data)
    }

    update(id: number, data: any) {
        return this.api.put(this.getUrl() + id.toString(), data)
    }

    delete(id: number) {
        return this.api.delete(this.getUrl() + id.toString())
    }
}