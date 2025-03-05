<template>
  <div class="container">
      <h1 class="header">Calculator</h1>
      <input v-model.number="num1" type="number" class="input" />
      <input v-model.number="num2" type="number" class="input" />
      <div class="buttons">
        <button @click="sum" class="button">Сумма</button>
        <button @click="subtraction" class="button">Вычитание</button>
        <button @click="proizvedenie" class="button">Произведение</button>
        <button @click="division" class="button">Деление</button>
      </div>
      <p class="result">Результат: {{ result }}</p>
  </div>
</template>

<script>
export default {
  data() {
      return {
          num1: 0,
          num2: 0,
          result: null
      };
  },
  methods: {
      sum() {
        window.electronAPI.calculateSum(this.num1, this.num2);
      },
      subtraction() {
        window.electronAPI.calculateSubtraction(this.num1, this.num2);
      },
      proizvedenie() {
        window.electronAPI.calculateProizvedenie(this.num1, this.num2);
      },
      division() {
        window.electronAPI.calculateDivision(this.num1, this.num2);
      },
  },
  mounted() {
      window.electronAPI.onPythonData((event, data) => {
          this.result = parseFloat(data);
      });
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
}

.container {
  display: flex;
  flex-direction: column;
  text-align: center;
  justify-content: center;
  gap: 14px;
  width: 50vh;
}

.header {
  color: #42b983;
}

.input {
  padding: 5px;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #369670;
}

.result {
  text-align: start;
}
</style>