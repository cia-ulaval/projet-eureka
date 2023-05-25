import axios from 'axios';


export async function getScore(path) {
    const url = `${axios.defaults.baseURL}score`;
    const data = {
        path: path
    };
    return axios.post(url, data).then((response) => response.data);
}