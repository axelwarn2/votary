import { createStore } from "vuex";
import axios from "axios";

export default createStore({
    state: {
        currentView: "RecordButton",
        viewHistory: [],
        selectNote: null,
        selectedTask: null,
        selectedStatistic: null,
        user: null,
        notesData: {
            title: "Записи собраний",
            headers: ["Номер собрания", "Дата собрания", "Длительность"],
            items: [],
        },
        taskData: {
            title: "Задачи",
            headers: ["Номер  задачи", "Исполнитель", "Дата создания", "Крайний срок"],
            items: []
        },
        statisticsData: {
            title: "Статистика задач",
            headers: ["Сотрудник", "Количество задач", "Завершено", "Просрочено", "Эффективность"],
            items: []
        }
    },
    mutations: {
        selectNote(state, meeting) {
            state.selectNote = meeting;
            state.viewHistory.push(state.currentView);
            state.currentView = "RecordNotesDetail";
        },
        selectTask(state, task) {
            state.selectedTask = task;
            state.viewHistory.push(state.currentView);
            state.currentView = "RecordTasksDetail";
        },
        selectStatistic(state, statistic) {
            state.selectedStatistic = statistic;
            state.viewHistory.push(state.currentView);
            state.currentView = "RecordStatisticDetail";
        },
        setMeetings(state, meetings) {
            state.notesData.items = meetings;
        },
        setTasks(state, tasks) {
            state.taskData.items = tasks;
        },
        setStatistics(state, statistics) {
            state.statisticsData.items = statistics
        },
        setUser(state, user) {
            state.user = user;
        },
        clearUser(state) {
            state.user = null;
        }
    },
    actions: {
        async fetchUser({ commit }) {
            try {
                const response = await axios.get("http://localhost:8000/me", {
                    withCredentials: true
                });
                commit("setUser", response.data);
            } catch (error) {
                commit("clearUser");
                console.error("Ошибка получения пользователя:", error);
            }
        },
        async logout({ commit }) {
            try {
                await axios.post("http://localhost:8000/logout", null, {
                    withCredentials: true
                });
                commit("clearUser");
            } catch (error) {
                console.error("Ошибка выхода:", error);
            }
        },
        async fetchMeetings({ commit }) {
            try {
                const response = await axios.get('http://localhost:8000/meetings');
                commit('setMeetings', response.data);
            } catch (error) {
                console.error('Ошибка при получении встреч:', error);
            }
        },
        async fetchTasks({ commit }) {
            try {
                const response = await axios.get('http://localhost:8000/tasks');
                commit('setTasks', response.data);
            } catch (error) {
                console.error('Ошибка при получении задач:', error);
            }
        },
        async fetchStatistics({ commit }) {
            try {
                const response = await axios.get('http://localhost:8000/employees');
                commit('setStatistics', response.data);
            } catch (error) {
                console.error('Ошибка при получении статистики:', error);
            }
        }
    }
});
