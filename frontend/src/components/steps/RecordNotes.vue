<script>
export default {
  name: "RecordNotes",
  data() {
    return {
      headers: ["Номер собрания", "Дата собрания", "Длительность"],
      items: [
        {id: "Собрание №12398", date: "01.01.2025", duration: "58:32"},
        {id: "Собрание №12748", date: "02.01.2025", duration: "08:11"},
        {id: "Собрание №12398", date: "03.01.2025", duration: "60:00"},
      ]
    }
  }
}
</script>

<template>
  <div class="record-notes">
    <h3 class="record-notes__title">Записи собраний</h3>
    <div class="record-notes__content">
      <div class="record-notes__header">
        <p
            v-for="(header, index) in headers"
            :key="index"
            class="record-notes__header-item">
          {{ header }}
        </p>
      </div>
      <div class="record-notes__list">
        <div
            v-for="(item, index) in items"
            :key="index"
            class="record-notes__item">

          <p v-for="(value, idx) in item"
             :key="idx"
              class="record-notes__item-text">
            {{ value }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>