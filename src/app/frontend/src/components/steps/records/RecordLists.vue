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
const employeeIdsFilter = ref([]);
const dateFromFilter = ref('');
const dateToFilter = ref('');
const projectFilter = ref(null);
const urgencyFilter = ref('');
const projects = ref([]);
const tasks = ref([]);
const employees = ref([]);
const expandedProjects = ref({});
const errorMessage = ref('');

const loadData = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    if (props.isTasks) {
      try {
        const employeeResponse = await axios.get('http://localhost:8000/employees');
        console.log('Employees response:', employeeResponse.data); // Логирование для отладки
        employees.value = employeeResponse.data;
      } catch (err) {
        errorMessage.value = 'Ошибка загрузки сотрудников: ' + err.message;
        console.error('Employee fetch error:', err);
      }

      const params = {};
      if (employeeIdsFilter.value.length) params.employee_ids = employeeIdsFilter.value.join(',');
      if (dateFromFilter.value) params.date_from = dateFromFilter.value;
      if (dateToFilter.value) params.date_to = dateToFilter.value;
      if (projectFilter.value) params.project_id = projectFilter.value;
      if (urgencyFilter.value) params.urgency = urgencyFilter.value === 'Приоритетная' ? 'да' : 'нет';
      const taskResponse = await axios.get('http://localhost:8000/tasks', { params });
      console.log('Tasks response:', taskResponse.data); // Логирование для отладки
      tasks.value = taskResponse.data;
      store.commit('setTasks', taskResponse.data);

      const projectResponse = await axios.get('http://localhost:8000/projects');
      projects.value = projectResponse.data;
    } else if (props.isStatistics) {
      await store.dispatch('fetchStatistics');
    } else if (props.isProjects) {
      await store.dispatch('fetchProjects');
    } else {
      const params = {};
      if (dateFromFilter.value) params.date_from = dateFromFilter.value;
      if (dateToFilter.value) params.date_to = dateToFilter.value;
      const meetingResponse = await axios.get('http://localhost:8000/meetings', { params });
      store.commit('setMeetings', meetingResponse.data);
    }
  } catch (err) {
    errorMessage.value = 'Ошибка загрузки данных: ' + err.message;
    console.error('Load data error:', err);
  } finally {
    isLoading.value = false;
  }
};

onMounted(loadData);

watch(
  () => [props.isTasks, props.isStatistics, props.isProjects, employeeIdsFilter.value, dateFromFilter.value, dateToFilter.value, projectFilter.value, urgencyFilter.value],
  () => {
    loadData();
  },
  { deep: true }
);

const tasksByProject = computed(() => {
  const grouped = {};
  projects.value.forEach(project => {
    grouped[project.id] = {
      name: project.name,
      tasks: tasks.value.filter(task => task.project_id === project.id),
    };
  });
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
    return [name, item.count_task, item.completed, item.expired, item.efficiency];
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

const toggleProject = (projectId) => {
  expandedProjects.value[projectId] = !expandedProjects.value[projectId];
};
</script>

<template>
  <div class="record-notes">
    <h3 class="record-notes__title">{{ title }}</h3>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div class="filters">
      <div v-if="props.isTasks" class="filters__group filters__group--employees">
        <p class="filters__label">Сотрудники</p>
        <select v-model="employeeIdsFilter" class="filters__input filters__input--select 
        filters__input--single-line">
          <option value="" class="filters__option">Все сотрудники</option>
          <option v-for="employee in employees" :key="employee.id" :value="employee.id" class="filters__option">
            {{ employee.surname }} {{ employee.name }}
          </option>
        </select>
      </div>
      <div class="filters__group filters__group--period">
        <p class="filters__label">Период</p>
        <div class="filters__period">
          <div class="filters__period-item">
            <p class="filters__sublabel">От:</p>
            <input type="date" v-model="dateFromFilter" class="filters__input filters__input--date">
          </div>
          <div class="filters__period-item">
            <p class="filters__sublabel">До:</p>
            <input type="date" v-model="dateToFilter" class="filters__input filters__input--date">
          </div>
        </div>
      </div>
      <div v-if="props.isTasks" class="filters__group filters__group--project">
        <p class="filters__label">Проект</p>
        <select v-model="projectFilter" class="filters__input filters__input--select">
          <option :value="null" class="filters__option">Все проекты</option>
          <option v-for="project in projects" :key="project.id" :value="project.id" class="filters__option">
            {{ project.name }}
          </option>
        </select>
      </div>
      <div v-if="props.isTasks" class="filters__group filters__group--urgency">
        <p class="filters__label">Приоритетность</p>
        <select v-model="urgencyFilter" class="filters__input filters__input--select">
          <option value="" class="filters__option">Все задачи</option>
          <option value="Приоритетная" class="filters__option">Приоритетная</option>
          <option value="Не приоритетная" class="filters__option">Не приоритетная</option>
        </select>
      </div>
    </div>
    <div class="record-notes__content">
      <div v-if="props.isTasks" class="record-notes__header">
        <p v-for="(header, index) in headers" :key="index" class="record-notes__header-item">
          {{ header }}
        </p>
      </div>
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
              :class="{ 'priority-task': task.urgency === 'да', 'non-priority-task': task.urgency === 'нет' }"
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
            v-for="(value, key) in getItemValues(item)"
            :key="key"
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
  <div class="record-button__add-employee" v-if="isProjects">
    <router-link to="/add-project" class="record-button__add-employee--link">
      <button class="button__add-employee">Добавить проект</button>
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
.priority-task {
  position: relative;
  border: 2px solid #ffd700;
}
.priority-task::before {
  content: '★';
  position: absolute;
  top: -6px;
  right: 6px;
  color: #ffd700;
  font-size: 20px;
}
.non-priority-task {
  border: 1px solid #ccc;
}
.filters {
  display: flex;
  width: 100%;
  gap: 3%;
}

.filters__group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filters__label {
  font-weight: 600;
}

.filters__group--employees {
  width: 20%;
}

.filters__period {
  display: flex;
  gap: 10px;
}

.filters__period-item {
  display: flex;
  gap: 10px;
}
</style>