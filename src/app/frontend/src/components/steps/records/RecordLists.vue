<script setup>
import { computed, ref, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import axios from 'axios';

const props = defineProps({
  isTasks: Boolean,
  isStatistics: Boolean,
  isProjects: Boolean,
});

const store = useStore();
const router = useRouter();
const isLoading = ref(false);
const employeeNameFilter = ref('');
const dateFilter = ref('');
const projectFilter = ref(null);
const projects = ref([]);
const tasks = ref([]);
const expandedProjects = ref({}); // Состояние раскрытых проектов

const loadData = async () => {
  isLoading.value = true;
  try {
    if (props.isTasks) {
      const params = {};
      if (employeeNameFilter.value) params.employee_name = employeeNameFilter.value;
      if (dateFilter.value) params.date_filter = dateFilter.value;
      if (projectFilter.value) params.project_id = projectFilter.value;
      const taskResponse = await axios.get('http://localhost:8000/tasks', { params });
      tasks.value = taskResponse.data;
      store.commit('setTasks', taskResponse.data);

      const projectResponse = await axios.get('http://localhost:8000/projects');
      projects.value = projectResponse.data;
    } else if (props.isStatistics) {
      await store.dispatch('fetchStatistics');
    } else if (props.isProjects) {
      await store.dispatch('fetchProjects');
    } else {
      await store.dispatch('fetchMeetings');
    }
  } finally {
    isLoading.value = false;
  }
};

onMounted(loadData);

watch(
  () => [props.isTasks, props.isStatistics, props.isProjects, employeeNameFilter.value, dateFilter.value, projectFilter.value],
  () => {
    loadData();
  }
);

// Группировка задач по проектам
const tasksByProject = computed(() => {
  const grouped = {};
  projects.value.forEach(project => {
    grouped[project.id] = {
      name: project.name,
      tasks: tasks.value.filter(task => task.project_id === project.id),
    };
  });
  // Добавляем задачи без проекта
  grouped['no_project'] = {
    name: 'Без проекта',
    tasks: tasks.value.filter(task => !task.project_id),
  };
  return grouped;
});

const headers = computed(() => {
  if (props.isTasks) return store.state.taskData.headers;
  if (props.isStatistics) return store.state.statisticsData.headers;
  if (props.isProjects) return store.state.projectsData.headers;
  return store.state.notesData.headers;
});

const title = computed(() => {
  if (props.isTasks) return store.state.taskData.title;
  if (props.isStatistics) return store.state.statisticsData.title;
  if (props.isProjects) return store.state.projectsData.title;
  return store.state.notesData.title;
});

const items = computed(() => {
  if (props.isTasks) return store.state.taskData.items;
  if (props.isStatistics) return store.state.statisticsData.items;
  if (props.isProjects) return store.state.projectsData.items;
  return store.state.notesData.items;
});

const selectItem = (item) => {
  if (props.isTasks) {
    store.commit('selectTask', item);
    router.push(`/tasks/${item.id}`);
  } else if (props.isStatistics) {
    store.commit('selectStatistic', item);
    router.push(`/statistics/${item.id}`);
  } else if (props.isProjects) {
    store.commit('selectProjects', item);
    router.push(`/projects/${item.id}`);
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
  } else if (props.isProjects) {
    return [item.name, item.completed_tasks || 0, item.incomplete_tasks || 0];
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

// Переключение состояния раскрытия проекта
const toggleProject = (projectId) => {
  expandedProjects.value[projectId] = !expandedProjects.value[projectId];
};
</script>

<template>
  <div class="record-notes">
    <h3 class="record-notes__title">{{ title }}</h3>
    <div class="record-notes__content">
      <!-- Заголовок таблицы для задач -->
      <div v-if="props.isTasks" class="record-notes__header">
        <p v-for="(header, index) in headers" :key="index" class="record-notes__header-item">
          {{ header }}
        </p>
      </div>
      <!-- Список задач, сгруппированный по проектам -->
      <div v-if="props.isTasks" class="record-notes__list">
        <div v-for="(project, projectId) in tasksByProject" :key="projectId" class="project-group">
          <div class="project-header" @click="toggleProject(projectId)">
            <span class="toggle-button">{{ expandedProjects[projectId] ? '-' : '+' }}</span>
            <span class="project-name">{{ project.name }} ({{ project.tasks.length }})</span>
          </div>
          <div v-if="expandedProjects[projectId]" class="project-tasks">
            <div
              v-for="task in project.tasks"
              :key="task.id"
              class="record-notes__item"
              @click="selectItem(task)"
            >
              <p
                v-for="(value, index) in getItemValues(task)"
                :key="index"
                class="record-notes__item-text"
              >
                {{ value }}
              </p>
            </div>
          </div>
        </div>
      </div>
      <!-- Обычный список для других типов данных -->
      <div v-else class="record-notes__list">
        <div class="record-notes__header">
          <p v-for="(header, index) in headers" :key="index" class="record-notes__header-item">
            {{ header }}
          </p>
        </div>
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

<style scoped>
.project-group {
  padding-bottom: 10px;
}
.project-header {
  display: flex;
  align-items: center;
  padding: 10px;
  background: #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
}
.toggle-button {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #007bff;
  color: white;
  font-size: 14px;
  margin-right: 10px;
  user-select: none;
}
.project-tasks {
  padding-top: 10px;
  padding-left: 30px;
}
.record-button__add-employee {
  margin-top: 20px;
  text-align: center;
}
</style>
