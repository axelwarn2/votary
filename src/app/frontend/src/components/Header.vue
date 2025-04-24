<script>
export default {
    name: 'Header',
    methods: {
        goToLogin() {
            this.$router.push('/login');
        },
        goToRegister() {
            this.$router.push('/registration');
        },
    },
};
</script>

<template>
    <header class="app-header">
        <div class="header-actions">
            <button class="header-button" @click="goToLogin">Вход</button>
            <button class="header-button header-button--register" @click="goToRegister">Регистрация</button>
        </div>
    </header>
</template>

<style scoped>
.app-header {
    display: flex;
    justify-content: flex-end;
    padding: 10px 20px;
}

.header-actions {
    display: flex;
    gap: 10px;
}

.header-button {
    padding: 8px 16px;
    background-color: #0059AC;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.header-button--register {
    background-color: #0059AC;
}
</style>
