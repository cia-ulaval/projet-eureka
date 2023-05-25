import axios from 'axios';


export async function getMap() {
    const url = `${axios.defaults.baseURL}/map`;
    axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
    return axios.get(url).then(response => response.data);
}