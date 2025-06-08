<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

const store = useStore();
const router = useRouter();
const route = useRoute();

const isLoading = ref(false);
const completed = ref([]);
const incomplete = ref([]);
const incompleteEl = ref(null);
const completedEl = ref(null);

const title = computed(() => {
  const projectName = store.state.selectedProject?.name || 'Неизвестный проект';
  return `Поручения проекта ${projectName}`;
});

const loadData = async () => {
  isLoading.value = true;
  try {
    const projectId = parseInt(route.params.id);
    await store.dispatch('fetchProjectTasks', projectId);
    const items = store.state.projectTasks.items;
    completed.value = items.filter(task => task.status === 'выполнена');
    incomplete.value = items.filter(task => task.status !== 'выполнена');
  } catch (error) {
    console.error('[loadData] Ошибка:', error.response?.data || error.message);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await loadData();
  await nextTick();

  const { useSortable } = await import('@vueuse/integrations/useSortable');
  useSortable(incompleteEl, incomplete, {
    group: 'tasks',
    animation: 150,
    onEnd: (event) => handleDragEnd(event, 'выполняется'),
  });
  useSortable(completedEl, completed, {
    group: 'tasks',
    animation: 150,
    onEnd: (event) => handleDragEnd(event, 'выполнена'),
  });
});

const handleDragEnd = async (event, targetStatus) => {
  const { oldIndex, newIndex, from, to } = event;

  const sourceList = from === incompleteEl.value ? incomplete : completed;
  const targetList = to === incompleteEl.value ? incomplete : completed;
  const movedTask = sourceList.value[oldIndex];

  if (!movedTask) {
    return;
  }

  const actualTargetStatus = to === incompleteEl.value ? 'выполняется' : 'выполнена';
  
  if (movedTask.status === actualTargetStatus) {
    return;
  }

  try {
    const response = await axios.put(
      `http://localhost:8000/tasks/${movedTask.id}/status`,
      { status: actualTargetStatus },
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      }
    );

    store.commit('setProjectTasks', store.state.projectTasks.items.map(task =>
      task.id === movedTask.id ? { ...task, status: actualTargetStatus } : task
    ));

    const items = store.state.projectTasks.items;
    completed.value = items.filter(task => task.status === 'выполнена');
    incomplete.value = items.filter(task => task.status !== 'выполнена');
  } catch (error) {
    await loadData();
  }
};

const selectItem = (item, event) => {
  if (event.target.draggable) return;
  store.commit('selectTask', item);
  router.push(`/tasks/${item.id}`);
};

const formatDeadline = (deadline) =>
  deadline ? new Date(deadline).toLocaleDateString('ru-RU') : 'N/A';

const formatAssignee = (task) =>
  task.employee_surname && task.employee_name
    ? `${task.employee_surname} ${task.employee_name}`
    : 'N/A';

const hasTasks = computed(() => completed.value.length > 0 || incomplete.value.length > 0);
</script>

<template>
  <div class="record-kanban">
    <h3 class="record-kanban__title">{{ title }}</h3>

    <div v-if="isLoading" class="loading">Загрузка...</div>
    <div v-else-if="!hasTasks" class="no-tasks">Нет задач для этого проекта</div>
    <div v-else class="kanban-board">
      <div class="kanban-column">
        <h4 class="kanban-column__title">Незавершённые ({{ incomplete.length }})</h4>
        <div ref="incompleteEl" class="kanban-column__list">
          <div
            v-for="task in incomplete"
            :key="task.id"
            class="kanban-card"
            :class="{ 'incomplete-task': task.status !== 'выполнена' }"
            draggable="true"
            @click="selectItem(task, $event)"
          >
            <p class="kanban-card__id">Задача №{{ task.id }}</p>
            <p class="kanban-card__description">{{ task.description || 'Без описания' }}</p>
            <p class="kanban-card__assignee">Исполнитель: {{ formatAssignee(task) }}</p>
            <p class="kanban-card__deadline">Дедлайн: {{ formatDeadline(task.deadline) }}</p>
            <p class="kanban-card__status">Статус: {{ task.status }}</p>
          </div>
        </div>
      </div>

      <div class="kanban-column">
        <h4 class="kanban-column__title">Завершённые ({{ completed.length }})</h4>
        <div ref="completedEl" class="kanban-column__list">
          <div
            v-for="task in completed"
            :key="task.id"
            class="kanban-card"
            :class="{ 'completed-task': task.status === 'выполнена' }"
            draggable="true"
            @click="selectItem(task, $event)"
          >
            <p class="kanban-card__id">Задача №{{ task.id }}</p>
            <p class="kanban-card__description">{{ task.description || 'Без описания' }}</p>
            <p class="kanban-card__assignee">Исполнитель: {{ formatAssignee(task) }}</p>
            <p class="kanban-card__deadline">Дедлайн: {{ formatDeadline(task.deadline) }}</p>
            <p class="kanban-card__status">Статус: {{ task.status }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.record-kanban {
  padding: 20px;
}
.record-kanban__title {
  font-size: 24px;
  margin-bottom: 20px;
}
.kanban-board {
  display: flex;
  gap: 20px;
}
.kanban-column {
  flex: 1;
  background: #f4f5f7;
  border-radius: 8px;
  padding: 10px;
  min-height: 400px;
}
.kanban-column__title {
  font-size: 18px;
  margin-bottom: 10px;
  text-align: center;
}
.kanban-column__list {
  min-height: 300px;
}
.kanban-card {
  background: white;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: move;
  transition: background 0.2s;
  border: 2px solid transparent;
}
.kanban-card:hover {
  background: #f9f9f9;
}
.incomplete-task {
  border: 2px solid #0059AC;
}
.completed-task {
  border: 2px solid transparent;
  background-image: linear-gradient(white, white), linear-gradient(rgba(8, 166, 82, 1) 0%, rgba(68, 231, 32, 1) 64%, rgba(33, 186, 114, 1) 100%);
  background-clip: padding-box, border-box;
}
.kanban-card__id {
  font-weight: bold;
  font-size: 16px;
}
.kanban-card__description {
  margin: 5px 0;
  font-size: 14px;
  color: #333;
}
.kanban-card__assignee,
.kanban-card__deadline,
.kanban-card__status {
  font-size: 12px;
  color: #666;
}
.loading,
.no-tasks {
  text-align: center;
  font-size: 16px;
  padding: 20px;
}
</style>