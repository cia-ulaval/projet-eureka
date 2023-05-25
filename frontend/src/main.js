import { createApp } from 'vue'
import axios from "axios";
import App from './App.vue'

axios.defaults.baseURL = "http://192.168.1.20:5000";
createApp(App).mount('#app')

