<script>

import RecordButton from "./steps/RecordButton.vue";
import RecordLists from "./steps/RecordLists.vue";
import RecordNotesDetail from "./steps/RecordNotesDetail.vue";
import RecordTasksDetail from "./steps/RecordTasksDetail.vue";
import RecordStatisticDetail from "./steps/RecordStatisticDetail.vue";
import { mapState } from "vuex";

export default {
    name: "AppointmentMain",
    components: { RecordButton, RecordLists, RecordNotesDetail, RecordTasksDetail, RecordStatisticDetail },
    computed: {
        ...mapState(["currentView", "notesData", "taskData", "statisticsData"]),
        currentItems() {
            if (this.currentView === "RecordNotes") return this.notesData.items;
            if (this.currentView === "RecordTasks") return this.taskData.items;
            if (this.currentView === "RecordStatistics") return this.statisticsData.items;
            return [];
        },
        isTasks() {
            return this.currentView === "RecordTasks";
        },
        isStatistics() {
            return this.currentView === "RecordStatistics";
        }
    }
}
</script>

<template>
    <div class="votary-content" :class="{'scroll' : currentView === 'RecordStatisticDetail'}">
        <RecordButton v-if="currentView === 'RecordButton'"/>
        <RecordLists
            v-if="currentView === 'RecordNotes' || currentView === 'RecordTasks' || currentView === 'RecordStatistics'"
            :items="currentItems"
            :isTasks="isTasks"
            :isStatistics="isStatistics"
        />
        <RecordNotesDetail v-if="currentView === 'RecordNotesDetail'"/>
        <RecordTasksDetail v-if="currentView === 'RecordTasksDetail'"/>
        <RecordStatisticDetail v-if="currentView === 'RecordStatisticDetail'"/>
    </div>
</template>
