<template>
    <div v-if="role === 'user'">
    <div>
    <h4>Welcome {{ users }}!</h4>
      <nav class="nav-bar">
        <ul>
          <li><router-link :to="{ name: 'carts'}" class="nav-link">My Cart</router-link></li>
          <li><router-link :to="{ name: 'sections'}" class="nav-link">Sections</router-link></li>
          <li><router-link to="/login" @click="logout" class="nav-link">Logout</router-link></li>
        </ul>
      </nav>
      <br>
      <iframe :src="pdfUrl" type="application/pdf" width="100%" height="700px"></iframe>
    </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  const API_BASE_URL = 'http://localhost:7000/api';
  
  export default {
    data() {
      return {
        pdfUrl: '',
        role: '',
        message: '',
        authToken:'',
        userId:'',
        users: '',
        book_name:''
      };
    },
    created() {
        this.authToken = localStorage.getItem('authToken');
      this.userId = this.$route.params.userId;
      this.role = localStorage.getItem('userRole');
      this.users = localStorage.getItem('email');

  
      if (!this.authToken && !this.role=='user') {
        this.$router.push('/login');
        return;
      }
      this.fetchPdf();
    },
    methods: {
      fetchPdf() {
        const bookId = this.$route.params.bookId; 
        axios.get(`${API_BASE_URL}/pdfissue/${bookId}`, {
          headers: {
            'Authentication-Token': this.authToken
          }
        })
        .then(response => {
          const bookName = response.data.book_name;
          this.book_name = response.data.book_name;
          this.pdfUrl = `http://localhost:8000/${bookName}#toolbar=0`;
        })
        .catch(error => {
          this.message= error.response.data.message;
        });
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
