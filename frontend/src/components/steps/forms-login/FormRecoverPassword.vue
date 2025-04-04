<template>
    <div class="form">
        <div class="form__container">
            <h2 class="form__title">Восстановление пароля</h2>

            <div class="form__container--gap">
                <form class="form__element" @submit.prevent="login">
                    <div class="form__fields">
                        <div class="form__field">
                            <h3 class="form__field-title">Email</h3>
                            <input class="form__input" type="email"/>
                        </div>
                    </div>

                    <button class="form__submit" type="submit">Продолжить</button>
                </form>

                <p class="form__text">
                    <router-link class="form__link" to="/login">Вернуться к авторизации</router-link>
                </p>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
</script>