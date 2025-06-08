<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const task = ref(null);
const project = ref(null);

onMounted(async () => {
    try {
        const taskResponse = await axios.get(`http://localhost:8000/tasks/${route.params.id}`);
        task.value = taskResponse.data;

        if (task.value.project_id) {
            const projectResponse = await axios.get(`http://localhost:8000/projects/${task.value.project_id}`);
            project.value = projectResponse.data;
        }
    } catch (error) {
        console.error("Ошибка получения данных: ", error);
    }
});

const date_created = computed(() => {
    return task.value?.date_created
        ? new Date(task.value.date_created).toLocaleString('ru-RU', {
              day: '2-digit',
              month: '2-digit',
              year: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
              hour12: false
          }).replace(',', '')
        : 'N/A';
});

const date_deadline = computed(() => {
    return task.value?.deadline
        ? new Date(task.value.deadline).toLocaleDateString('ru-RU')
        : 'N/A';
});

const date_production = computed(() => {
    return task.value?.date_created
        ? new Date(task.value.date_created).toLocaleDateString('ru-RU')
        : 'N/A';
});

const responcible = computed(() => {
    return task.value
        ? `${task.value.employee_surname} ${task.value.employee_name}`
        : 'N/A';
});

const leader = computed(() => {
    return task.value && task.value.leader_surname
        ? `${task.value.leader_surname} ${task.value.leader_name}`
        : 'N/A';
});

const projectName = computed(() => {
    return project.value ? project.value.name : 'Без проекта';
});
</script>

<template>
    <div v-if="task" class="record-notes-detail">
        <h3 class="record-notes-detail__title">Задача №{{ task.id }}</h3>
        <div class="record-task">
            <div class="record-notes-detail__content">
                <div class="record-notes-detail__section record-notes-detail__section--key-points">
                    <p class="record-notes-detail__section-title">Задача №{{ task.id }} - {{ task.status }}</p>
                    <a class="record-notes-detail__section-link">Изменить</a>
                </div>
                <div class="record-notes-detail__section record-notes-detail__section--text">
                    <p class="record-notes-detail__text">{{ task.description }}</p>
                </div>
                <div class="record-notes-detail__section record-notes-detail__section--download">
                    <p class="record-notes-detail__download-text">
                        Задача в проекте:
                        <router-link
                            v-if="project"
                            :to="`/projects/${task.project_id}`"
                            class="record-notes-detail__link"
                        >
                            {{ projectName }}
                        </router-link>
                        <span v-else>Без проекта</span>
                    </p>
                </div>
            </div>

            <div class="task-details">
                <div class="task-details__status" :class="{'task-details__status--green': task.status==='выполнена'}">
                    <p v-if="task.status=='выполняется'" class="task-details__status-text">Ждет выполнения с {{ date_created }}</p>
                    <p v-else class="task-details__status-text">Задача завершена</p>
                </div>

                <div class="task-details-main">
                    <div class="task-details__info">
                        <p class="task-details__info-item">Крайний срок: {{ date_deadline }}</p>
                        <p class="task-details__info-item">Напоминание: установлено</p>
                        <p class="task-details__info-item">Поставлена: {{ date_production }}</p>
                    </div>

                    <div class="task-details__participants">
                        <div class="task-details__participant">
                            <p class="task-details__participant-title">Постановщик</p>
                            <div class="task-details__participant-info">
                                <div class="task-details__avatar"></div>
                                <p class="task-details__participant-name">{{ leader }}</p>
                            </div>
                        </div>
                        <div class="task-details__participant">
                            <p class="task-details__participant-title">Ответственный</p>
                            <div class="task-details__participant-info">
                                <div class="task-details__avatar"></div>
                                <p class="task-details__participant-name">{{ responcible }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
