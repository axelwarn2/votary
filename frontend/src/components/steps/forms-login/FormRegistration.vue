<template>
    <div class="form">
        <div class="form__container">
            <h2 class="form__title">Регистрация</h2>

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

                        <div class="form__field">
                            <h3 class="form__field-title">Пароль</h3>
                            <input class="form__input" type="password"/>
                        </div>

                        <div class="form__field">
                            <h3 class="form__field-title">Подтверждение пароля</h3>
                            <input class="form__input" type="password"/>
                        </div>
                    </div>

                    <button class="form__submit" type="submit">Зарегистрироваться</button>
                </form>

                <p class="form__text">
                    Уже есть аккаунт?
                    <router-link class="form__link" to="/login">Войдите в него</router-link>
                </p>
            </div>
        </div>
    </div>
</template>
