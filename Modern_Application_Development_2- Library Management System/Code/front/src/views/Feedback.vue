<template>
  <div v-if="role === 'user'">
    <h4>Welcome {{user}} !</h4>
  <nav class="nav-bar">
    <ul>
      <li><router-link :to="{ name: 'carts'}" class="nav-link">My Cart</router-link></li>
      <li><router-link :to="{ name: 'sections'}" class="nav-link">Sections</router-link></li>
      <li><router-link to="/login" @click="logout" class="nav-link">Logout</router-link></li>
    </ul>
  </nav>
    <div class="feedback-container">
      <h1>Leave Feedback</h1>
      <form @submit.prevent="submitFeedback" class="feedback-form">
        <label for="rating">Rating (1-5):</label>
        <input type="number" id="rating" v-model="rating" min="1" max="5" required>
        
        <label for="comment">Comment:</label>
        <textarea id="comment" v-model="comment"></textarea>
        
        <button type="submit">Submit Feedback</button>
        <p>{{message}}</p>
      </form>
    </div>
    </div>
  </template>
  
  <script>
import axios from 'axios';
const API_BASE_URL = 'http://localhost:7000/api';

export default {
  data() {
    return {
      rating: null,
      comment: null,
      authToken: null,
      message: '',
      bookId: null,
      role: '',
      user: ''
    };
  },
  created() {
    this.authToken = localStorage.getItem('authToken');
    this.role = localStorage.getItem('userRole');
    this.user = localStorage.getItem('email');
    if (!this.authToken || !this.role == 'user') {
      this.$router.push('/');
    }
    this.bookId = this.$route.params.bookId;
  },
  methods: {
    submitFeedback() {
  axios.post(`${API_BASE_URL}/feedback/${this.bookId}`, {   // upon submitting the feedback; it goes into the backend and posts it into the backend and responds
    rating: this.rating,
    comment: this.comment
  }, {
    headers: {
      'Authentication-Token': this.authToken
    }
  })
  .then(response => {
    this.message = response.data.message; // this is the response that the backend gives after submitting the feedback
    this.$router.push('/cart');
  })
  .catch(error => {
    this.message = error.response.data.message;
  });
}
,
    logout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
      localStorage.removeItem('email');
      this.$router.push('/');
    }
  }
};
</script>

  <style scoped>
  .feedback-container {
    max-width: 400px;
    margin: 0 auto;
  }
  
  .feedback-container h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .feedback-form label {
    display: block;
    margin-bottom: 5px;
  }
  
  .feedback-form input[type="number"],
  .feedback-form textarea {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .feedback-form button {
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .feedback-form button:hover {
    background-color: #0056b3;
  }
  
  .feedback-form button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  .section-item {
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .section-item h2 {
    margin-bottom: 5px;
  }
  
  .section-item p {
    margin-top: 5px;
    color: #666;
  }
  
  .nav-link,
  .section-link,
  .section-action {
    text-decoration: none;
    margin-right: 10px;
  }
  
  .nav-link {
    color: white;
  }
  
  .nav-link:hover,
  .section-link:hover,
  .section-action:hover {
    background-color: #111;
  }
  
  .section-link,
  .section-action {
    color: #333;
  }
  
  .search-container {
    margin-bottom: 20px;
  }
  
  .search-input {
    width: 100%;
    padding: 10px;
    box-sizing: border-box;
    border: 2px solid #ccc;
    border-radius: 4px;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #007bff;
  }
  
  .nav-bar {
    background-color: #333;
    overflow: hidden;
    list-style-type: none;
    padding: 0;
  }
  
  .nav-bar ul {
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
  
  .nav-bar li {
    float: left;
  }
  
  .nav-bar li a {
    display: block;
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
  }
  
  .nav-bar .active {
    background-color: #04AA6D;
  }
  
  .nav-bar li a:hover:not(.active) {
    background-color: #111;
  }
  
  .button {
    background-color: #007bff;
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
  }
  
  .button:hover {
    background-color: #0056b3;
  }
  
  .section-link:hover h2 {
    color: #007bff; 
  }
  </style>
  