<script setup>
import { computed, ref, watch } from "vue";
import { validateForm } from "../../../assets/validation.js";

const formData = ref({
    companyName: '',
    email: '',
    password: '',
    passwordConfirm: '',
});

const errors = ref({
    companyName: '',
    email: '',
    password: '',
    passwordConfirm: '',
});

const fieldsConfig = {
    companyName: { required: true, label: "Наименование компании" },
    email: { required: true, isEmail: true, label: "Email" },
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

const register = () => {
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
            <h2 class="form__title">Регистрация</h2>

            <div class="form__container--gap">
                <form class="form__element" @submit.prevent="register">
                    <div class="form__fields">
                        <div class="form__field">
                            <h3 class="form__field-title">Наименование компании</h3>
                            <input class="form__input" :class="{'form__input--error': errors.companyName}" type="text" v-model="formData.companyName"/>
                            <p class="form__error" v-if="errors.companyName">{{ errors.companyName }}</p>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Email</h3>
                            <input class="form__input" :class="{'form__input--error': errors.email}" type="email" v-model="formData.email"/>
                            <p class="form__error" v-if="errors.email">{{ errors.email }}</p>
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
