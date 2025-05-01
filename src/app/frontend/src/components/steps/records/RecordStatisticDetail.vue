<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const statistic = ref(null);

onMounted(async () => {
    try {
        const response = await axios.get(`http://localhost:8000/employees/${route.params.id}`);
        statistic.value = response.data;
    } catch (error) {
        console.error("Ошибка получения детальной информации сотрудника: ", error);
    }
});

const name = computed(() => {
    return `${statistic.value?.surname} ${statistic.value?.name}`;
})
</script>

<template>
    <div v-if="statistic" class="record-notes-detail">
        <h3 class="record-notes-detail__title">Эффективность: {{ name }}</h3>

        <div class="efficiency-stats">
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
                <p class="efficiency-stats__completed-value">{{ statistic.complete }}</p>
            </div>
            <div class="efficiency-stats__overdue">
                <h3 class="efficiency-stats__overdue-title">Просрочено</h3>
                <p class="efficiency-stats__overdue-value">{{ statistic.expired }}</p>
            </div>
        </div>
    </div>
</template>
