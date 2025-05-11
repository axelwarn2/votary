<script setup>
import { computed, ref, watch } from "vue";
import axios from "axios";
import { validateForm } from "../../../assets/validation.js";

const formData = ref({
    email: '',
});

const errors = ref({
    email: '',
    general: '',
});

const fieldsConfig = {
    email: { required: true, isEmail: true, label: "Email" },
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

const submitLink = async () => {
    validatesForm();
    isFormSubmit.value = true;

    if (hasError.value) {
        return;
    }

    try {
        await axios.post("http://localhost:8000/invitation", {
            email: formData.value.email,
        }, {
            headers: { "Cookie": `session_id=${document.cookie.split('session_id=')[1]?.split(';')[0]}` }
        });
        formData.value.email = '';
        isFormSubmit.value = false;
        errors.value.general = "Приглашение успешно отправлено!";
    } catch (error) {
        console.error("Ошибка при отправке приглашения:", error);
        errors.value.general = error.response?.data?.detail || "Ошибка отправки приглашения";
    }
};
</script>

<template>
    <div class="form">
        <div class="form__container">
            <h2 class="form__title">Добавление сотрудника</h2>

            <div class="form__container--gap">
                <form class="form__element" @submit.prevent="submitLink">
                    <div class="form__fields">
                        <div class="form__field">
                            <h3 class="form__field-title">Email</h3>
                            <input class="form__input" :class="{'form__input--error': errors.email}" type="email" v-model="formData.email"/>
                            <p class="form__error" v-if="errors.email">{{ errors.email }}</p>
                        </div>
                    </div>

                    <p class="form__error" v-if="errors.general && errors.general.includes('Ошибка')">{{ errors.general }}</p>
                    <p class="form__success" v-else-if="errors.general">{{ errors.general }}</p>

                    <button class="form__submit"
                            type="submit"
                            :class="{'form__submit--error': hasError}"
                            :disabled="hasError">
                        Отправить приглашение
                    </button>
                </form>

                <p class="form__text">
                    Не пришло сообщение?
                    <router-link class="form__link" to="/add-employee">Добавить вручную</router-link>
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
