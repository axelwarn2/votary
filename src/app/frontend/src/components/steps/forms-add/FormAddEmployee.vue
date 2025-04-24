<script setup>
import { computed, ref, watch } from "vue";
import { validateForm } from "../../../assets/validation.js";

const formData = ref({
    email: '',
    lastname: '',
    name: '',
    patronymic: '',
});

const errors = ref({
    email: '',
    lastname: '',
    name: '',
    patronymic: '',
});

const fieldsConfig = {
    email: { required: true, isEmail: true, label: "Email" },
    lastname: { required: true, minLength: 2, maxLength: 35, label: "Фамилия" },
    name: { required: true, minLength: 2, maxLength: 35, label: "Имя" },
    patronymic: { required: true, minLength: 2, maxLength: 35, label: "Отчество" },
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

const addEmployee = () => {
    validatesForm();
    isFormSubmit.value = true;

    if (hasError.value) {
        return;
    }
};
</script>

<template>
    <div class="form">
        <div class="form__container">
            <h2 class="form__title">Добавление сотрудника</h2>

            <div class="form__container--gap">
                <form class="form__element" @submit.prevent="addEmployee">
                    <div class="form__fields">
                        <div class="form__field">
                            <h3 class="form__field-title">Email</h3>
                            <input class="form__input" :class="{'form__input--error': errors.email}" type="email" v-model="formData.email"/>
                            <p class="form__error" v-if="errors.email">{{ errors.email }}</p>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Фамилия</h3>
                            <input class="form__input" :class="{'form__input--error': errors.lastname}" type="text" v-model="formData.lastname"/>
                            <p class="form__error" v-if="errors.lastname">{{ errors.lastname }}</p>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Имя</h3>
                            <input class="form__input" :class="{'form__input--error': errors.name}" type="text" v-model="formData.name"/>
                            <p class="form__error" v-if="errors.name">{{ errors.name }}</p>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Отчество</h3>
                            <input class="form__input" :class="{'form__input--error': errors.patronymic}" type="text" v-model="formData.patronymic"/>
                            <p class="form__error" v-if="errors.patronymic">{{ errors.patronymic }}</p>
                        </div>
                    </div>

                    <button class="form__submit"
                            type="submit"
                            :class="{'form__submit--error': hasError}"
                            :disabled="hasError">
                        Добавить сотрудника
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>
