<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const task = ref(null);

onMounted(async () => {
    try {
        const response = await axios.get(`http://localhost:8000/tasks/${route.params.id}`);
        task.value = response.data;
    } catch (error) {
        console.error("Ошибка получения детальной информации задачи: ", error);
    }
});

const date_created = computed(() => {
    return new Date(task.value.date_created).toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    }).replace(',', '');
});

const date_deadline = computed(() => {
    return new Date(task.value.deadline).toLocaleDateString('ru-RU');
});

const date_production = computed(() => {
    return new Date(task.value.date_created).toLocaleDateString('ru-RU');
});

const responcible = computed(() => {
    return `${task.value?.employee_surname} ${task.value?.employee_name}`;
})

const leader = computed(() => {
    return `${task.value?.leader_surname} ${task.value?.leader_name}`;
});
</script>

<template>
    <div v-if="task" class="record-notes-detail">
        <h3 class="record-notes-detail__title">Задача №{{ task.id }}</h3>
        <div class="record-task">
            <div class="record-notes-detail__content">
                <div class="record-notes-detail__section record-notes-detail__section--key-points">
                    <p class="record-notes-detail__section-title">Задача №{{ task.id }} - {{ task.status }}</p>
                </div>
                <div class="record-notes-detail__section record-notes-detail__section--text">
                    <p class="record-notes-detail__text">{{ task.description }}</p>
                </div>
                <div class="record-notes-detail__section record-notes-detail__section--download">
                    <p class="record-notes-detail__download-text">
                        Задача в проекте: <a href="#" class="record-notes-detail__link">Модуль фильтрации</a>
                    </p>
                </div>
            </div>

            <div class="task-details">
                <div class="task-details__status">
                    <p class="task-details__status-text">Ждет выполнения с {{ date_created }}</p>
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
