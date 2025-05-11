<script setup>
import { computed, ref, watch } from "vue";
import { validateForm } from "../../../assets/validation.js";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

const formData = ref({
    email: '',
    password: '',
    passwordConfirm: '',
});

const errors = ref({
    email: '',
    password: '',
    passwordConfirm: '',
    general: '',
});

const successMessage = ref('');

const fieldsConfig = {
    email: { required: true, isEmail: true, label: "Email" },
    password: { required: true, minLength: 8, label: "Пароль" },
    passwordConfirm: { required: true, matchWith: 'password', label: "Подтверждение пароля" },
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

const resetPassword = async () => {
    validatesForm();
    isFormSubmit.value = true;

    if (hasError.value) {
        return;
    }

    try {
        const response = await axios.post("http://localhost:8000/password/reset", {
            email: formData.value.email,
            password: formData.value.password,
            password_confirm: formData.value.passwordConfirm,
        });
        successMessage.value = response.data.message;
        errors.value.general = '';
        formData.value = { email: '', password: '', passwordConfirm: '' };
        isFormSubmit.value = false;
        setTimeout(() => router.push("/login"), 2000);
    } catch (error) {
        console.error("Ошибка сброса пароля:", error);
        errors.value.general = error.response?.data?.detail || "Ошибка сброса пароля";
        successMessage.value = '';
    }
};
</script>

<template>
    <div class="form">
        <div class="form__container">
            <h2 class="form__title">Восстановление пароля</h2>

            <div class="form__container--gap">
                <form class="form__element" @submit.prevent="resetPassword">
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
                        <div class="form__field">
                            <h3 class="form__field-title">Подтверждение пароля</h3>
                            <input class="form__input" :class="{'form__input--error': errors.passwordConfirm}" type="password" v-model="formData.passwordConfirm"/>
                            <p class="form__error" v-if="errors.passwordConfirm">{{ errors.passwordConfirm }}</p>
                        </div>
                    </div>

                    <p class="form__error" v-if="errors.general">{{ errors.general }}</p>
                    <p class="form__success" v-if="successMessage">{{ successMessage }}</p>

                    <button class="form__submit"
                            type="submit"
                            :class="{'form__submit--error': hasError}"
                            :disabled="hasError">
                        Изменить пароль
                    </button>
                </form>

                <p class="form__text">
                    <router-link class="form__link" to="/login">Вернуться к авторизации</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.form__success {
    color: green;
    font-size: 14px;
    margin-top: 10px;
}
</style>