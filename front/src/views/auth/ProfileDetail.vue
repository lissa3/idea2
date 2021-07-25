<template> 
  <section class="row min-vh-100">
      <div class="col-md-10 min-vh-100 mx-auto p-0">
        <div class="d-flex align-items-center 
                    justify-content-center 
                    flex-column
                    text-center
                    min-vh-100
                    custom-wrap">
            <!-- style="max-width: 100%; width: 250px; object-fit: cover"          -->
            
            <div>        
              <div v-if="!noImgShow" >
                
                <img  :src="profile.image" alt="profile image">    
             </div>
             <div v-if="noImgShow" >
              <!-- style="max-width: 100%; width: 250px; object-fit: cover"   -->
              <b-avatar size="144px"></b-avatar>
            </div>
            </div>                   
            <!-- <img  v-else alt="profile image" class="rounded-circle" src="/220px.jpg"> -->
            <h1 class="display-4">Profile: {{profile.name}}</h1>
            <div class="d-flex  mx-auto">
            <p class="mb-3 lead"><strong>Bio: </strong> {{profile.bio}}Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum itaque nam ipsa, officia fugiat maxime molestiae voluptas explicabo error, expedita autem suscipit, accusamus eligendi obcaecati corrupti culpa veniam eos nesciunt.
            </p>
            <p v-if="profile.website">Website: {{profile.website}}</p>
            <p class="lead px-2" v-if="profile.image"><strong>Website:</strong>{{profile.website}}</p>
            </div>
            <button type="button" class="btn btn-success btn-lg">
              Contact
            </button>
        </div>
      </div>
  </section> 
</template>
            
<script>
// import {actionTypes} from '@/store/modules/profile'
// import simpleAPI from '@/api/plainAxios'
export default {
  name:'ProfileDetail',
  data(){
      return {
          profile:{}
      }
  },
  methods:{
      // showProfile(){        
      //   this.$store.dispatch(actionTypes.retrieveProfile,this.$route.params.id)
      //    .then((resp)=>{
      //        console.log(resp)
      //         if(resp.status === 200){
      //             this.profile = resp.data
      //         }
      //    })
      //    .catch(err=>console.log(err))

      // }
  },
  created(){
      // this.showProfile()
  },
  computed:{
    noImgShow(){      
      return this.profile.image===null   
     
        
      }
    
  }
}
</script>
<style scoped>
.custom-wrap{
  background-color: blanchedalmond;
} 
</style>
