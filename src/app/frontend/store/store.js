import { createStore } from 'vuex';

export default createStore({
    state: {
        currentView: 'RecordButton',
        viewHistory: [],
        selectNote: null,
        selectedTask: null,
        selectedStatistic: null,
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
            state.currentView = 'RecordNotesDetail';
        },
        selectTask(state, task) {
            state.selectedTask = task;
            state.viewHistory.push(state.currentView);
            state.currentView = 'RecordTasksDetail';
        },
        selectStatistic(state, statistic) {
            state.selectedStatistic = statistic;
            state.viewHistory.push(state.currentView);
            state.currentView = 'RecordStatisticDetail';
        },
        setMeetings(state, meetings) {
            state.notesData.items = meetings;
        },
        setTasks(state, tasks) {
            state.taskData.items = tasks;
        },
        setStatistics(state, statistics) {
            state.statisticsData.items = statistics
        }
    },
});
