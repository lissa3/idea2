<template> 
  <section class="row min-vh-100">
<!-- loader     -->
       <div class="col-xs-12 col-md-10 py-3 text-center offset-md-1">
              <app-loader v-if="isLoading"></app-loader>
            </div>
            <!-- errors          -->
<!-- django server is down ect-->
            <div class="warn mb-3" v-if="error">
              <div class="px-1">{{errors}}</div>
            </div>  
      <ul class="nav nav-tabs">
          <li class="nav-item">
                <a class="nav-link disabled" href="#">
                    <b-avatar size="48px"></b-avatar>
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#" active-class="active">Current Profile</a>
            </li>
            <li class="nav-item">                
                <router-link :to="{name:'editProfile',params:{unid:user.unid}}"
                class="nav-link" active-class="active"
                >Edit Profile
                </router-link>
               
                
            </li>
            <!-- <li class="nav-item disabled">
                <a class="nav-link" href="#">Edit Profile</a>
            </li> -->
            
        </ul>
      
      <div class="col-md-8 min-vh-100 mx-auto p-0">
        <div class="d-flex align-items-center 
                    justify-content-center 
                    flex-column
                    text-center
                    min-vh-100
                    ">
            <!-- style="max-width: 100%; width: 250px; object-fit: cover"          -->
            
            <div>        
              <div v-if="!noImgShow" >
                
                <img  :src="profile.image" alt="profile image">    
             </div>
             <div v-if="noImgShow" >
              <!-- style="max-width: 100%; width: 250px; object-fit: cover"   -->
              <b-avatar size="48px"></b-avatar>
            </div>
            </div>                   
            <!-- <img  v-else alt="profile image" class="rounded-circle" src="/220px.jpg"> -->
            <h1 class="display-4">Profile: {{profile.name}}</h1>
            <div class="d-flex align-items-start  flex-column text-left">
            <p class="lead px-2"><strong>Bio: </strong> {{profile.bio}}Where am ILorem ipsum dolor sit amet consectetur adipisicing elit. Cum itaque nam ipsa, officia fugiat maxime molestiae voluptas explicabo error, expedita autem suscipit, accusamus eligendi obcaecati corrupti culpa veniam eos nesciunt.
            </p>
            <p class="lead px-2" v-if="profile.website"><strong>Website:</strong>{{profile.website}}</p>
            <p class="lead px-2" v-if="profile.image"><strong>Website:</strong>{{profile.website}}</p>
            </div>
           
              <router-link :to="{name:'editProfile',params:{unid:user.unid}}"> <button type="button" class="btn btn-secondary btn-lg">Edit
            </button></router-link>
            </div>
            
        
      </div>
    
  </section> 
</template>
            
<script>

import {mapState} from 'vuex'
import {mapGetters} from 'vuex'
import {getterTypes} from '@/store/modules/auth'
import AppLoader from '@/components/Loader'
export default {
  name:'AccountProfile',
  components:{
    AppLoader
  },
  computed:{
      ...mapGetters({
            user:getterTypes.currentUser
      }),
      ...mapState({            
            profile:state=>state.profile.data,
            isLoading:state=>state.ideas.isLoading,
            error:state=>state.ideas.error,
                      
        }),
    noImgShow(){      
      return this.profile.image===null   
     
        
      }
    
  }
}
</script>
<style scoped>
/* .custom-wrap{
  background-color: blanchedalmond;
}  */
.link-decor{
  color:black;
  text-decoration:none;
}
.link-decor:hover{
  color:rgb(221, 216, 216);
}
body {
  height: 100vh;
  margin: 0; padding: 0;
}
  /* display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;

  font-family: 'Nunito', sans-serif;
  background-color: blanchedalmond; 

 main {
    height: 100%;
    width: 100%;

    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: row;
}
.card {
      width: 470px;
      min-height: 185px;
      display: flex;

      padding: 10px;
      border-radius: 5px;
      
      background: rgba(255, 255, 255, .8);
}
.avatar {
        width: 100px;
        height: 100px;
        margin-right: 10px;
        border-radius: 50%;
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
        border: 4px solid rgba(255, 255, 255, .5);
}

 */  

</style>
