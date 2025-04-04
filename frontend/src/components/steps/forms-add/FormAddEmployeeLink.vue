<template>
    <div class="form">
        <div class="form__container">
            <h2 class="form__title">Добавление сотрудника</h2>

            <div class="form__container--gap">
                <form class="form__element" @submit.prevent="register">
                    <div class="form__fields">
                        <div class="form__field">
                            <h3 class="form__field-title">Наименование компании</h3>
                            <input class="form__input" type="text"/>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Email</h3>
                            <input class="form__input" type="email"/>
                        </div>
                    </div>

                    <button class="form__submit" type="submit">Отправить приглашение</button>
                </form>

                <p class="form__text">
                    Не пришло сообщение?
                    <router-link class="form__link" to="/add-employee">Добавить вручную</router-link>
                </p>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
</script>