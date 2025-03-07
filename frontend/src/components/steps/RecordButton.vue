<script>
export default {
  name: "RecordButton",
  data() {
    return {
      isRecording: false
    }
  },
  methods: {
    toogleMicro() {
      this.isRecording = !this.isRecording;
    }
  }
}
</script>

<template>
  <div class="record-button">
    <button class="record-button__button"
            :class="{'record-button__button--off' : !isRecording, 'record-button__button--on' : isRecording}"
            @click="toogleMicro">
      <div class="record-button__icon--off"
            :class="{'record-button__icon--on' : isRecording}">
      </div>
    </button>

    <p class="record-button__status">{{ isRecording ? "Микрофон включен" : "Микрофон выключен" }}</p>
  </div>
</template>
