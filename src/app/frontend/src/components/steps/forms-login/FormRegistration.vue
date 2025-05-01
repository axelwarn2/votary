<script setup>
import { computed, ref, watch } from "vue";
import { validateForm } from "../../../assets/validation.js";
import axios from "axios";

const formData = ref({
    email: '',
    surname: '',
    name: '',
    lastname: '',
    password: '',
    passwordConfirm: '',
});

const errors = ref({
    email: '',
    surname: '',
    name: '',
    lastname: '',
    password: '',
    passwordConfirm: '',
});

const fieldsConfig = {
    email: { required: true, isEmail: true, label: "Email" },
    surname: { required: true, minLength: 2, maxLength: 35, label: "Фамилия" },
    name: { required: true, minLength: 2, maxLength: 35, label: "Имя" },
    lastname: { required: true, minLength: 2, maxLength: 35, label: "Отчество" },
    password: { required: true,  minLength: 8, label: "Пароль" },
    passwordConfirm: { required: true, matchWith: 'password', label: "Подтверждение пароля"},
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

const register = async () => {
    validatesForm();
    isFormSubmit.value = true;

    if (hasError.value) {
        return;
    }

    try {
        const response = await axios.post("http://localhost:8000/employee", {
            surname: formData.value.surname,
            name: formData.value.name,
            lastname: formData.value.lastname,
            email: formData.value.email,
            password: formData.value.password,
            role: "руководитель",
        });

        formData.value = {
            email: '',
            surname: '',
            name: '',
            lastname: '',
            password: '',
            passwordConfirm: '',
        };
        isFormSubmit.value = false;

    } catch (error) {
        console.error("Ошибка при регистрации: " + error);
    }
};
</script>

<template>
    <div class="form">
        <div class="form__container">
            <h2 class="form__title">Регистрация</h2>

            <div class="form__container--gap">
                <form class="form__element" @submit.prevent="register">
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
                            <input class="form__input" :class="{'form__input--error': errors.lastname}" type="text" v-model="formData.lastname"/>
                            <p class="form__error" v-if="errors.lastname">{{ errors.lastname }}</p>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Пароль</h3>
                            <input class="form__input" :class="{'form__input--error': errors.password}" type="password" v-model="formData.password"/>
                            <p class="form__error" v-if="errors.password">{{ errors.password }}</p>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Подтверждение пароля</h3>
                            <input class="form__input" :class="{'form__input--error': errors.passwordConfirm}" type="password" v-model="formData.passwordConfirm"/>
                            <p class="form__error" v-if="errors.passwordConfirm">{{ errors.passwordConfirm }}</p>
                        </div>
                    </div>

                    <button class="form__submit"
                            type="submit"
                            :class="{'form__submit--error': hasError}"
                            :disabled="hasError">
                        Зарегистрироваться
                    </button>
                </form>

                <p class="form__text">
                    Уже есть аккаунт?
                    <router-link class="form__link" to="/login">Войдите в него</router-link>
                </p>
            </div>
        </div>
    </div>
</template>
