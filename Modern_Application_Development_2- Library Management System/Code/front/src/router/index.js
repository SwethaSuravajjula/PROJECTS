import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

function isAdmin(to, from, next) {
  const userRole = window.localStorage.getItem("userRole");
  if (userRole === "admin") {
    next(); // Allow access for admin
  } else {
    next("/login"); // if the user is trying to get into admin then it redirects to login
  }
}


const routes = [
  {
    path: '/',
    redirect: '/login',
  },

  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "about" */ '../views/login.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "about" */ '../views/register.vue')
  },
  {
    path: '/sections',
    name: 'sections',
    component: () => import(/* webpackChunkName: "about" */ '../views/UserAdminSections.vue')
  
  },
  {
    path: '/books/:sectionId',
    name: 'sectionbooks',
    component: () => import(/* webpackChunkName: "about" */ '../views/UserAdminBooks.vue')
  },
  {
    path: '/createsection',
    name: 'createsections',
    component: () => import(/* webpackChunkName: "about" */ '../views/CreateSections.vue'),
    beforeEnter: isAdmin,
  },
  {
    path: '/modifysection/:sectionId',
    name: 'modifysections',
    component: () => import(/* webpackChunkName: "about" */ '../views/ModifySections.vue'),
    beforeEnter: isAdmin,
  },
  {
    path: '/deletesection/:sectionId',
    name: 'deletesections',
    component: () => import(/* webpackChunkName: "about" */ '../views/DeleteSections.vue'),
    beforeEnter: isAdmin,
  },
  {
    path: '/createbook/:sectionId',
    name: 'createbooks',
    component: () => import(/* webpackChunkName: "about" */ '../views/CreateBooks.vue'),
    beforeEnter: isAdmin,
  },
  {
    path: '/modifybook/:sectionId/:bookId',
    name: 'modifybooks',
    component: () => import(/* webpackChunkName: "about" */ '../views/ModifyBooks.vue'),
    beforeEnter: isAdmin,
  },
  {
    path: '/deletebook/:sectionId/:bookId',
    name: 'deletebooks',
    component: () => import(/* webpackChunkName: "about" */ '../views/DeleteBooks.vue'),
    beforeEnter: isAdmin,
  },
  {
    path: '/cart',
    name: 'carts',
    component: () => import(/* webpackChunkName: "about" */ '../views/UserCart.vue')
  },
  {
    path: '/user',
    name: 'users',
    component: () => import(/* webpackChunkName: "about" */ '../views/UserDetails.vue')
  },
  {
    path: '/profile/:userId',
    name: 'profiles',
    component: () => import(/* webpackChunkName: "about" */ '../views/User.vue'),
    beforeEnter: isAdmin,
  },
  {
    path: '/useractivity',
    name: 'useractivities',
    component: () => import(/* webpackChunkName: "about" */ '../views/UserActivity.vue'),
    beforeEnter: isAdmin,
  },
  {
    path: '/feedback/:bookId',
    name: 'feedbacks',
    component: () => import(/* webpackChunkName: "about" */ '../views/Feedback.vue')
  },
  {
    path: '/feedbackdetails',
    name: 'feedbackdetail',
    component: () => import(/* webpackChunkName: "about" */ '../views/FeedbackDetail.vue')
  },
  
  {
    path: '/issuebook',
    name: 'issuebooks',
    component: () => import(/* webpackChunkName: "about" */ '../views/IssuedBooks.vue'),
    beforeEnter: isAdmin,
  }
  ,
  {
    path: '/viewpdf/:bookId',
    name: 'pdfs',
    component: () => import(/* webpackChunkName: "about" */ '../views/pdf.vue')


  }

  
  
  



]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})




export default router
