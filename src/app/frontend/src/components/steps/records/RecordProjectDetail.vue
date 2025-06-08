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

function editProject() {
  router.push(`/projects/${project.value.id}/edit`);
}
</script>

<template>
    <div class="record-project-detail">
        <h3 class="project__title">Детали проекта</h3>
        <div v-if="project" class="project__info">
            <p class="info__item"><span class="item--size">Название:</span> {{ project.name }}</p>
            <p class="info__item"><span class="item--size">Описание:</span> {{ project.description || 'Нет описания' }}</p>
            <p class="info__item"><span class="item--size">Создан:</span> {{ new Date(project.created_at).toLocaleString('ru-RU') }}</p>
            <p class="info__item"><span class="item--size">Обновлён:</span> {{ new Date(project.updated_at).toLocaleString('ru-RU') }}</p>
            <p class="info__item"><span class="item--size">Завершённые задачи:</span> {{ project.completed_tasks || 0 }}</p>
            <p class="info__item"><span class="item--size">Незавершённые задачи:</span> {{ project.incomplete_tasks || 0 }}</p>
            
            <div class="container__button">
                <button @click="editProject" class="button__change-info">Обновить информацию</button>
                <button @click="goToProjectTasks" class="button__view-tasks">Посмотреть задачи</button>
            </div>
        </div>
        
        <div v-else>
            <p>Проект не найден</p>
        </div>
    </div>
</template>

<style scoped>
.record-project-detail {
  display: flex;
  flex-direction: column;
  padding: 50px 46px 0 46px;
  gap: 24px;
}

.project__title {
  color: rgba(0, 0, 0, 0.88);
  font-size: 32px;
  font-weight: 300;
}

.project__info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info__item {
  font-size: 16px;
}

.item--size {
  font-weight: bold;
  font-size: 18px;
}

.container__button {
  display: flex;
  gap: 24px;
}

.button__view-tasks,
.button__change-info {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button__view-tasks:hover,
.button__change-info:hover {
  background-color: #0056b3;
}
</style>
