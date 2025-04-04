<script>
import LeftBorder from "./components/LeftBorder.vue";
import Header from "./components/Header.vue";

export default {
    components: {
        Header,
        LeftBorder,
    },
}
</script>

<template>
    <div class="votary-app">
        <LeftBorder/>

        <main class="votary-main">
            <Header />
            <router-view/>
        </main>
    </div>
</template>
