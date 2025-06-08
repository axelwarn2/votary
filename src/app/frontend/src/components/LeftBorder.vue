<script>
export default {
    name: "LeftBorder",
    methods: {
        goToHome() {
            this.$router.push('/record');
        },
        goToMeetings() {
            this.$router.push('/meetings');
        },
        goToTasks() {
            this.$router.push('/tasks');
        },
        goToStatistics() {
            this.$router.push('/statistics');
        },
        goToProjects() {
            this.$router.push('/projects');
        },
    },
    computed: {
        currentRoute() {
            return this.$route.name;
        },
    },
}
</script>

<template>
    <div class="left-border">
        <div class="logo" @click="goToHome">
            <div class="logo__image"><img src="../assets/images/logo.svg" alt=""></div>
            <h1 class="logo__title">Votary</h1>
        </div>

        <div class="left-panel">
            <ul class="left-panel__list">
                <li class="left-panel__item" @click="goToMeetings"
                    :class="{'isActive' : currentRoute === 'RecordNotes'}">
                    <div class="left-panel__item-image--record"></div>
                    <button class="left-panel__item-text">Записи собраний</button>
                </li>
                <li class="left-panel__item" @click="goToTasks" :class="{'isActive' : currentRoute === 'RecordTasks'}">
                    <div class="left-panel__item-image--note"></div>
                    <button class="left-panel__item-text">Поручения</button>
                </li>
                <li class="left-panel__item" @click="goToStatistics"
                    :class="{'isActive' : currentRoute === 'RecordStatistics'}">
                    <div class="left-panel__item-image--graphic"></div>
                    <button class="left-panel__item-text">Статистика задач</button>
                </li>
                <li class="left-panel__item" @click="goToProjects"
                    :class="{'isActive' : currentRoute === 'RecordProjects'}">
                    <div class="left-panel__item-image--graphic"></div>
                    <button class="left-panel__item-text">Проекты</button>
                </li>
            </ul>
        </div>
    </div>
</template>
