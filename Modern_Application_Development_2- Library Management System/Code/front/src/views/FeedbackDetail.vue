<template>
    <div>
      <h4>Welcome {{ user }} !</h4>
      <nav class="nav-bar">
        <ul>
          <li><router-link :to="{ name: 'sections' }" class="nav-link">Sections</router-link></li>
          <li><router-link :to="{ name: 'users' }" class="nav-link">User Details</router-link></li>
          <li><router-link to="/createsection" class="nav-link">New Section</router-link></li>
          <li><router-link :to="{ name: 'useractivities' }" class="nav-link">User Activity</router-link></li>
          <li><router-link to="/feedbackdetails" class="nav-link">Feedback</router-link></li>
          <li><router-link to="/issuebook" class="nav-link">Issued Details</router-link></li>
          <li><router-link to="/login" @click="logout" class="nav-link">Logout</router-link></li>
        </ul>
      </nav>
      <h1>Feedback</h1>
      <div class="search-container">
      <input type="text" v-model="searchQuery" placeholder="Search feedback..." class="search-input">
      </div>
      <table class="table">
        <thead>
          <tr>
            <th>User</th>
            <th>Book</th>
            <th>Section</th>
            <th>Rating</th>
            <th>Comment</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="feedback in filteredFeedback" :key="feedback.id">
            <td>{{ feedback.user }}</td>
            <td>{{ feedback.book }}</td>
            <td>{{ feedback.section }}</td>
            <td>{{ feedback.rating }}</td>
            <td>{{ feedback.comment }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  const API_BASE_URL = 'http://localhost:7000/api';
  
  export default {
    data() {
      return {
        feedback: [],
        searchQuery: '',
        user: ''
      };
    },
    created() {
      this.authToken = localStorage.getItem('authToken');
      this.role = localStorage.getItem('userRole');
      this.user = localStorage.getItem('email');
      if (!this.authToken || !this.role == 'admin') {
        this.$router.push('/');
      }
      this.getFeedback();
    },
    computed: {
      filteredFeedback() {
        return this.feedback.filter(feed => {
          return feed.user.toString().toLowerCase().includes(this.searchQuery.toLowerCase()) ||
             feed.book.toString().toLowerCase().includes(this.searchQuery.toLowerCase()) ||
             feed.section.toString().toLowerCase().includes(this.searchQuery.toLowerCase()) ||
             feed.comment.toLowerCase().includes(this.searchQuery.toLowerCase());
        });
      }
    },
    methods: {
      getFeedback() {
        axios.get(`${API_BASE_URL}/user/feedback`, {
          headers: {
            'Authentication-Token': this.authToken
          }
        })
        .then(response => {
          this.feedback = response.data.feedback;
        })
        .catch(error => {
          console.error('Error fetching feedback:', error);
        });
      },
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
  
  .table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .table th,
  .table td {
    padding: 8px;
    border: 1px solid #ddd;
  }
  
  .table th {
    background-color: #f2f2f2;
    text-align: left;
  }
  
  .table tbody tr:nth-child(even) {
    background-color: #f2f2f2;
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
  
  </style>
  