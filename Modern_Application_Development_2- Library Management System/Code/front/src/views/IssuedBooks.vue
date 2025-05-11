<template>
  <div v-if="role === 'admin'">
    <h4>Welcome {{user}} !</h4>
    <nav class="nav-bar">
      <ul>
        <li><router-link :to="{ name: 'sections' }" class="nav-link">Sections</router-link></li>
        <li><router-link :to="{ name: 'users' }" class="nav-link">User Details</router-link></li>
        <li><router-link to="/createsection" class="nav-link">New Section</router-link></li>
        <li><router-link :to="{ name: 'useractivities'}" class="nav-link">User Activity</router-link></li>
        <li><router-link to="/feedbackdetails" class="nav-link">Feedback</router-link></li>
        <li><router-link to="/issuebook" class="nav-link">Issued Details</router-link></li>
        <li><router-link to="/login" @click="logout" class="nav-link">Logout</router-link></li>
        
      </ul>
    </nav>
    <div class="issued-books">
      <h1>Issued Books</h1>
      <div class="search-container">
        <input type="text" v-model="searchQuery" @input="filterIssues" placeholder="Search books..." class="search-input">
      </div>
      <div v-if="isLoading" class="loading">Loading...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else>
        <table class="table">
          <thead>
            <tr>
              <th>User</th>
              <th>Book Title</th>
              <th>Section</th>
              <th>Issued Date</th>
              <th>Return Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="issue in filteredIssues" :key="issue.id">
              <td>{{ issue.name }}</td>
              <td>{{ issue.book }}</td>
              <td>{{ issue.section }}</td>
              <td>{{ issue.issue_date }}</td>
              <td>{{ issue.return_date }}</td>
            </tr>
          </tbody>
        </table>
        
      </div>
    </div>
  </div>
</template>
    

</template>

  
  <script>
  import axios from 'axios';
  const API_BASE_URL = 'http://localhost:7000/api';
  
  export default {
    data() {
      return {
        issues: [],
        filteredIssues: [],
        isLoading: false,
        error: '',
        searchQuery: '',
        role: '',
        user: ''
      };
    },
    created() {
      this.authToken = localStorage.getItem('authToken');
      this.role = localStorage.getItem('userRole');
      this.user = localStorage.getItem('email');
      if (!this.authToken || !this.role =='admin') {
        this.$router.push('/');
      }
      this.fetchIssuedBooks();
    },
    methods: {
      fetchIssuedBooks() {   // this template gives the user to check what are the books that are issued and to whom they are issued.
        this.isLoading = true;
        axios.get(`${API_BASE_URL}/admin/issue`, {
          headers: {
            'Authentication-Token': this.authToken
          }
        })
        .then(response => {
          this.issues = response.data.issue;
          this.filteredIssues = this.issues; // Initializing filteredIssues with all issue.This is basically for the search
          this.isLoading = false;
        })
        .catch(error => {
          this.error = 'Error fetching issued books data.';
          console.error('Error fetching issued books:', error);
          this.isLoading = false;
        });
      },
      filterIssues() {
        const query = this.searchQuery.toLowerCase();
        this.filteredIssues = this.issues.filter(issue => {
          return issue.book_title.toLowerCase().includes(query) || issue.user.toLowerCase().includes(query);
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
  </style>
  