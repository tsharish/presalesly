function getBaseUrl() {
    const url = window.location.origin
    const urlWithoutPort = url.substring(0, url.search(":5173"))
    return urlWithoutPort
}

export default class BaseApiService {
    baseUrl = import.meta.env.DEV ? getBaseUrl() + ':8000/api/v1' : '/api/v1'
    resource: string

    constructor(resource: string) {
        this.resource = resource
    }

    getUrl() {
        return `${this.baseUrl}/${this.resource}/`
    }
}