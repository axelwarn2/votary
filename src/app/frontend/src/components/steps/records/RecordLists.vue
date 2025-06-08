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
const showDeleteDialog = ref(false);
const itemToDelete = ref(null);
const deleteType = ref('');

const loadData = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    if (props.isTasks) {
      try {
        const employeeResponse = await axios.get('http://localhost:8000/employees');
        console.log('Employees response:', employeeResponse.data);
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
      console.log('Tasks response:', taskResponse.data);
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

const openDeleteDialog = (item, type) => {
  itemToDelete.value = item;
  deleteType.value = type;
  showDeleteDialog.value = true;
};

const closeDeleteDialog = () => {
  showDeleteDialog.value = false;
  itemToDelete.value = null;
  deleteType.value = '';
};

const confirmDelete = async () => {
  try {
    if (deleteType.value === 'task') {
      await axios.delete(`http://localhost:8000/tasks/${itemToDelete.value.id}`);
      tasks.value = tasks.value.filter(task => task.id !== itemToDelete.value.id);
      store.commit('setTasks', tasks.value);
    } else if (deleteType.value === 'project') {
      await axios.delete(`http://localhost:8000/projects/${itemToDelete.value.id}`);
      projects.value = projects.value.filter(project => project.id !== itemToDelete.value.id);
      store.commit('setProjects', projects.value);
    } else if (deleteType.value === 'employee') {
      await axios.delete(`http://localhost:8000/employees/${itemToDelete.value.id}`);
      employees.value = employees.value.filter(employee => employee.id !== itemToDelete.value.id);
      store.commit('setStatistics', employees.value);
    }
    closeDeleteDialog();
    await loadData();
  } catch (error) {
    errorMessage.value = `Ошибка при удалении: ${error.response?.data?.detail || error.message}`;
    console.error('Delete error:', error);
    closeDeleteDialog();
  }
};
</script>

<template>
  <div class="record-notes">
    <h3 class="record-notes__title">{{ title }}</h3>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div class="filters">
      <div v-if="props.isTasks" class="filters__group filters__group--employees">
        <p class="filters__label">Сотрудники</p>
        <select v-model="employeeIdsFilter" class="filters__input filters__input--select filters__input--single-line">
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
        <span class="record-notes__header-item record-notes__actions"></span>
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
            >
              <div class="record-notes__item-content" @click="selectItem(task)">
                <p
                  v-for="(value, index) in getItemValues(task)"
                  :key="index"
                  class="record-notes__item-text"
                >
                  {{ value }}
                </p>
              </div>
              <button class="record-notes__delete-btn" @click.stop="openDeleteDialog(task, 'task')">
                <svg class="delete-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2m-8 0h8m-10 4v10a2 2 0 002 2h6a2 2 0 002-2V10m-7 7v-7m4 7v-7"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="record-notes__list">
        <div class="record-notes__header">
          <p v-for="(header, index) in headers" :key="index" class="record-notes__header-item">
            {{ header }}
          </p>
          <span v-if="props.isProjects || props.isStatistics" class="record-notes__header-item record-notes__actions"></span>
        </div>
        <div
          v-for="(item, index) in items"
          :key="index"
          class="record-notes__item"
        >
          <div class="record-notes__item-content" @click="selectItem(item)">
            <p
              v-for="(value, key) in getItemValues(item)"
              :key="key"
              class="record-notes__item-text"
            >
              {{ value }}
            </p>
          </div>
          <button
            v-if="props.isProjects || props.isStatistics"
            class="record-notes__delete-btn"
            @click.stop="openDeleteDialog(item, props.isProjects ? 'project' : 'employee')"
          >
            <svg class="delete-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2m-8 0h8m-10 4v10a2 2 0 002 2h6a2 2 0 002-2V10m-7 7v-7m4 7v-7"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="record-button__add-employee" v-if="props.isStatistics">
    <router-link to="/add-employee-link" class="record-button__add-employee--link">
      <button class="button__add-employee">Добавить сотрудника</button>
    </router-link>
  </div>
  <div class="record-button__add-employee" v-if="props.isProjects">
    <router-link to="/add-project" class="record-button__add-employee--link">
      <button class="button__add-employee">Добавить проект</button>
    </router-link>
  </div>
  <dialog class="delete-dialog" v-if="showDeleteDialog" open>
    <div class="delete-dialog__content">
      <h3 class="delete-dialog__title">Подтверждение удаления</h3>
      <p class="delete-dialog__message">
        Вы уверены, что хотите удалить
        {{ deleteType === 'task' ? 'поручение' : deleteType === 'project' ? 'проект' : 'сотрудника' }}
        {{ deleteType === 'task' ? `#${itemToDelete?.id}` : deleteType === 'project' ? itemToDelete?.name : `${itemToDelete?.surname} ${itemToDelete?.name}` }}?
      </p>
      <div class="delete-dialog__buttons">
        <button class="delete-dialog__btn delete-dialog__btn--confirm" @click="confirmDelete">Удалить</button>
        <button class="delete-dialog__btn delete-dialog__btn--cancel" @click="closeDeleteDialog">Отмена</button>
      </div>
    </div>
  </dialog>
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
.record-notes__actions {
  width: 40px;
}
.record-notes__item {
  display: flex;
  align-items: center;
}
.record-notes__item-content {
  display: flex;
  flex: 1;
}
.record-notes__delete-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: none;
  border: none;
  cursor: pointer;
  color: #dc3545;
}
.delete-icon {
  width: 20px;
  height: 20px;
}
.record-notes__delete-btn:hover .delete-icon {
  color: #b02a37;
}
.delete-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background: rgba(128, 128, 128, 0.5);
  border: none;
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}
.delete-dialog__content {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  max-width: 400px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.delete-dialog__title {
  font-size: 20px;
  margin: 0;
}
.delete-dialog__message {
  margin: 0;
}
.delete-dialog__buttons {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}
.delete-dialog__btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.delete-dialog__btn--confirm {
  background-color: #dc3545;
  color: white;
}
.delete-dialog__btn--confirm:hover {
  background-color: #b02a37;
}
.delete-dialog__btn--cancel {
  background-color: #6c757d;
  color: white;
}
.delete-dialog__btn--cancel:hover {
  background-color: #5a6268;
}
</style>