<template>
    <div class="form">
        <div class="form__container">
            <h2 class="form__title">Добавление сотрудника</h2>

            <div class="form__container--gap">
                <form class="form__element" @submit.prevent="register">
                    <div class="form__fields">
                        <div class="form__field">
                            <h3 class="form__field-title">Email</h3>
                            <input class="form__input" type="email"/>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Фамилия</h3>
                            <input class="form__input" type="text"/>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Имя</h3>
                            <input class="form__input" type="text"/>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Отчество</h3>
                            <input class="form__input" type="text"/>
                        </div>
                    </div>

                    <button class="form__submit" type="submit">Добавить сотрудника</button>
                </form>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
</script>