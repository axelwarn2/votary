import { createRouter, createWebHistory} from "vue-router";
import RecordButton from "./components/steps/RecordButton.vue";
import RecordLists from "./components/steps/RecordLists.vue";
import RecordNotesDetail from "./components/steps/RecordNotesDetail.vue";
import RecordTasksDetail from "./components/steps/RecordTasksDetail.vue";
import RecordStatisticDetail from "./components/steps/RecordStatisticDetail.vue";

const routes = [
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
