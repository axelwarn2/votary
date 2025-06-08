<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const project = computed(() => store.state.selectedProject);

function goToProjectTasks() {
    router.push(`/projects/${project.value.id}/tasks`);
}
</script>

<template>
    <div class="record-project-detail">
        <h3>Детали проекта</h3>
        <div v-if="project">
            <p><strong>Название:</strong> {{ project.name }}</p>
            <p><strong>Описание:</strong> {{ project.description || 'Нет описания' }}</p>
            <p><strong>Создан:</strong> {{ new Date(project.created_at).toLocaleString('ru-RU') }}</p>
            <p><strong>Обновлён:</strong> {{ new Date(project.updated_at).toLocaleString('ru-RU') }}</p>
            <p><strong>Завершённые задачи:</strong> {{ project.completed_tasks || 0 }}</p>
            <p><strong>Незавершённые задачи:</strong> {{ project.incomplete_tasks || 0 }}</p>
            <button @click="goToProjectTasks" class="button__view-tasks">Посмотреть задачи</button>
        </div>
        <div v-else>
            <p>Проект не найден</p>
        </div>
    </div>
</template>

<style scoped>
.button__view-tasks {
    margin-top: 10px;
    padding: 8px 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
.button__view-tasks:hover {
    background-color: #0056b3;
}
</style>
