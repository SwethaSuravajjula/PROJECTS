<template>
    <div v-if="role === 'admin'">
      <h4>Welcome {{users}}!</h4>
      <div>
        <nav class="nav-bar">
          <ul>
            <li><router-link :to="{ name: 'sections'}" class="nav-link">Sections</router-link></li>
            <li><router-link :to="{ name: 'users'}" class="nav-link">User Details</router-link></li>
            <li><router-link to="/createsection" class="nav-link">New Section</router-link></li>
            <li><router-link to="/feedbackdetail" class="nav-link">Feedback Details</router-link></li>
            <li><router-link :to="{ name: 'useractivities'}" class="nav-link">User Activity</router-link></li>
            <li><router-link to="/feedbackdetails" class="nav-link">Feedback</router-link></li>
            <li><router-link to="/issuebook" class="nav-link">Issued Details</router-link></li>
            <li><router-link to="/login" @click="logout" class="nav-link">Logout</router-link></li>

        
          </ul>
          </nav>
          </div>
          <br>

      <h1>User Profile</h1>
      <div v-if="user">
        <table class="profile-table">
          <thead>
            <tr>
              <th colspan="2">User Details</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>User ID:</td>
              <td>{{ userId }}</td>
            </tr>
            <tr>
              <td>Email:</td>
              <td>{{ user.email }}</td>
            </tr>
            <tr>
              <td>Active:</td>
              <td>{{ user.active ? 'Yes' : 'No' }}</td>
            </tr>
          </tbody>
        </table>
  
        <h2>Issued Books</h2>
        <div v-if="user.issue && user.issue.length > 0">
          <table class="profile-table">
            <thead>
              <tr>
                <th>Issue ID</th>
                <th>Book Issued</th>
                <th>Section of the Book</th>
                <th>Issue Date</th>
                <th>Return Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="issue in user.issue" :key="issue.issue_id">
                <td>{{ issue.issue_id }}</td>
                <td>{{ issue.book_issued }}</td>
                <td>{{ issue.section_of_the_book }}</td>
                <td>{{ formatDate(issue.issue_date) }}</td>
                <td>{{ formatDate(issue.return_date) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else>No books issued</p>
      </div>
      <div v-else>
        <p>Loading user details...</p>
      </div>
      
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  const API_BASE_URL = 'http://localhost:7000/api';
  
  export default {
    data() {
      return {
        user: null,
        authToken: '',
        userId: null,
        users:''
        
      };
    },
    created() {
      this.authToken = localStorage.getItem('authToken');
      this.userId = this.$route.params.userId;
      this.role = localStorage.getItem('userRole');
      this.users = localStorage.getItem('email');

  
      if (!this.authToken && !this.role=='admin') {
        this.$router.push('/login');
        return;
      }
  
      this.getUserDetails();
    },
    methods: {
      getUserDetails() { // gives the details of the user
        axios.get(`${API_BASE_URL}/admin/${this.userId}`, {
          headers: {
            'Authentication-Token': this.authToken
          }
        })
        .then(response => {
          this.user = response.data.users;
        })
        .catch(error => {
          console.error('Error fetching user details:', error.response ? error.response.data.message : error.message);
        });
      },
      formatDate(timestamp) { // there was timestamps earlier now it is formatted properly
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
  .profile-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  .profile-table th, .profile-table td {
    padding: 8px;
    border: 1px solid #ddd;
  }
  
  .profile-table th {
    background-color: #f2f2f2;
    text-align: left;
  }
  
  .profile-table tbody tr:nth-child(even) {
    background-color: #f2f2f2;
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
  