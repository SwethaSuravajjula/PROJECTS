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
    <br>
    <h1>User Activity</h1>
    <div class="search-container">
      <input type="text" v-model="searchQuery" class="search-input" placeholder="Search activity or user...">
    </div>
    <div v-if="filteredItems.length > 0">
      <table class="activity-table">
        <thead>
          <tr>
            <th>Activity ID</th>
            <th>User ID</th>
            <th>User</th>
            <th>Activity Type</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredItems" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.user_id || '' }} </td>
            <td>{{ item.user || '' }} </td>
            <td>{{ item.activity_type }}</td>
            <td>{{item.activity_timestamp}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>No activity found for this user</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
const API_BASE_URL = 'http://localhost:7000/api';

export default {
  data() {
    return {
      activities: [],
      users: [], 
      authToken: '',
      userId: null,
      searchQuery: '',
      role: '',
      user: ''
    };
  },
  created() {
    this.authToken = localStorage.getItem('authToken');
    this.role = localStorage.getItem('userRole');
    this.user = localStorage.getItem('email');
    if (!this.authToken && !this.role=='admin') {
      this.$router.push('/login');
      return;
    }

    this.getUserActivity();
  },
  methods: {
    getUserActivity() {  // gives all the details of the user activity i.e whether the user has logged in or was issued a particular book from a particular section and so on.
      axios.get(`${API_BASE_URL}/admin/activity`, {
        headers: {
          'Authentication-Token': this.authToken
        }
      })
      .then(response => {
        this.activities = response.data.activity;
      })
      .catch(error => {
        console.error('Error fetching user activity:', error.response ? error.response.data.message : error.message);
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
    filteredItems() { // this is for the search bar whether it filters out based on all the elements present in the activities list
      const allItems = [...this.activities, ...this.users];
      return allItems.filter(item => {
        return (
          item.activity_type.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          item.user.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      });
    }
  }
};
</script>

<style scoped>
.activity-table {
  width: 100%;
  border-collapse: collapse;
}

.activity-table th, .activity-table td {
  padding: 8px;
  border: 1px solid #ddd;
}

.activity-table th {
  background-color: #f2f2f2;
  text-align: left;
}

.activity-table tbody tr:nth-child(even) {
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
