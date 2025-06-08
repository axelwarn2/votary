import { createStore } from "vuex";
import axios from "axios";

export default createStore({
    state: {
        currentView: "RecordButton",
        viewHistory: [],
        selectNote: null,
        selectedTask: null,
        selectedStatistic: null,
        selectedProject: null,
        user: null,
        notesData: {
            title: "Записи собраний",
            headers: ["Номер собрания", "Дата собрания", "Длительность"],
            items: [],
        },
        taskData: {
            title: "Поручения",
            headers: ["Номер поручения", "Исполнитель", "Дата создания", "Крайний срок"],
            items: []
        },
        statisticsData: {
            title: "Статистика задач",
            headers: ["Сотрудник", "Количество задач", "Завершено", "Просрочено", "Эффективность"],
            items: []
        },
        projectsData: {
            title: "Проекты",
            headers: ["Название", "Количество завершенных задач", "Количество незавершенных задач"],
            items: []
        },
        projectTasks: {
            title: "Задачи проекта",
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
        selectProjects(state, project) {
            state.selectedProject = project;
            state.viewHistory.push(state.currentView);
            state.currentView = "RecordProjectDetail";
        },
        setMeetings(state, meetings) {
            state.notesData.items = meetings;
        },
        setTasks(state, tasks) {
            state.taskData.items = tasks;
        },
        setStatistics(state, statistics) {
            state.statisticsData.items = statistics;
        },
        setProjects(state, projects) {
            state.projectsData.items = projects;
        },
        setProjectTasks(state, tasks) {
            state.projectTasks.items = tasks;
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
        async fetchProjectTasks({ commit }, projectId) {
            try {
                const response = await axios.get('http://localhost:8000/tasks', {
                    params: { project_id: projectId }
                });
                commit('setProjectTasks', response.data);
                return response.data;
            } catch (error) {
                console.error('Ошибка при получении задач проекта:', error);
                throw error;
            }
        },
        async fetchStatistics({ commit }) {
            try {
                const response = await axios.get('http://localhost:8000/employees');
                commit('setStatistics', response.data);
            } catch (error) {
                console.error('Ошибка при получении статистики:', error);
            }
        },
        async fetchProjects({ commit }) {
            try {
                const response = await axios.get('http://localhost:8000/projects');
                commit('setProjects', response.data);
            } catch (error) {
                console.error('Ошибка при получении проектов:', error);
            }
        }
    }
});
