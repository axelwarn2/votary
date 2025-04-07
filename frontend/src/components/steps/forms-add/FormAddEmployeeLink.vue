<script setup>
import { computed, ref, watch } from "vue";
import { validateForm } from "../../../assets/validation.js";

const formData = ref({
    companyName: '',
    email: '',
});

const errors = ref({
    companyName: '',
    email: '',
});

const fieldsConfig = {
    companyName: { required: true, label: "Наименование компании" },
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

const submitLink = () => {
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
                <form class="form__element" @submit.prevent="submitLink">
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
                    </div>

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
