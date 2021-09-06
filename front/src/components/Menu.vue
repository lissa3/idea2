<template>
<div>
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
        <!-- <b-nav-item href="#">Link</b-nav-item>
        <b-nav-item href="#">Anonymous</b-nav-item> -->
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
      

      <!-- Right aligned nav items d-flex justify-content-between-->
      <b-navbar-nav class="ml-auto">
        <b-nav-form class="">
          <b-form-input v-model="term" size="sm" class="mr-2 pt-2 top-adjust" placeholder="Search"></b-form-input>
          <b-button @click="doSearch" size="sm" class="" type="submit">Search</b-button>

          <!-- <b-form-input v-model="term" size="sm" class="mr-sm-2" placeholder="Search"></b-form-input> -->
          <!-- <b-button @click="doSearch" size="sm" class="my-2 my-sm-0" type="submit">Search</b-button> -->
        </b-nav-form>       
      <template v-if="isLoggedIn">
          <b-nav-item href="#" >
            <router-link :to="{ name: 'ideaCreate' }" class="link-decor" active-class="active"
              >New Idea</router-link>
        </b-nav-item>
          <!-- <b-nav-item href="#">IsLoggedIn</b-nav-item>               -->
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
                <b-icon-tools></b-icon-tools>
              </template>
              <b-dropdown-item href="#" @click="showProfile">Profile</b-dropdown-item>
              <b-dropdown-item href="#" @click="changePsw">Change Password</b-dropdown-item>
              <b-dropdown-item href="#" @click="deleteAccount" class="danger">Delete Account</b-dropdown-item>
            </b-nav-item-dropdown>  
      </template>
        
        
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
</header>  
  <app-delete-account-confirmation v-if="makeModalVisible" @close="close" @deleteAccount="deleteAccount">
    <template v-slot:header>
        <h3>Warning</h3>
    </template>
      <template v-slot:body>
        <h4>Do you really want to delete your account?</h4>
    </template>
    <template v-slot:modal-footer>
        <button class="btn btn-sm btn-danger" @click="confirmDeleteAccount">
          Yes,I want to delete my account
        </button>       
        <button class="btn btn-sm btn-success" @click="close">No</button>
    </template>
  </app-delete-account-confirmation>
</div> 
</template>
<script>
import {mapGetters} from 'vuex'
import {actionTypes} from '@/store/modules/auth'
import {actionTypes as profileActionTypes} from '@/store/modules/profile'
import {getterTypes} from '@/store/modules/auth'

import AppDeleteAccountConfirmation from '@/components/Modal.vue'


export default {
    name:'Menu',
    components:{
      AppDeleteAccountConfirmation
    },
    data(){
      return {
        term:'',
        makeModalVisible: false,
        
      }
    },
    computed:{
      ...mapGetters({
        currentUser:getterTypes.currentUser,
        isLoggedIn:getterTypes.isLoggedIn,
        isAnonymous:getterTypes.isAnonymous,
        // foo: gT.fooProfile
        }),
        
          
     
    },
    methods:{
      doSignOut(){
        // console.log("Sign out...")
        console.log(actionTypes.signOut)
        this.$store.dispatch( actionTypes.signOut)
        window.location.reload()
        
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
        //  console.log("looking for profile",this.currentUser.unid)
         const unid = this.currentUser.unid
         console.log(this.$store.state.profile.myprofile)
         this.$store.dispatch(actionTypes.getUser)
         this.$store.dispatch(profileActionTypes.showPersonalInfo,unid)
        .then((resp)=>{
          if(resp.status===200){
            console.log("from store status 200?",resp.status)
            this.$router.push({name:'accountProfile',params:{unid}})
          }else if(resp.status===401){
            this.$router.push({name:'login'})
          }else if(resp.status===500){
            alert("err 500 from Menu")
            
          }else{
            console.log("gor from store: status",resp.status)
            console.log("pushing to account Profile")
            this.$router.push({name:'accountProfile',params:{unid}})
          }
        })          
        .catch((err)=>{
          console.log(err.servDown)
          this.$router.push({name:'accountProfile',params:{unid}})
        })
      },
      deleteAccount(){
        console.log("user wants to delete his account")        
        this.makeModalVisible = true;
        this.$router.push({name:'deleteAccount'})
      },
      //close modal
      close(){
        this.makeModalVisible = false
        this.$router.push({name:'home'})
      },
      confirmDeleteAccount(){
        console.log("confirm delete account")
         this.makeModalVisible=false
        // this.$store.dispatch(singleIdeaActionType.deleteIdea,{slug})
      }
      
    },
    mounted(){
      this.$store.dispatch(actionTypes.getUser)
      // console.log("action type from menu", actionTypes.getUser)
      // console.log("menu mounted, call for getUser from store")
    },
    created(){
     setInterval(()=>{ 
       // sending request for a new access token each 60 min
       console.log("setimeout calling, time is voorbij, asking for a new access token")
       let refresh = localStorage.getItem('refreshToken')
      //  let access = localStorage.getItem('accessToken')
      //  console.log("access is is",access)
       this.$store.dispatch(actionTypes.fetchFreshAccessToken,refresh) 
       }, 600000);
      //  this.$store.dispatch(actionTypes.fetchFreshAccessToken,refresh) 
      //  }, 3600000);
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
.dropdowm-item .danger{
  color:red;
  background-color: burlywood;
}
/* input search form */
.top-adjust{
  margin-top:20px;
  padding-top:16px;
  margin-bottom:20px;
}
</style>
