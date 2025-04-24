<script setup>
import { computed, ref, watch } from "vue";
import { validateForm } from "../../../assets/validation.js";

const formData = ref({
    email: '',
});

const errors = ref({
    email: '',
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

const recover = () => {
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
            <h2 class="form__title">Восстановление пароля</h2>

            <div class="form__container--gap">
                <form class="form__element" @submit.prevent="recover">
                    <div class="form__fields">
                        <div class="form__field">
                            <h3 class="form__field-title">Email</h3>
                            <input class="form__input" :class="{'form__input--error': errors.email}" type="email" v-model="formData.email"/>
                            <p class="form__error" v-if="errors.email">{{ errors.email }}</p>
                        </div>
                    </div>

                    <button class="form__submit"
                            type="submit"
                            :class="{'form__submit--error': hasError}"
                            :disabled="hasError">
                        Продолжить
                    </button>
                </form>

                <p class="form__text">
                    <router-link class="form__link" to="/login">Вернуться к авторизации</router-link>
                </p>
            </div>
        </div>
    </div>
</template>
