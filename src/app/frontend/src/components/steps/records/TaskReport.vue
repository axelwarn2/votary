<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const report = ref(null);

onMounted(async () => {
    try {
        const response = await axios.get(`http://localhost:8000/tasks/report/${route.params.employee_id}`);
        report.value = response.data;
    } catch (error) {
        console.error("Ошибка получения отчета:", error);
    }
});
</script>

<template>
    <div v-if="report" class="task-report">
        <h3 class="task-report__title">Отчет по задачам сотрудника №{{ report.employee_id }}</h3>
        <div class="task-report__content">
            <p class="task-report__item">Всего задач: {{ report.total_tasks }}</p>
            <p class="task-report__item">Завершено: {{ report.completed }}</p>
            <p class="task-report__item">В работе: {{ report.in_progress }}</p>
            <p class="task-report__item">Просрочено: {{ report.expired }}</p>
        </div>
    </div>
</template>

<style scoped>
.task-report {
    padding: 20px;
}
.task-report__title {
    font-size: 24px;
    margin-bottom: 20px;
}
.task-report__content {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.task-report__item {
    font-size: 16px;
}
</style>
