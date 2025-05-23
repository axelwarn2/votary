<script setup>
import { computed, ref, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import axios from 'axios';

const props = defineProps({
    isTasks: Boolean,
    isStatistics: Boolean,
});

const store = useStore();
const router = useRouter();
const isLoading = ref(false);

const loadData = async () => {
    isLoading.value = true;

    try {
        if (props.isTasks) {
            await store.dispatch('fetchTasks');
        } else if (props.isStatistics) {
            await store.dispatch('fetchStatistics');
        } else {
            await store.dispatch('fetchMeetings');
        }
    } finally {
        isLoading.value = false;
    }
}

onMounted(loadData);

watch(
    () => [props.isTasks, props.isStatistics],
    () => {
        loadData();
    }
)

const headers = computed(() => {
    if (props.isTasks) return store.state.taskData.headers;
    if (props.isStatistics) return store.state.statisticsData.headers;
    return store.state.notesData.headers;
});

const title = computed(() => {
    if (props.isTasks) return store.state.taskData.title;
    if (props.isStatistics) return store.state.statisticsData.title;
    return store.state.notesData.title;
});

const items = computed(() => {
    if (props.isTasks) return store.state.taskData.items;
    if (props.isStatistics) return store.state.statisticsData.items;
    return store.state.notesData.items;
});

const selectItem = (item) => {
    if (props.isTasks) {
        store.commit('selectTask', item);
        router.push(`/tasks/${item.id}`);
    } else if (props.isStatistics) {
        store.commit('selectStatistic', item);
        router.push(`/statistics/${item.id}`);
    } else {
        store.commit('selectNote', item);
        router.push(`/meetings/${item.id}`);
    }
};

const getItemValues = (item) => {
    if (props.isStatistics) {
        const name = `${item.surname} ${item.name}`;
        return [name, item.count_task, item.complete, item.expired, item.efficiency];
    } else if (props.isTasks) {
        const date_created = item.date_created ? new Date(item.date_created).toLocaleDateString('ru-RU') : 'N/A';
        const deadline = item.deadline ? new Date(item.deadline).toLocaleDateString('ru-RU') : 'N/A';
        const name = `${item.employee_surname} ${item.employee_name}`;

        return [item.id, name, date_created, deadline];
    } else {
        const date = item.date_event ? new Date(item.date_event).toLocaleDateString('ru-RU') : 'N/A';
        const duration = item.time_start && item.time_end ? calculateDuration(item.time_start, item.time_end) : '0:00';
        return [item.id, date, duration];
    }
};

function calculateDuration(start, end) {
    if (!start || !end) return '0:00';
    try {
        const startTime = new Date(`1970-01-01T${start}Z`);
        const endTime = new Date(`1970-01-01T${end}Z`);
        const diffMs = endTime - startTime;

        if (isNaN(diffMs)) return '0:00';

        const hours = Math.floor(diffMs / (1000 * 60 * 60));
        const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diffMs % (1000 * 60)) / 1000);

        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    } catch (error) {
        console.error('Ошибка в calculateDuration:', error);
        return '0:00';
    }
}
</script>

<template>
    <div class="record-notes">
        <h3 class="record-notes__title">{{ title }}</h3>
        <div class="record-notes__content">
            <div class="record-notes__header">
                <p
                        v-for="(header, index) in headers"
                        :key="index"
                        class="record-notes__header-item"
                >
                    {{ header }}
                </p>
            </div>
            <div class="record-notes__list">
                <div
                        v-for="(item, index) in items"
                        :key="index"
                        class="record-notes__item"
                        @click="selectItem(item)"
                >
                    <p
                            v-for="(value, index) in getItemValues(item)"
                            :key="index"
                            class="record-notes__item-text"
                    >
                        {{ value }}
                    </p>
                </div>
            </div>
        </div>
    </div>
    <div class="record-button__add-employee" v-if="isStatistics">
        <router-link to="/add-employee-link" class="record-button__add-employee--link">
            <button class="button__add-employee">Добавить сотрудника</button>
        </router-link>
    </div>
</template>
