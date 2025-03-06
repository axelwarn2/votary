<script>

import RecordButton from "./steps/RecordButton.vue";
import RecordNotes from "./steps/RecordNotes.vue";
import RecordNotesDetail from "./steps/RecordNotesDetail.vue";
import RecordTasks from "./steps/RecordTasks.vue";

export default {
    name: "AppointmentMain",
    components: {
        RecordButton,
        RecordNotes,
        RecordNotesDetail,
       RecordTasks
    },
}
</script>

<template>
    <div class="votary-content">
      <RecordButton />
<!--      <RecordNotes />-->
<!--      <RecordNotesDetail />-->
<!--      <RecordTasks />-->
    </div>
</template>
