<template>
  <div>
    <div v-if="role === 'user'">
      <h4>Welcome {{ user }}!</h4>
      <nav class="nav-bar">
        <ul>
          <li><router-link :to="{ name: 'carts'}" class="nav-link">My Cart</router-link></li>
          <li><router-link :to="{ name: 'sections'}" class="nav-link">Sections</router-link></li>
          <li><router-link to="/login" @click="logout" class="nav-link">Logout</router-link></li>
        </ul>
      </nav>
      <br>
      <h1>My Cart</h1>
      <br>
      <div v-if="issued.length > 0">        
        <div v-for="issue in issued" :key="issue.issue_id" class="section-item">
          <h2>{{ issue.book }}</h2>
          <p><strong>Content:</strong></p> <router-link :to="{ name: 'pdfs', params: { bookId: issue.book_id } }">
            <img :src="`http://localhost:5000/${issue.image}`" alt="Book Image" class="book-image"></router-link>
          
          <p><strong>Authors:</strong> {{ issue.authors }}</p>
          <p><strong>Section Name:</strong> {{ issue.section_name }}</p>
          <p><strong>Issue Date:</strong> {{ formatDate(issue.issue_date) }}</p>
          <p><strong>Return Date:</strong> {{ formatDate(issue.return_date) }}</p>
          <p><router-link :to="{ name: 'sectionbooks', params: { sectionId: issue.section_id } }">
            View more in this section
          </router-link></p>
          <button @click="returnBook(issue.book_id)" :disabled="returning" class="button">Return Book</button>
          <p class="form-message">{{ issue.message }}</p>
        </div>
      </div>
      <p v-else>No books issued</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
const API_BASE_URL = 'http://localhost:7000/api';

export default {
  data() {
    return {
      issued: [],
      message: '',
      authToken: '',
      role: '',
      returning: false,
      user: '' 
    };
  },
  created() {
    this.authToken = localStorage.getItem('authToken');
    this.role = localStorage.getItem('userRole');
    this.user = localStorage.getItem('email');

    if (!this.authToken || !this.role == 'user') {
      this.$router.push('/login');
      return;
    }
    this.fetchUserCart();

    },
  methods: {
  
    fetchUserCart() {
      axios.get(`${API_BASE_URL}/user/cart`, {
        headers: {
          'Authentication-Token': this.authToken
        }
      })
      .then(response => {
        this.issued = response.data.issued;
      })
      .catch(error => {
        console.error('Error fetching user cart:', error.response.data.message);
      });
    },
    returnBook(bookId) {
      this.returning = true; // here flag  is used to disable the return button during the process
      axios.post(`${API_BASE_URL}/return-book/${bookId}`, null, {
        headers: {
          'Authentication-Token': this.authToken
        }
      })
      .then(response => {
        this.message = response.data.message;
        // Filtering  the returned book from the issued list
        this.$router.push({ name: "feedbacks", params: { bookId: bookId } })
        this.issued = this.issued.filter(issue => issue.book_id !== bookId);
      })
      .catch(error => {
        console.error('Error returning book:', error.response.data.message);
      })
      .finally(() => {
        this.returning = false; // Reseting the flag after the process is completed. now the button should be enabled
      });
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
    logout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
      localStorage.removeItem('email');
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
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

.book-image {
  width: 150px; 
  height: 200px; 
}
</style>