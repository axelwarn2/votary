<script>
import {mapState, mapMutations} from 'vuex';

export default {
    name: 'RecordLists',
    props: {
        isTasks: Boolean,
        isStatistics: Boolean,
    },
    computed: {
        ...mapState(['notesData', 'taskData', 'statisticsData']),
        headers() {
            if (this.isTasks) return this.taskData.headers;
            if (this.isStatistics) return this.statisticsData.headers;
            return this.notesData.headers;
        },
        title() {
            if (this.isTasks) return this.taskData.title;
            if (this.isStatistics) return this.statisticsData.title;
            return this.notesData.title;
        },
        items() {
            if (this.isTasks) return this.taskData.items;
            if (this.isStatistics) return this.statisticsData.items;
            return this.notesData.items;
        },
    },
    methods: {
        ...mapMutations(['selectNote', 'selectTask', 'selectStatistic']),
        selectItem(item) {
            if (this.isTasks) {
                this.selectTask(item);
                this.$router.push(`/tasks/${item.id}`);
            } else if (this.isStatistics) {
                this.selectStatistic(item);
                this.$router.push(`/statistics/${item.id}`);
            } else {
                this.selectNote(item);
                this.$router.push(`/meetings/${item.id}`);
            }
        },
        getItemValues(item) {
            if (this.isStatistics) {
                return [item.employee, item.count_task, item.complete, item.expired, item.efficiency];
            } else if (this.isTasks) {
                return [item.id, item.name, item.create, item.deadline];
            } else {
                return [item.id, item.date, item.duration];
            }
        },
    },
};
</script>

<template>
    <div class="record-notes">
        <h3 class="record-notes__title">{{ title }}</h3>
        <div class="record-notes__content">
            <div class="record-notes__header">
                <p
                        v-for="(header, index) in headers"
                        :key="index"
                        class="record-notes__header-item"
                >
                    {{ header }}
                </p>
            </div>
            <div class="record-notes__list">
                <div
                        v-for="(item, index) in items"
                        :key="index"
                        class="record-notes__item"
                        @click="selectItem(item)"
                >
                    <p
                            v-for="(value, index) in getItemValues(item)"
                            :key="index"
                            class="record-notes__item-text"
                    >
                        {{ value }}
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>