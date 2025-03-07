<script>
import { mapState } from 'vuex';

export default {
    name: "RecordLists",
    props: {
        items: Array,
        isTasks: Boolean,
        isStatistics: Boolean,
    },
    computed: {
        ...mapState(['notesData', 'taskData', "statisticsData"]),
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
    },
    methods: {
        selectItem(item) {
            if (this.isTasks) {
                return this.$store.commit("selectTask", item);
            } else if (!this.isStatistics) {
                return this.$store.commit("selectNote", item);
            } else {
                return this.$store.commit("selectNote", item);
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
        }
    }
}
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