import { createRouter, createWebHistory } from "vue-router";
import FormLogin from "./components/steps/forms-login/FormLogin.vue";
import FormRegistration from "./components/steps/forms-login/FormRegistration.vue";
import FormRecoverPassword from "./components/steps/forms-login/FormRecoverPassword.vue";
import RecordButton from "./components/steps/records/RecordButton.vue";
import RecordLists from "./components/steps/records/RecordLists.vue";
import RecordNotesDetail from "./components/steps/records/RecordNotesDetail.vue";
import RecordTasksDetail from "./components/steps/records/RecordTasksDetail.vue";
import RecordStatisticDetail from "./components/steps/records/RecordStatisticDetail.vue";
import FormAddEmployeeLink from "./components/steps/forms-add/FormAddEmployeeLink.vue";
import FormAddEmployee from "./components/steps/forms-add/FormAddEmployee.vue";
import axios from "axios";

const routes = [
    {
        path: "/login",
        name: "Login",
        component: FormLogin,
    },
    {
        path: "/registration",
        name: "Registration",
        component: FormRegistration,
    },
    {
        path: "/recover-password",
        name: "FormRecoverPassword",
        component: FormRecoverPassword,
    },
    {
        path: "/record",
        name: "Home",
        component: RecordButton,
        meta: { requiresAuth: true },
    },
    {
        path: "/meetings",
        name: "RecordNotes",
        component: RecordLists,
        props: { isTasks: false, isStatistics: false },
        meta: { requiresAuth: true },
    },
    {
        path: "/tasks",
        name: "RecordTasks",
        component: RecordLists,
        props: { isTasks: true, isStatistics: false },
        meta: { requiresAuth: true },
    },
    {
        path: "/statistics",
        name: "RecordStatistics",
        component: RecordLists,
        props: { isTasks: false, isStatistics: true },
        meta: { requiresAuth: true },
    },
    {
        path: "/meetings/:id",
        name: "RecordNotesDetail",
        component: RecordNotesDetail,
        props: true,
        meta: { requiresAuth: true },
    },
    {
        path: "/tasks/:id",
        name: "RecordTasksDetail",
        component: RecordTasksDetail,
        props: true,
        meta: { requiresAuth: true },
    },
    {
        path: "/statistics/:id",
        name: "RecordStatisticDetail",
        component: RecordStatisticDetail,
        props: true,
        meta: { requiresAuth: true },
    },
    {
        path: "/add-employee-link",
        name: "FormAddEmployeeLink",
        component: FormAddEmployeeLink,
        meta: { requiresAuth: true },
    },
    {
        path: "/add-employee",
        name: "FormAddEmployee",
        component: FormAddEmployee,
        meta: { requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAuth) {
        try {
            const response = await axios.get("http://localhost:8000/me", {
                withCredentials: true,
            });
            if (response.data) {
                next();
            } else {
                next("/login");
            }
        } catch (error) {
            console.error("Ошибка проверки авторизации:", error);
            next("/login");
        }
    } else {
        next();
    }
});

export default router;
