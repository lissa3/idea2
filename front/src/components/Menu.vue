<template>
<header >     
<div>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#"><b-icon-house-door></b-icon-house-door></b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="#">
          <router-link :to="{ name: 'home' }" class="link-decor" exact active-class="active">Home</router-link> 
        </b-nav-item>
      <template v-if="isAnonymous">
        <b-nav-item href="#">Link</b-nav-item>
        <b-nav-item href="#">Anonymous</b-nav-item>
        <b-nav-item href="#" >
            <router-link :to="{ name: 'login' }" class="link-decor" active-class="active">Login</router-link>
          </b-nav-item>
        <b-nav-item href="#" >
            <router-link :to="{ name: 'signup' }" class="link-decor" active-class="active">SignUp</router-link>
        </b-nav-item>
        <b-nav-item href="#" >
            <router-link :to="{ name: 'google' }" class="link-decor" active-class="active"
              >Login via Google</router-link>
        </b-nav-item>
      </template>       

      <b-nav-item href="#"><router-link :to="{ name: 'ideaGeneral' }" class="link-decor" active-class="active"
              >Ideas</router-link></b-nav-item>
      </b-navbar-nav>
      <b-nav-item href="#" >
            <router-link :to="{ name: 'ideaCreate' }" class="link-decor" active-class="active"
              >New Idea</router-link>
      </b-nav-item>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-form>
          <b-form-input v-model="term" size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
          <b-button @click="doSearch" size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
        </b-nav-form>       
      <template v-if="isLoggedIn">
          
          <b-nav-item href="#">IsLoggedIn</b-nav-item>              
          <b-nav-item href="#" >
            <a href="#" @click="doSignOut" class="link-decor" >Sign Out</a>
          </b-nav-item> 
          <b-nav-item href="#" >
            <b-icon icon="person-fill"></b-icon>
            <a href="#" class="link-decor" >Welcome, &nbsp;{{currentUser.username}}</a>
          </b-nav-item>
          <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template #button-content>
            <em>User</em>
          </template>
            <b-dropdown-item href="#" @click="showProfile">Profile</b-dropdown-item>
            <b-dropdown-item href="#" @click="changePsw">Change Password</b-dropdown-item>
            <!-- <b-dropdown-item href="#">Sign Out</b-dropdown-item> -->
            </b-nav-item-dropdown>  
          </template>
        
        
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
</header>   
</template>
<script>
import {actionTypes} from '@/store/modules/auth'
import {actionTypes as profileActionTypes} from '@/store/modules/profile'
import {getterTypes} from '@/store/modules/auth'
import {mapGetters} from 'vuex'
export default {
    name:'Menu',
    data(){
      return {
        term:''
      }
    },
    computed:{
      ...mapGetters({
        currentUser:getterTypes.currentUser,
        isLoggedIn:getterTypes.isLoggedIn,
        isAnonymous:getterTypes.isAnonymous})
      // currentUser(){
      //   return this.$store.getters[getterTypes.currentUser]
      // },
     
     
    },
    methods:{
      doSignOut(){
        // console.log("Sign out...")
        console.log(actionTypes.signOut)
        this.$store.dispatch( actionTypes.signOut)
        location.reload();
      },
      doSearch(){
        this.$router.push({name:'search',params:{term:this.term}})       
        this.term = ''
      },
      changePsw(){
        console.log("user wants to change psw")
        this.$router.push({name:'passwordChange'}) 
        
      },
      showProfile(){
        console.log("looking for profile",this.currentUser.unid)
        const unid = this.currentUser.unid
        console.log("str url",profileActionTypes.showPersonalInfo)
        this.$store.dispatch(profileActionTypes.showPersonalInfo,unid)
        .then((resp)=>{
          if(resp.status===200){
            this.$router.push({name:'accountProfile',params:{unid}})
          }
        })          
        .catch(err=>console.log(err))
      }
    },
    mounted(){
      this.$store.dispatch(actionTypes.getUser)
      // console.log("action type from menu", actionTypes.getUser)
      // console.log("menu mounted, call for getUser from store")
    }
}
</script>

<style scoped>
.menu-nav{
    background-color: bisque;
}
.bg-info-2{
  background-color: brown;
  color:white;
}
.link-decor{
  color:white;
  text-decoration:none;
}
.link-decor:hover{
  color:rgb(221, 216, 216);
}
.active{
  background-color: rgb(245, 239, 239);
  color:black;
  padding:5px 10px;
  border: 1px solid white;
  border-radius: 3px;
}
</style>
