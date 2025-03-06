<script>

import LeftBorder from "./components/LeftBorder.vue";
import AppointmentMain from "./components/AppointmentMain.vue";

export default {
   components: {
      LeftBorder,
      AppointmentMain
   },
}
</script>

<template>
  <div class="votary-app">
    <LeftBorder />

    <main class="votary-main">
      <AppointmentMain />
    </main>
  </div>
</template>
