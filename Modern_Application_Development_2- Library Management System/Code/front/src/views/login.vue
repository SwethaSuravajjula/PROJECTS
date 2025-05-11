<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <div class="form-group">
        <label>Name:</label>
        <input type="text" v-model="name" :class="{ 'invalid': nameError }" required @input="validateName">
        <p v-if="nameError" class="error-message">{{ nameError }}</p>
      </div>
      <div class="form-group">
        <label>Email:</label>
        <input type="email" v-model="email" required @input="validateEmail">
        <p v-if="emailError" class="error-message">{{ emailError }}</p>
      </div>
      <div class="form-group">
        <label>Password:</label>
        <input type="password" v-model="password" required>
      </div>
      <button type="submit">Login</button>
      <br>
    </form>
    <br>
    <router-link :to="{ name: 'register' }">New User</router-link>
    <br>
    <p v-if="message" class="error-message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE_URL = 'http://localhost:7000/api';

export default {
  data() {
    return {
      email: '',
      password: '',
      name: '',
      message: '',
      emailError: '',
      nameError: '',
    };
  },
  methods: {
    validateEmail() {  // it  gives the message whether the input entered into this box contains an @ symbol
      if (!this.email.includes('@')) {
        this.emailError = 'Email must contain "@" symbol';
      } else {
        this.emailError = '';
      }
    },
    validateName() { // it gives the message whether the input entered into this box contains starts with a capital letter
      if (!/^[A-Z]/.test(this.name)) {
        this.nameError = 'Name must start with caps';
      } else {
        this.nameError = '';
      }
    },
    loginUser() {
  
      if (this.emailError || this.nameError) {
        return; // make it invalid if email or name is invalid
      }

      axios.post(`${API_BASE_URL}/login`, {
        name: this.name,
        email: this.email,
        password: this.password,
      })
      .then(response => {
        this.message = response.data.message;
        this.name = '';
        this.email = '';
        this.password = '';
        localStorage.setItem('userRole', response.data.role);
        localStorage.setItem('authToken', response.data.token);
        localStorage.setItem('email', response.data.email);
        localStorage.setItem('username',response.data.name);
        this.$router.push('/sections');
      })
      .catch(error => {
        if (error.response && error.response.data.message) {
          this.message = error.response.data.message;
        } else {
          this.message = error.message;
        }
      });
    }
  },
};
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
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
  margin-top: 10px;
}

.invalid {
  border-color: red;
}
</style>
