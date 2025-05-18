<script setup>
import { onMounted, computed } from "vue";
import LeftBorder from "./components/LeftBorder.vue";
import Header from "./components/Header.vue";
import { useStore } from 'vuex';

const store = useStore();
const user = computed(() => store.state.user);

onMounted(() => {
    store.dispatch('fetchUser');
});
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
        border: 2px solid #000000;
        padding: 60px 40px;
        box-shadow: 3px 3px 4px #000000;
    }

    .access__title {
        font-size: 44px;
        background: linear-gradient(0.25turn, #000000, #343434, #131212);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .access__description {
        font-size: 20px;
        background: linear-gradient(0.25turn, #000000, #343434, #131212);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
