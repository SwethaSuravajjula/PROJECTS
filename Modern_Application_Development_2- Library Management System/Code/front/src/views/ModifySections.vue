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
              <br>
        </div>
        
        <div class="form-container">
            <h1>Update Section</h1>
        <form @submit.prevent="updateSection">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" v-model="updatedsection.name" required>
            </div>
            <div class="form-group">
                <label for="description">Description:</label>
                <textarea id="description" v-model="updatedsection.description" required></textarea>
            </div>
            <button type="submit" class="button">Update Section</button>
        </form>
        <p v-if="message" class="form-message">{{ message }}</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
const API_BASE_URL = 'http://localhost:7000/api';

export default {
    data() {
        return {
            section: {},
            updatedsection: {
                name: '',
                description: '',
            },
            message: '',
            role: '',
            user: ''
        };
    },
    created() {
        this.authToken = localStorage.getItem('authToken');
        this.role = localStorage.getItem('userRole');
        this.user = localStorage.getItem('email');
        if (!this.authToken || !this.role == 'admin') {
            this.$router.push('/login');
            return;
        }
        const sectionId = this.$route.params.sectionId;
        this.fetchSectionDetails(sectionId);
    },
    methods: {
        fetchSectionDetails(sectionId) { // gives the sections details 
            axios.get(`${API_BASE_URL}/admin/sections/${sectionId}`, {
                headers: {
                    'Authentication-Token': this.authToken,
                },
            })
            .then(response => {
                this.section = response.data.section;
                this.updatedsection.name = this.section.name;
                this.updatedsection.description = this.section.description;
            })
            .catch(error => {
                console.error('Error fetching section details:', error);
            });
        },
        updateSection() { // updates the sections 
            const sectionId = this.$route.params.sectionId;
            axios.put(`${API_BASE_URL}/admin/sections/${sectionId}`, this.updatedsection, {
                headers: {
                    'Authentication-Token': this.authToken,
                },
            })
            .then(response => {
                this.message = response.data.message;
                this.$router.push('/sections');
            })
            .catch(error => {
                this.message = error.response.data.message;
            });
        },
        logout() { // logs out 
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
  
  .button {
    background-color: #007bff;
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer; 
    transition: background-color 0.3s ease; 
  }
  
  .button:hover {
    background-color: #0056b3;
  }
  
  .section-link:hover h2 {
    color: #007bff; 
  }
  
  .form-container {
    margin-top: 20px;
    border: 1px solid #ccc;
    padding: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: inline-block;
    width: 150px; 
    margin-right: 10px;
  }
  
  .form-group input[type="text"],
  .form-group input[type="number"],
  .form-group input[type="file"],
  .form-group button[type="submit"] {
    width: calc(100% - 160px); 
    padding: 10px;
    box-sizing: border-box;
    border: 2px solid #ccc;
    border-radius: 4px;
  }
  
  .form-group input[type="text"],
  .form-group input[type="number"],
  .form-group input[type="file"] {
    height: 40px;
  }
  
  .form-group input[type="text"]:focus,
  .form-group input[type="number"]:focus,
  .form-group input[type="file"]:focus {
    outline: none;
    border-color: #007bff;
  }
  
  .form-group button[type="submit"] {
    background-color: #007bff;
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer; 
    transition: background-color 0.3s ease; 
  }
  
  .form-group button[type="submit"]:hover {
    background-color: #0056b3;
  }
  
  .form-message {
    margin-top: 10px;
    color: red;
  }

  .form-group textarea {
    width: calc(100% - 160px); 
    padding: 10px;
    box-sizing: border-box;
    border: 2px solid #ccc;
    border-radius: 4px;
    height: 120px; 
  }
  
  .form-group textarea:focus {
    outline: none;
    border-color: #007bff;
  }
  
</style>
