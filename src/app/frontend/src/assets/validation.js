export const validateForm = (formData, fieldConfig) => {
    const errors = {};

    Object.keys(fieldConfig).forEach((field) => {
        const value = formData[field] ? formData[field].trim() : '';
        const config = fieldConfig[field];

        if (config.required && !value) {
            errors[field] = `Поле "${config.label}" обязательно к заполнению`;
            return;
        }

        if (config.minLength && value.length < config.minLength) {
            errors[field] = `Поле "${config.label}" должно содержать не менее ${config.minLength} символов`;
            return;
        }

        if (config.maxLength && value.length > config.maxLength) {
            errors[field] = `Поле "${config.label}" должно содержать не более ${config.maxLength} символов`;
        }

        if (config.isEmail && value && !value.includes('@')) {
            errors[field] = 'Введите корректный email';
            return;
        }

        if (config.matchWith && formData[config.matchWith] && value !== formData[config.matchWith].trim()) {
            errors[field] = 'Пароли не совпадают';
            return;
        }
    });

    return errors;
}
