<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const meeting = ref([]);
onMounted(async () => {
    try {
        const response = await axios.get(`http://localhost:8000/meetings/${route.params.id}`);
        meeting.value = response.data;
        console.log(meeting.value)
    } catch (error) {
        console.error('Ошибка получения детальной информации собрания:', error);
    }
});
</script>

<template>
    <div class="record-notes-detail">
        <h3 class="record-notes-detail__title">Собрание №{{ meeting.id }}</h3>
        <div class="record-notes-detail__content">
            <div class="record-notes-detail__section record-notes-detail__section--key-points">
                <p class="record-notes-detail__section-title">Ключевые моменты</p>
            </div>

            <div class="record-notes-detail__section record-notes-detail__section--text">
                <p class="record-notes-detail__text">
                    {{ meeting.text }}
                </p>
            </div>

            <div class="record-notes-detail__section record-notes-detail__section--download">
                <p class="record-notes-detail__download-text">
                    Скачать полную запись: <a href="#" class="record-notes-detail__link">Ссылка</a>
                </p>
            </div>
        </div>
    </div>
</template>
