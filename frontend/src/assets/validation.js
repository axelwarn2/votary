export const validateForm = (formData, fieldConfig) => {
    const errors = {};

    Object.keys(fieldConfig).forEach((field) => {
        const value = formData[field] ? formData[field].trim() : '';
        const config = fieldConfig[field];

        if (config.required && !value) {
            errors[field] = 'Поле обязательно к заполнению';
            return;
        }

        if (config.minLength && value.length < config.minLength) {
            errors[field] = `Поле должно содержать не менее ${config.minLength} символов`;
            return;
        }

        if (config.isEmail && value && !value.includes('@')) {
            errors[field] = 'Введите корректный email';
            return;
        }

        if (config.matchWith && formData[config.matchWith] && value !== formData[config.matchWith].trim()) {
            errors[field] = 'Поля не совпадают';
            return;
        }
    });

    return errors;
}
