import { createApp } from 'vue'
import axios from "axios";
import App from './App.vue'

axios.defaults.baseURL = "https://quiet-hamlet-73980.herokuapp.com/";
createApp(App).mount('#app')

