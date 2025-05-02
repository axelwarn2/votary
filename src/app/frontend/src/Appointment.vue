<script setup>
import {onMounted, ref} from "vue";
import LeftBorder from "./components/LeftBorder.vue";
import Header from "./components/Header.vue";
import axios from "axios";

const user = ref(null)

const checkAuth = async () => {
    try {
        const response = await axios.get("http://localhost:8000/me", {
            withCredentials: true
        });
        user.value = response.data;
    } catch (error) {
        console.error("Ошибка получения пользователя", error)
        user.value = null;
    }
}

checkAuth();
</script>

<template>
    <div class="votary-app">
        <LeftBorder v-if="user"/>

        <main class="votary-main">
            <Header />
            <router-view />
            <template v-if="!user && $route.path === '/'">
                <div class="votary-main__access">
                    <div class="access">
                        <h1 class="access__title">Votary</h1>
                        <h3 class="access__description">Войдите или авторизуйтесь для получения всех функций</h3>
                    </div>
                </div>
            </template>
        </main>
    </div>
</template>

<style scoped>
    .votary-main__access {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 90vh;
    }

    .access {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        text-align: center;
        border: 2px solid #FFFFFF;
        padding: 60px 40px;
        box-shadow: 3px 3px 4px #FFFFFF;
    }

    .access__title {
        font-size: 44px;
        background: linear-gradient(0.25turn, #FBFBFB, #C8C8C8, #7C7C7C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .access__description {
        font-size: 20px;
        background: linear-gradient(0.25turn, #7C7C7C, #8E8E8E, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>