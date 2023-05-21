import { createApp } from 'vue'
import axios from "axios";
import App from './App.vue'

axios.defaults.baseURL = "http://127.0.0.1:5000";
createApp(App).mount('#app')

