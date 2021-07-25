import Vue from 'vue'
import VueRouter from 'vue-router'
// https://stackoverflow.com/questions/62462276 ow-to-solve-avoided-redundant-navigation-to-current-location-error-in-vue
import Router from 'vue-router'

import Activate from '@/views/auth/Activate'
import ConfirmEmail from '@/views/auth/ConfirmEmail'
import Google from '@/views/auth/Google'
import GoogleForm from '@/views/auth/GoogleForm'
import Home from "@/views/Home";
import IdeaGeneral from '@/views/IdeaGeneral'
import IdeaSearch from '@/views/IdeaSearch'
import IdeaDetail from '@/views/IdeaDetail'
import IdeaCreate from '@/views/IdeaCreate'
import IdeaEdit from '@/views/IdeaEdit'
import IdeaFilter from '@/views/IdeaFilter'
import CategIdeas from '@/views/CategIdeas'
import Login from '@/views/auth/Login'
import SignUp from "@/views/auth/SignUp";
import PswForgotStart from "@/views/auth/PswForgotStart"
import SetPswReset from '@/views/auth/PswReset'
import SetPswChange from '@/views/auth/ChangePsw'
import PswForgotFailure from "@/views/auth/MsgPswResetFailure"
import ProfileDetail from '@/views/auth/ProfileDetail'
import AccountProfile from '@/views/auth/AccountProfile'
import EditProfile from '@/views/auth/ProfileEdit'
import IdeasByTagSlug from '@/views/IdeasByTagSlug'
import IdeasByTagName from '@/views/IdeasByTagName'
import NotFound from '@/views/NotFound'

Vue.use(VueRouter)
// https://stackoverflow.com/questions/62462276 ow-to-solve-avoided-redundant-navigation-to-current-location-error-in-vue
const routerPush = Router.prototype.push
Router.prototype.push = function push(location) {
return routerPush.call(this, location).catch(error => error)
};

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: "/signup",
    name: "signup",
    component: SignUp,
  },
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/google-login",
    name: "google",
    component: Google,
  },
  {
    path: "/google",
    name: "google-form",
    component: GoogleForm,
  },
  {
    path: "/confirm-email-link/",
    name: "confirmEmail",
    component: ConfirmEmail,
  },
  {
    path: "/activate/:uid/:token",
    name: "activate",
    component: Activate,
    props:true
  },
  {
    path: "/reset-password/",
    name: "resetForgotPsw",
    component: PswForgotStart,
  },
  {
    path: "/password/reset/confirm/:uid/:token",
    name: "setPswReset",
    component: SetPswReset,
    props:true
  },
  {
    path: "/change-password/",
    name: "passwordChange",
    component: SetPswChange,
  },
  {
    path: "/reset-password-failure/",
    name: "resetForgotPswFailure",
    component: PswForgotFailure,
  },
  {
    path: '/general-ideas',
    name: 'ideaGeneral',
    component: IdeaGeneral
  },
  {
    path: '/idea-detail/:slug',
    name: 'ideaDetail',
    component: IdeaDetail
  },
  {   
    path: '/idea-create',
    name: 'ideaCreate',
    component: IdeaCreate
  },
  {   
    path: '/idea-edit/:slug',
    name: 'editIdea', 
    component: IdeaEdit
  },
  
  {
    // to render all ideas for a given tag slug (unique)
    path: '/tags-slug/:slug',
    name: 'ideasBySlug',
    component: IdeasByTagSlug
  },
  {
    // to render all ideas for a given tag name (unique)
    path: '/tags-name/:name',
    name: 'ideasByName',
    component: IdeasByTagName
  },
  {
    // to render all ideas for a given category
    path: '/category-idea/:slug',
    name: 'categ',
    component: CategIdeas
  },
  {
    path: '/idea/search/:term',
    name: 'search',
    component: IdeaSearch
  },
  {
    // path: '/idea/:sort/',
    path: '/idea/filter/:sort/:featured',
    name: 'filter',
    component: IdeaFilter,
   
  },
  {
    path: '/profile/:id',
    name: 'profile',
    component: ProfileDetail
  },
  // private profile routes
  {
    path: '/account-profile/:unid',
    name: 'accountProfile',
    component: AccountProfile
  },
  {
    path: '/profile-edit/:unid',
    name: 'editProfile',
    component: EditProfile
  },
  {
   path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '*',
    name: 'notFound',
    component: NotFound
  },
]
/* 
11.07.2021 : problem can't go back from not found page
missing param for named route "notFound": Expected "0" to be defined  
*/

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
