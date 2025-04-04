<template>
    <div class="form">
        <div class="form__container">
            <h2 class="form__title">Вход в систему</h2>

            <div class="form__container--gap">
                <form class="form__element" @submit.prevent="login">
                    <div class="form__fields">
                        <div class="form__field">
                            <h3 class="form__field-title">Email</h3>
                            <input class="form__input" type="email"/>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Пароль</h3>
                            <input class="form__input" type="password"/>
                        </div>
                    </div>

                    <button class="form__submit" type="submit">Войти</button>
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
<script setup lang="ts">
</script>