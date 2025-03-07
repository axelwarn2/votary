import { createApp } from 'vue'
import "./assets/style.css"
import Appointment from './Appointment.vue'
import store from "../store/store.js";


createApp(Appointment).use(store).mount('#app')
