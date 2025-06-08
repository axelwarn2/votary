<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const statistic = ref(null);
const isOnSickLeave = ref(false);
const isOnVacation = ref(false);
const updateMessage = ref('');
const updateError = ref('');
const currentUser = ref(null);
const loadingError = ref('');

onMounted(async () => {
    console.log('Route params ID:', route.params.id);
    try {
        const userResponse = await axios.get('http://localhost:8000/me', { withCredentials: true });
        currentUser.value = userResponse.data;
        console.log('Current user:', currentUser.value);

        const response = await axios.get(`http://localhost:8000/employees/${route.params.id}`, { withCredentials: true });
        console.log('Employee response:', response.data);
        statistic.value = response.data;
        isOnSickLeave.value = statistic.value.is_on_sick_leave;
        isOnVacation.value = statistic.value.is_on_vacation;
    } catch (error) {
        loadingError.value = error.response?.data?.detail || 'Ошибка загрузки данных сотрудника';
        console.error('Ошибка получения данных:', error);
    }
});

const name = computed(() => {
    return statistic.value ? `${statistic.value.surname} ${statistic.value.name}` : 'Загрузка...';
});

const isLeader = computed(() => {
    return currentUser.value?.role === 'руководитель';
});

const updateStatus = async () => {
    updateMessage.value = '';
    updateError.value = '';
    try {
        const response = await axios.patch(
            `http://localhost:8000/employees/${route.params.id}/status`,
            {
                is_on_sick_leave: isOnSickLeave.value,
                is_on_vacation: isOnVacation.value,
            },
            { withCredentials: true }
        );
        updateMessage.value = response.data.message;
        statistic.value.is_on_sick_leave = isOnSickLeave.value;
        statistic.value.is_on_vacation = isOnVacation.value;
    } catch (error) {
        updateError.value = error.response?.data?.detail || 'Ошибка при обновлении статуса';
        console.error('Ошибка обновления статуса:', error);
    }
};
</script>

<template>
    <div class="record-notes-detail">
        <h3 class="record-notes-detail__title">Эффективность: {{ name }}</h3>

        <div v-if="loadingError" class="error-message">
            {{ loadingError }}
        </div>

        <div v-else-if="statistic" class="efficiency-stats">
            <div class="efficiency-stats__overview">
                <h3 class="efficiency-stats__overview-title">Эффективность</h3>
                <div class="efficiency-stats__circle-container">
                    <div class="efficiency-stats__circle--first">
                        <div class="efficiency-stats__circle--second">
                            <div class="efficiency-stats__circle--third">
                                {{ statistic.efficiency }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="efficiency-stats__in-progress">
                <h3 class="efficiency-stats__in-progress-title">Всего в работе</h3>
                <p class="efficiency-stats__in-progress-value">{{ statistic.count_task }}</p>
            </div>
            <div class="efficiency-stats__completed">
                <h3 class="efficiency-stats__completed-title">Завершено</h3>
                <p class="efficiency-stats__completed-value">{{ statistic.completed }}</p>
            </div>
            <div class="efficiency-stats__overdue">
                <h3 class="efficiency-stats__overdue-title">Просрочено</h3>
                <p class="efficiency-stats__overdue-value">{{ statistic.expired }}</p>
            </div>
        </div>

        <div v-if="isLeader && statistic" class="employee-status">
            <h3 class="employee-status__title">Статус сотрудника</h3>
            <div class="employee-status__checkboxes">
                <label class="employee-status__checkbox">
                    <input type="checkbox" v-model="isOnSickLeave" />
                    На больничном
                </label>
                <label class="employee-status__checkbox">
                    <input type="checkbox" v-model="isOnVacation" />
                    В отпуске
                </label>
            </div>
            <button class="employee-status__save-button" @click="updateStatus">Сохранить статус</button>
            <p v-if="updateMessage" class="employee-status__message">{{ updateMessage }}</p>
            <p v-if="updateError" class="employee-status__error">{{ updateError }}</p>
        </div>

        <div v-if="!statistic && !loadingError" class="loading-message">
            Загрузка данных...
        </div>
    </div>
</template>

<style scoped>
.employee-status {
    margin-top: 2rem;
    padding: 1.5rem;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.employee-status__title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #333;
}

.employee-status__checkboxes {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.employee-status__checkbox {
    display: flex;
    align-items: center;
    font-size: 1rem;
    color: #555;
}

.employee-status__checkbox input {
    margin-right: 0.5rem;
    width: 18px;
    height: 18px;
}

.employee-status__save-button {
    padding: 0.5rem 1rem;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s;
}

.employee-status__save-button:hover {
    background-color: #3d8b8f;
}

.employee-status__message {
    color: #28a745;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

.employee-status__error {
    color: #dc3545;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

.error-message {
    color: #dc3545;
    font-size: 1rem;
    margin-top: 1rem;
}

.loading-message {
    font-size: 1rem;
    color: #555;
    margin-top: 1rem;
}
</style>
