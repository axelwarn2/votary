<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from 'vuex';

const router = useRouter();
const store = useStore();
const isDropdownOpen = ref(false);

const user = computed(() => store.state.user);

const name = computed(() => {
    return `${user.value?.surname} ${user.value?.name}`
})

const toggleDropdown = () => {
    isDropdownOpen.value = !isDropdownOpen.value;
}

const logout = async () => {
    await store.dispatch('logout');
    isDropdownOpen.value = false;
    router.push('/');
}
</script>

<template>
    <header class="app-header">
        <div class="header-actions">
            <template v-if="!user">
                <button class="header-button" @click="$router.push('/login')">Вход</button>
                <button class="header-button header-button--register" @click="$router.push('/registration')">Регистрация</button>
            </template>

            <template v-else>
                <div class="user-container">
                    <span class="user-label" @click="toggleDropdown">{{ name }}</span>
                    <div v-if="isDropdownOpen" class="dropdown">
                        <button class="dropdown-item" @click="logout">Выйти</button>
                    </div>
                </div>
            </template>
        </div>
    </header>
</template>

<style scoped>
.app-header {
    display: flex;
    justify-content: flex-end;
    padding: 10px 20px;
    border-bottom: 1px solid #ccc;
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

.user-container {
    position: relative;
}

.user-label {
    cursor: pointer;
    color: #0059ac;
    font-size: 14px;
    padding: 8px 16px;
}

.dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}

.dropdown-item {
    display: block;
    padding: 8px 16px;
    background: none;
    border: none;
    width: 100%;
    text-align: left;
    cursor: pointer;
    font-size: 14px;
}

.dropdown-item:hover {
    background-color: #f0f0f0;
}
</style>
