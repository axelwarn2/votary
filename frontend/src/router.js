import { createRouter, createWebHistory} from "vue-router";
import FormLogin from "./components/steps/forms-login/FormLogin.vue";
import FormRegistration from "./components/steps/forms-login/FormRegistration.vue";
import FormRecoverPassword from "./components/steps/forms-login/FormRecoverPassword.vue";
import RecordButton from "./components/steps/records/RecordButton.vue";
import RecordLists from "./components/steps/records/RecordLists.vue";
import RecordNotesDetail from "./components/steps/records/RecordNotesDetail.vue";
import RecordTasksDetail from "./components/steps/records/RecordTasksDetail.vue";
import RecordStatisticDetail from "./components/steps/records/RecordStatisticDetail.vue";

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: FormLogin,
    },
    {
        path: '/registration',
        name: 'Registration',
        component: FormRegistration,
    },
    {
        path: '/recover-password',
        name: 'FormRecoverPassword',
        component: FormRecoverPassword,
    },
    {
        path: '/',
        name: 'Home',
        component: RecordButton,
    },
    {
        path: '/meetings',
        name: 'RecordNotes',
        component: RecordLists,
        props: { isTasks: false, isStatistics: false },
    },
    {
        path: '/tasks',
        name: 'RecordTasks',
        component: RecordLists,
        props: { isTasks: true, isStatistics: false },
    },
    {
        path: '/statistics',
        name: 'RecordStatistics',
        component: RecordLists,
        props: { isTasks: false, isStatistics: true },
    },
    {
        path: '/meetings/:id',
        name: 'RecordNotesDetail',
        component: RecordNotesDetail,
        props: true,
    },
    {
        path: '/tasks/:id',
        name: 'RecordTasksDetail',
        component: RecordTasksDetail,
        props: true,
    },
    {
        path: '/statistics/:id',
        name: 'RecordStatisticDetail',
        component: RecordStatisticDetail,
        props: true,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
