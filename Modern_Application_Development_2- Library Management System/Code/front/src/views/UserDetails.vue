<template>
  <div v-if="role === 'admin'">
    <h4>Welcome {{user}} !</h4>
    <div>
    
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
    </div>
    <br>
    <h1>User Details</h1>
    <br>
    
    <div class="search-container">
      <input type="text" v-model="searchQuery" class="search-input" placeholder="Search users...">
    </div>
    
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>User ID</th>
            <th>Email</th>
            <th>Active</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.id }}</td>
            <td><router-link :to="{ name: 'profiles', params: { userId: user.id } }">{{ user.email }}</router-link></td>
            <td>{{ user.active ? 'Yes' : 'No' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="filteredUsers.length === 0">
      <p>No Users</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
const API_BASE_URL = 'http://localhost:7000/api';

export default {
  data() {
    return {
      users: [],
      authToken: '',
      role: '',
      searchQuery: '',
      user:''
    };
  },
  created() {
    this.authToken = localStorage.getItem('authToken');
    this.role = localStorage.getItem('userRole');
    this.user = localStorage.getItem('email')

    if (!this.authToken || !this.role=='admin') {
      this.$router.push('/login');
      return;
    }
    
    this.fetchUserDetails();
  },
  methods: {
    fetchUserDetails() { // gets all the user details 
      axios.get(`${API_BASE_URL}/admin`, {
        headers: {
          'Authentication-Token': this.authToken
        }
      })
      .then(response => {
        this.users = response.data;
      })
      .catch(error => {
        console.error('Error fetching user details:', error);
    
        this.errorMessage = 'Failed to fetch user details. Please try again later.';
      });
    },
    logout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
      localStorage.removeItem('email');
      this.$router.push('/login');
    }
  },
  computed: {
    filteredUsers() { // this is for the search bar
      return this.users.filter(user => {
        return user.email.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
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

.table th, .table td {
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
