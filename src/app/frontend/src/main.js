import { createApp } from 'vue'
import "./assets/style.css"
import Appointment from './Appointment.vue'
import store from "../store/store.js";
import router from "./router.js";
import axios from "axios";

axios.defaults.withCredentials = true;

document.addEventListener("DOMContentLoaded", 
    createApp(Appointment).use(store).use(router).mount('#app')
)
