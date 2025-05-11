<template>
    <nav class="nav-bar">
    </nav>
  </template>
  
  <script>
  export default {
    // Component logic goes here
  }
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
  </style>
  