<script>
export default {
    name: "RecordTasks"
}
</script>

<template>
    <div class="record-notes-detail">
        <h3 class="record-notes-detail__title">Реализация фильтрации</h3>
        <div class="record-task">
            <div class="record-notes-detail__content">
                <div class="record-notes-detail__section record-notes-detail__section--key-points">
                    <p class="record-notes-detail__section-title">Задача № 12398 - выполняется</p>
                </div>
                <div class="record-notes-detail__section record-notes-detail__section--text">
                    <p class="record-notes-detail__text">
                        Константин, для тебя задача, чтобы ты прокачал свои навыки. Нам нужно добавить функциональность
                        фильтрации товаров на страницу каталога.
                        Итак, что требуется:
                        Разберись с текущим кодом. Посмотри, как сейчас отображаются товары и как данные приходят с
                        бэкенда.
                        Спроектируй интерфейс фильтров. Нужно что-то интуитивно понятное для пользователя. Подумай о
                        чекбоксах, слайдерах для цен и т.д.
                        Реализуй логику фильтрации. Нужно, чтобы данные отправлялись на сервер, обрабатывались, и товары
                        на странице обновлялись. Используй AJAX для этого, чтобы страница не перезагружалась.
                        Проверь все тщательно. Убедись, что фильтры работают корректно и не ломают существующую
                        функциональность.</p>
                </div>
                <div class="record-notes-detail__section record-notes-detail__section--download">
                    <p class="record-notes-detail__download-text">
                        Задача в проекте: <a href="#" class="record-notes-detail__link">Модуль фильтрации</a>
                    </p>
                </div>
            </div>

            <div class="task-details">
                <div class="task-details__status">
                    <p class="task-details__status-text">Ждет выполнения с 01.01.2025 10:23</p>
                </div>

                <div class="task-details-main">
                    <div class="task-details__info">
                        <p class="task-details__info-item">Крайний срок: 01.02.2025</p>
                        <p class="task-details__info-item">Напоминание: установлено</p>
                        <p class="task-details__info-item">Поставлена: 01.01.2025</p>
                        <p class="task-details__info-item">Оценка: ☆☆☆☆☆</p>
                    </div>

                    <div class="task-details__participants">
                        <div class="task-details__participant">
                            <p class="task-details__participant-title">Постановщик</p>
                            <div class="task-details__participant-info">
                                <div class="task-details__avatar"></div>
                                <p class="task-details__participant-name">Елисеев Андрей</p>
                            </div>
                        </div>
                        <div class="task-details__participant">
                            <p class="task-details__participant-title">Ответственный</p>
                            <div class="task-details__participant-info">
                                <div class="task-details__avatar"></div>
                                <p class="task-details__participant-name">Пятков Константин</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
