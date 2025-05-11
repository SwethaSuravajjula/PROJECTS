<template>
  <div class="register">
    <h1>User Registration</h1>
    <form @submit.prevent="registerUser">
      <div class="form-group">
        <label>Name:</label>
        <input type="text" v-model="name" :class="{ 'invalid': !isNameValid }" @input="validateName" required />
        <p v-if="!isNameValid" class="error-message">Name should start with a capital letter</p>
      </div><br>
      <div class="form-group">
        <label>Email:</label>
        <input type="email" v-model="email" :class="{ 'invalid': !isEmailValid }" @input="validateEmail" required />
        <p v-if="!isEmailValid" class="error-message">Enter a valid email address</p>
      </div><br>
      <div class="form-group">
        <label>Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Register</button>
      <br>
      <div>
      <router-link :to="{name:'login'}">Already have an account?</router-link>
      </div>
    </form>
    <p v-if="message" class="error-message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import router from '../router';

const API_BASE_URL = 'http://localhost:7000/api';

export default {
  data() {
    return {
      name: '',
      email: '',
      password: '',
      message: '',
      isNameValid: true,
      isEmailValid: true,
    
    };
  },
  methods: {
    registerUser() {  // this is the main part of user registration
      axios.post(`${API_BASE_URL}/register`, {
        name: this.name,
        email: this.email,
        password: this.password,
      })
      .then((response) => {
        this.message = response.data.message;
        this.name = '';
        this.email = '';
        this.password = '';
        router.push('/');
      })
      .catch((error) => {
        if (error.response && error.response.data.message) {
          this.message = error.response.data.message;
        } else {
          this.message = 'An error occurred while registering the user.';
        }
      });
    },
    validateName() { // this checkes whether the username starts with caps
      this.isNameValid = /^[A-Z]/.test(this.name);
    },
    validateEmail() { // this checks whether the user is entering an email address with @ included
      this.isEmailValid = /^[^@]+@[^@]+\.[a-zA-Z]{2,}$/.test(this.email);
    },
  },
};
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type='text'],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  margin-top: 5px;
}

.invalid {
  border-color: red;
}
</style>
