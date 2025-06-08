<script setup>
import { computed, ref, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { validateForm } from '../../../assets/validation.js';

const route = useRoute();
const router = useRouter();
const projectId = computed(() => route.params.id); // ID проекта для редактирования
const isEditMode = computed(() => !!projectId.value); // Режим редактирования

const formData = ref({
  name: '',
  description: '',
});

const errors = ref({
  name: '',
  description: '',
});

const fieldsConfig = {
  name: { required: true, maxLength: 100, label: 'Название' },
  description: { required: false, maxLength: 1000, label: 'Описание' },
};

const isFormSubmit = ref(false);

const validatesForm = () => {
  errors.value = validateForm(formData.value, fieldsConfig);
};

watch(formData, () => {
  if (isFormSubmit.value) validatesForm();
}, { deep: true });

const hasError = computed(() => {
  return Object.values(errors.value).some(error => error !== '');
});

// Загрузка данных проекта для редактирования
const loadProject = async () => {
  if (!isEditMode.value) return;
  try {
    const response = await axios.get(`http://localhost:8000/projects/${projectId.value}`);
    formData.value = {
      name: response.data.name,
      description: response.data.description || '',
    };
  } catch (error) {
    console.error('Ошибка загрузки проекта:', error);
    errors.value = { name: 'Не удалось загрузить проект' };
  }
};

onMounted(loadProject);

// Создание или обновление проекта
const submitProject = async () => {
  validatesForm();
  isFormSubmit.value = true;

  if (hasError.value) return;

  try {
    let response;
    if (isEditMode.value) {
      response = await axios.put(`http://localhost:8000/projects/${projectId.value}`, {
        name: formData.value.name,
        description: formData.value.description || null,
      });
    } else {
      response = await axios.post('http://localhost:8000/project', {
        name: formData.value.name,
        description: formData.value.description || null,
      });
    }

    formData.value = { name: '', description: '' };
    isFormSubmit.value = false;
    router.push('/projects'); // Редирект на список проектов
  } catch (error) {
    console.error(`Ошибка при ${isEditMode.value ? 'обновлении' : 'создании'} проекта:`, error);
    errors.value = {
      name: error.response?.data?.detail || `Ошибка ${isEditMode.value ? 'обновления' : 'создания'} проекта`,
    };
  }
};
</script>

<template>
  <div class="form">
    <div class="form__container">
      <h2 class="form__title">{{ isEditMode ? 'Редактирование проекта' : 'Создание проекта' }}</h2>
      <div class="form__container--gap">
        <form class="form__element" @submit.prevent="submitProject">
          <div class="form__fields">
            <div class="form__field">
              <h3 class="form__field-title">Название</h3>
              <input
                class="form__input"
                :class="{ 'form__input--error': errors.name }"
                type="text"
                v-model="formData.name"
                placeholder="Введите название проекта"
              />
              <p class="form__error" v-if="errors.name">{{ errors.name }}</p>
            </div>
            <div class="form__field">
              <h3 class="form__field-title">Описание</h3>
              <textarea
                class="form__input form__input--textarea"
                :class="{ 'form__input--error': errors.description }"
                v-model="formData.description"
                placeholder="Введите описание проекта (опционально)"
              ></textarea>
              <p class="form__error" v-if="errors.description">{{ errors.description }}</p>
            </div>
          </div>
          <button
            class="form__submit"
            type="submit"
            :class="{ 'form__submit--error': hasError }"
            :disabled="hasError"
          >
            {{ isEditMode ? 'Сохранить изменения' : 'Создать проект' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
