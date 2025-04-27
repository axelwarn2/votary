<script setup>
import { computed, ref, watch } from "vue";
import axios from "axios";
import { validateForm } from "../../../assets/validation.js";

const formData = ref({
    email: '',
    surname: '',
    name: '',
    lastname: '',
});

const errors = ref({
    email: '',
    surname: '',
    name: '',
    lastname: '',
});

const fieldsConfig = {
    email: { required: true, isEmail: true, label: "Email" },
    surname: { required: true, minLength: 2, maxLength: 35, label: "Фамилия" },
    name: { required: true, minLength: 2, maxLength: 35, label: "Имя" },
    lastname: { required: true, minLength: 2, maxLength: 35, label: "Отчество" },
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

const addEmployee = async () => {
    validatesForm();
    isFormSubmit.value = true;

    if (hasError.value) {
        return;
    }

    try {
        const response = await axios.post("http://localhost:8000/employee/", {
            surname: formData.value.surname,
            name: formData.value.name,
            lastname: formData.value.lastname,
            email: formData.value.email,
            password: "qwerty123!",
            role: "исполнитель"
        });

        formData.value = {
            email: '',
            lastname: '',
            name: '',
            patronymic: '',
        };
        isFormSubmit.value = false;

    } catch (error) {
        console.error("Ошибка при добавлении сотрудника:", error);
        alert("Ошибка при добавлении сотрудника!");
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
                            <input class="form__input" :class="{'form__input--error': errors.surname}" type="text" v-model="formData.surname"/>
                            <p class="form__error" v-if="errors.surname">{{ errors.surname }}</p>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Имя</h3>
                            <input class="form__input" :class="{'form__input--error': errors.name}" type="text" v-model="formData.name"/>
                            <p class="form__error" v-if="errors.name">{{ errors.name }}</p>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Отчество</h3>
                            <input class="form__input" :class="{'form__input--error': errors.patronymic}" type="text" v-model="formData.lastname"/>
                            <p class="form__error" v-if="errors.lastname">{{ errors.lastname }}</p>
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
