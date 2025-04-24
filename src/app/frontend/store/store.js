import {createStore} from 'vuex';

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
            items: [
                {id: 12398, date: "01.01.2025", duration: "58:32"},
                {id: 12748, date: "02.01.2025", duration: "08:11"},
                {id: 12399, date: "03.01.2025", duration: "60:00"},
            ]
        },
        taskData: {
            title: "Задачи",
            headers: ["Номер  задачи", "Исполнитель", "Дата создания", "Крайний срок"],
            items: [
                {id: 12395, name: "Пятков Константин", create: "01.01.2025", deadline: "01.02.2025"},
                {id: 12745, name: "Кашин Александр", create: "01.01.2025", deadline: "02.02.2025"},
                {id: 83255, name: "Матвеев Даниил", create: "01.01.2025", deadline: "03.02.2025"},
            ]
        },
        statisticsData: {
            title: "Статистика задач",
            headers: ["Сотрудник", "Количество задач", "Завершено", "Просрочено", "Эффективность"],
            items: [
                {id: 1, employee: "Пятков Константин", count_task: "3", complete: "2", expired: "1", efficiency: "66%"},
                {id: 2, employee: "Кашин Александр", count_task: "5", complete: "5", expired: "2", efficiency: "70%"},
                {id: 3, employee: "Матвеев Даниил", count_task: "2", complete: "1", expired: "0", efficiency: "100%"},
            ]
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
    },
});
