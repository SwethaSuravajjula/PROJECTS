
<template>
  <div>
    <div v-if="role === 'user'">
      <h4>Welcome {{user}} !</h4>
      <nav class="nav-bar">
        <ul>
          <li><router-link :to="{ name: 'carts'}" class="nav-link">My Cart</router-link></li>
          <li><router-link :to="{ name: 'sections'}" class="nav-link">Sections</router-link></li>
          <li><router-link to="/login" @click="logout" class="nav-link">Logout</router-link></li>
        </ul>
      </nav>
      <br>
      <h1>Books</h1>
      <div class="search-container">
        <input type="text" v-model="searchQuery" @input="filterBooks" placeholder="Search books..." class="search-input">
      </div>
      <br>
      <div v-if="filteredBooks.length >0">
      <p class="form-message">{{ message }}</p>
      <div class="book-card section-item" v-for="book in filteredBooks" :key="book.id">
        <div class="book-image-container">
         <img :src="`http://localhost:5000/${book.book_image}`" alt="Book Image" class="book-image">
        </div>
        <h2><strong>Name of the book:</strong> {{ book.name }}</h2>
        <p><strong>Authors:</strong> {{ book.authors }}</p>
        <p><strong>Number of pages:</strong> {{ book.no_of_pages }}</p>
        <p><strong>Available copies:</strong> {{ book.available_copies }}</p>
        <p><strong>Total copies:</strong> {{ book.total_copies }}</p>
        <button @click="requestBook(book.id)" class="button">Request Book</button>
        

      </div>
      </div>
      <div v-else>
        <p>No books created yet</p>
      </div>
    </div>
    <div v-else-if="role === 'admin'">
      <h4>Welcome {{user}} !</h4>
      <nav class="nav-bar">
        <ul>
          <li><router-link :to="{ name: 'createbooks', params: {sectionId: sectionId } }" class="nav-link"> New Book</router-link></li>
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
      <h1>Books</h1>
      <br>
      <div class="search-container">
        <input type="text" v-model="searchQuery" @input="filterBooks" placeholder="Search books..." class="search-input">
      </div>
      <div class="book-card section-item" v-for="book in filteredBooks" :key="book.id">
        <div class="book-image-container">
          <a :href="`http://localhost:8000/${book.book}`" target="_blank"><img :src="`http://localhost:5000/${book.book_image}`" alt="Book Image" class="book-image"></a>
        </div>
        <h2><strong>{{ book.name }}</strong></h2>
        <br>
        <p><strong>Authors:</strong> {{ book.authors }}</p>
        <p><strong>Number of pages:</strong> {{ book.no_of_pages }}</p>
        <p><strong>Available copies:</strong> {{ book.available_copies }}</p>
        <p><strong>Total copies:</strong> {{ book.total_copies }}</p>
        <div>
          <router-link :to="{ name: 'modifybooks', params: { sectionId: sectionId, bookId: book.id } }" class="section-action button">Modify</router-link> |
          <router-link :to="{ name: 'deletebooks', params: { sectionId: sectionId, bookId: book.id } }" class="section-action button">Delete</router-link>
        </div>
        <br>
      </div>
      </div>
     </div>
  
</template>

<script>
import axios from 'axios';
const API_BASE_URL = 'http://localhost:7000/api';
const BASE_URL = 'http://localhost:7000';

export default {
  data() {
    return {
      books: [],
      filteredBooks: [],
      searchQuery: '', // this is for the search bar 
      role: null,
      authToken: null,
      sectionId: null,
      message: "",
      user: ""
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

    this.books_list();
  },
  methods: {
    books_list() { // fetches the list of all the books 
      axios.get(`${API_BASE_URL}/sections/${this.sectionId}/books`, {
        headers: {
          'Authentication-Token': this.authToken,
        }
      })
      .then(response => {
        if (response && response.data && response.data.books) {
          this.books = response.data.books;
          this.filteredBooks = this.books; // Initializing the filteredBooks with all books 
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
    requestBook(bookId) { // this is a button where when book is requested this method is invoked 
      axios.post(`${API_BASE_URL}/request-book/${bookId}`, null, {
        headers: {
          'Authentication-Token': this.authToken,
        }
      })
      .then(response => {
        console.log(response.data.message);
        this.message = response.data.message;
        this.$router.push('/cart');
      })
      .catch(error => {
        this.message = error.response.data.message;
        setTimeout(() => {
          this.message = '';
        }, 3000)
      });
    },
    filterBooks() { // this is mainly for the search bar 
      const query = this.searchQuery.trim().toLowerCase();
      this.filteredBooks = this.books.filter(book => {
        const bookName = book.name.toLowerCase();
        const authors = book.authors.toLowerCase();
        return bookName.includes(query) || authors.includes(query);
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


  .book-image {
    width: 150px; 
    height: 200px; 
  }




.book-details {
  flex: 1; 
}

.book-image-container {
  margin-left: 20px; 
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
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
  background-color: rgb(29, 34, 17);
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
