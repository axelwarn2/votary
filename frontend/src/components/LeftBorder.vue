<script>
import { mapState } from "vuex";

export default {
    name: "AppointmentMain",
    computed: {
        ...mapState(["currentView", "notesData", "taskData", "statisticsData"]),
    }
}
</script>

<template>
    <div class="left-border">
        <div class="logo" @click="$store.commit('resetToHome')">
            <div class="logo__image"></div>
            <h1 class="logo__title">Votary</h1>
        </div>

        <div class="left-panel">
            <ul class="left-panel__list">
                <li class="left-panel__item" @click="$store.dispatch('showMeetings')" :class="{'isActive' : currentView === 'RecordNotes'}">
                    <div class="left-panel__item-image--record"></div>
                    <button class="left-panel__item-text">Записи собраний</button>
                </li>
                <li class="left-panel__item" @click="$store.dispatch('showTasks')" :class="{'isActive' : currentView === 'RecordTasks'}">
                    <div class="left-panel__item-image--note"></div>
                    <button class="left-panel__item-text">Задачи</button>
                </li>
                <li class="left-panel__item" @click="$store.dispatch('showStatistics')" :class="{'isActive' : currentView === 'RecordStatistics'}">
                    <div class="left-panel__item-image--graphic"></div>
                    <button class="left-panel__item-text">Статистика задач</button>
                </li>
            </ul>
        </div>
    </div>
</template>
