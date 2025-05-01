import { createApp } from 'vue'
import "./assets/style.css"
import Appointment from './Appointment.vue'
import store from "../store/store.js";
import router from "./router.js";
import axios from "axios";

axios.defaults.withCredentials = true;

const app = createApp(Appointment);
app.use(store);
app.use(router);
app.mount('#app');
