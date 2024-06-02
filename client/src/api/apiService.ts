import axios from 'axios'

export default async function postRequest(endpoint: string, body: { code: string }) {
    let data: string = ''
    let error: string = ''
    // TODO: Move to .env
    const url: string = 'http://localhost:8000' + endpoint
    try {
        const response = await axios.post(url, body);
        data = response.data
    } catch (err) {
        error = err;
    }
    return { data, error }
}