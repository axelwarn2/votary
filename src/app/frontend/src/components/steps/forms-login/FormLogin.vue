<script setup>
import { computed, ref, watch } from "vue";
import { validateForm } from "../../../assets/validation.js";

const formData = ref({
    email: '',
    password: '',
});

const errors = ref({
    email: '',
    password: '',
});

const fieldsConfig = {
    email: { required: true, isEmail: true, label: "Email" },
    password: { required: true, minLength: 8, label: "Пароль" },
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
})

const login = () => {
    validatesForm();
    isFormSubmit.value = true;

    if ((hasError.value)) {
        return;
    }
};
</script>

<template>
    <div class="form">
        <div class="form__container">
            <h2 class="form__title">Вход в систему</h2>

            <div class="form__container--gap">
                <form class="form__element" @submit.prevent="login">
                    <div class="form__fields">
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
                    </div>

                    <button class="form__submit"
                            type="submit"
                            :class="{'form__submit--error': hasError}"
                            :disabled="hasError">
                        Войти
                    </button>
                </form>

                <p class="form__text">
                    <router-link class="form__link" to="/recover-password">Забыли пароль?</router-link>
                </p>

                <p class="form__text">
                    Нет аккаунта?
                    <router-link class="form__link" to="/registration">Регистрация</router-link>
                </p>
            </div>
        </div>
    </div>
</template>
