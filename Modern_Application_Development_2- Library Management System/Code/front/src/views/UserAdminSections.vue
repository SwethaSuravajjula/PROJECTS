<template>
  <div>
    <div v-if="role === 'user'">
      <h4>Welcome {{user}} !</h4>
      <nav class="nav-bar">
        <ul>
          <li><router-link :to="{ name: 'carts'}" class="nav-link">My Cart</router-link></li>
          <li><router-link :to="{name: 'sections'}" class="nav-link">Sections </router-link></li>
          <li><router-link to="/" @click="logout" class="nav-link">Logout</router-link></li>
        </ul>
      </nav>
      <br>
      <h1>Sections</h1>
      <br>
      <div class="search-container">
        <input type="text" v-model="searchQuery" @input="filterSections" placeholder="Search books..." class="search-input">
      </div>
      <div v-for="section in filteredSections" :key="section.section_id" class="section-item">
        <router-link :to="{ name: 'sectionbooks', params: { sectionId: section.section_id } }" class="section-link">
          <h2>{{ section.section_name }}</h2>
        </router-link>
        <p><strong>Description:</strong>{{ section.section_description }}</p>
      </div>
    </div>

    <div v-else-if="role === 'admin'">
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
      <h1>Sections</h1>
      <br>
      <div class="search-container">
        <input type="text" v-model="searchQuery" @input="filterSections" placeholder="Search sections..." class="search-input">
      </div>
      <div v-for="section in filteredSections" :key="section.section_id" class="section-item">
        <div>
          <router-link :to="{ name: 'sectionbooks', params: { sectionId: section.section_id } }" class="section-link">
            <h2>{{ section.section_name }}</h2>
          </router-link>
          <p><strong>Description:</strong>{{ section.section_description }}</p>
          <br>
        </div>
        <router-link :to="{ name: 'modifysections', params: { sectionId: section.section_id } }" class="section-action button">Modify</router-link>|
        <router-link :to="{ name: 'deletesections', params: { sectionId: section.section_id } }" class="section-action button">Delete</router-link>|
        <router-link :to="{ name: 'createbooks', params: { sectionId: section.section_id } }" class="section-action button">New Book</router-link>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
const API_BASE_URL = 'http://localhost:7000/api';

export default {
  data() {
    return {
      sections: [],
      filteredSections: [],
      searchQuery: '',
      role: null,
      authToken: null,
      sectionId: null,
      paramName: null,
      message: "",
      user:''
    };
  },
  
  created() {
    this.authToken = localStorage.getItem('authToken');
    this.role = localStorage.getItem('userRole');
    this.user = localStorage.getItem('email');

    if (!this.authToken) {
      this.$router.push('/login');
      return;
    }

    this.sectionId = this.$route.params.sectionId;
    
    this.sections_list();
  },
  methods: {
    sections_list() { //fetches the list of sections created by the admin
      axios.get(`${API_BASE_URL}/sections`, {
          headers: {
            'Authentication-Token': this.authToken,
          },
        })
        .then(response => {
          if (response && response.data && response.data.sections) {
            this.sections = response.data.sections;
            this.filteredSections = this.sections; // Initializing the filteredSections with all sections 
          } else {
            console.error('Error: Invalid response data');
            this.message = 'Invalid response data';
          }
        })
        .catch(error => {
          console.error('Error:', error.response ? error.response.data.message : error.message);
          this.message = error.response ? error.response.data.message : error.message;
        });
    },
    filterSections() { // this is mainly for the search bar 
      const query = this.searchQuery.toLowerCase();
      this.filteredSections = this.sections.filter(section => {
        return section.section_name.toLowerCase().includes(query) || section.section_description.toLowerCase().includes(query);
      });
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
</style>
