import axios from 'axios';


export async function getMap() {
    const url = `${axios.defaults.baseURL}map`;
    return axios.get(url).then(response => response.data);
}
