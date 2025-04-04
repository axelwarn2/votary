<script setup>
import { computed, ref } from "vue";
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
    companyName: { required: true },
    email: { required: true, isEmail: true },
    password: { required: true,  minLength: 8 },
    passwordConfirm: { required: true, matchWith: 'password'},
}

const validatesForm = () => {
  errors.value = validateForm(formData.value, fieldsConfig);
};

const hasError = computed(() => {
    return Object.values(errors.value).some(error => error !== '');
})

const register = () => {
    validatesForm();
    if (hasError.value) {
        return;
    }

    console.log('Form submitted:', formData.value);
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
                            <input class="form__input" :class="{'form__input--error': errors.companyName }"
                                   type="text"/>
                            <p class="form__error" v-if="errors.companyName">{{ errors.companyName }}</p>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Email</h3>
                            <input class="form__input" :class="{'form__input--error': errors.email }" type="email"/>
                            <p class="form__error" v-if="errors.email">{{ errors.email }}</p>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Пароль</h3>
                            <input class="form__input" :class="{'form__input--error': errors.password }"
                                   type="password"/>
                            <p class="form__error" v-if="errors.password">{{ errors.password }}</p>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Подтверждение пароля</h3>
                            <input class="form__input" :class="{'form__input--error': errors.passwordConfirm }"
                                   type="password"/>
                            <p class="form__error" v-if="errors.passwordConfirm">{{ errors.passwordConfirm }}</p>
                        </div>
                    </div>

                    <button class="form__submit" type="submit" :class="{'form__submit--error': hasError}" :disabled="hasError">Зарегистрироваться</button>
                </form>

                <p class="form__text">
                    Уже есть аккаунт?
                    <router-link class="form__link" to="/login">Войдите в него</router-link>
                </p>
            </div>
        </div>
    </div>
</template>
