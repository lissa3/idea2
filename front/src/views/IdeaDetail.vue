<template>
<div class="container-fluid mt-3">
  <section  v-if="idea" class="jumbotron text-center">
        <div class="container banner">
          <h1 class="jumbotron-heading">Title: {{idea.title}} </h1>
          <div >
              <div class="idea-date  text-center">
                <span>{{idea.created_at| filterDateTime}}</span>
              </div>
               <!-- <div class="d-flex justify-content-around offset-md-2"> -->
               <!-- <div class="d-flex justify-content-around">
                <div>
                    <p><span>Rating: </span><b-icon-star-fill></b-icon-star-fill>
                      <span class="px-1"><strong>5</strong></span>
                    </p>
                </div>             
                <div>
                  <span><b-icon-heart-fill></b-icon-heart-fill><span class="px-1">{{idea.an_likes}}</span></span>
                 </div> 
              </div> -->
              <!-- <div>
                 <div class="box d-flex ">              
                  <p class="b1" @click="doStar(5)"><b-icon-star-fill></b-icon-star-fill></p> 
                  <p class="b2" @click="doStar(4)"><b-icon-star-fill></b-icon-star-fill></p> 
                  <p class="b3" @click="doStar(3)"><b-icon-star-fill></b-icon-star-fill></p> 
                  <p class="b4" @click="doStar(2)"><b-icon-star-fill></b-icon-star-fill></p> 
                  <p class="b5" @click="doStar(1)"><b-icon-star-fill></b-icon-star-fill></p>             
                </div> 
              </div>               -->
          </div>
          <div class="banner-collection">
            <div class="author-info d-flex align-items-center justify-content-around">              
              <b-avatar></b-avatar>
              <router-link :to="{name:'profile',params:{id:idea.author}}" class="px-2">
                {{idea.owner_idea}}
              </router-link>
            </div>
            <template v-if="!authorIsCurrentUser">
              <div class="follow-block">Follow</div>
              <!-- <div class="favorite-block d-flex justify-content-between align-items-center"> -->
              <div class="favorite-block d-flex">
                <p>Add to Favorite</p>
                <div class="col-lg-1 col-md-1 col-sm-1">
                  <b-icon icon="flower1"></b-icon>
                </div>
              </div>
            </template> 
            <template v-if="authorIsCurrentUser">
              <div class="edit-block">
                <router-link class="btn btn-outline-secondary btn-sm" :to="{name:'editIdea',params:{slug:idea.slug}}">
                  <b-icon-pencil></b-icon-pencil>Edit Idea 
                </router-link>
              </div>           
              <div class="delete-block">
                <div class="btn btn-danger btn-sm" @click="showModal">
                  <b-icon-trash></b-icon-trash>Delete Idea 
                </div>            
              </div>     
            </template>   
          </div>          
        </div>
    </section>    
    <section >
        <div v-if="isLoading"><app-loader></app-loader></div>  
        <div v-if="error" :message="error"><app-error-msg></app-error-msg>Ms</div>  
    </section>
<!-- body Idea -->
      <div v-if="idea" class="album py-5 ">
        <div class="container">
          <div class="row idea-container">
            <div class="col-xs-12">
              <div class="card mb-4 box-shadow">
                <div   class="col-lg-4 col-md-12 col-sm-12">
                    <div class="idea-img mb-2">
                        <div v-if="idea.thumbnail">
                            <img  :src="idea.thumbnail" alt="img idea">                            
                        </div>
                        <div v-else>
                          <img class="card-img-top"  style="height: 225px; width: 100%; display: block;" src="../assets/logo.png" data-holder-rendered="true">                        
                        </div>
                    </div>
                </div>  
                <!-- <div class="d-flex justify-content-end mt-3 px-3 "> -->
                <div class="d-flex justify-content-between mt-3 px-3 ">
                  <!-- <div class="d-flex justify-content-between"> -->
                   
                    <div class="d-flex justify-content-start">
                      <div class="lead">Current rating:&nbsp; </div>
                       <app-rating-show :rating="idea.avg_rate"></app-rating-show> 
                       <div><span class="px-1"><strong>&nbsp;&nbsp;{{idea.avg_rate}}</strong></span></div>                   
                   
                    </div>
<!-- add rating for auth-ed users                     -->
                <template v-if="isLoggedIn">
                    <div class="d-flex justify-content-start">
                      <div class="lead">Add  rating&nbsp; &nbsp; </div>
                      <div class="box d-flex px-1">              
                        <p class="b1" @click="doStar(5)"><b-icon-star-fill></b-icon-star-fill></p> 
                        <p class="b2" @click="doStar(4)"><b-icon-star-fill></b-icon-star-fill></p> 
                        <p class="b3" @click="doStar(3)"><b-icon-star-fill></b-icon-star-fill></p> 
                        <p class="b4" @click="doStar(2)"><b-icon-star-fill></b-icon-star-fill></p> 
                        <p class="b5" @click="doStar(1)"><b-icon-star-fill></b-icon-star-fill></p>             
                      </div>
                  </div>  
                </template>             
                  
                </div>
                <div class="d-flex justify-content-end mt-3 px-3 ">                  
                    <p v-if="thxRating" class="thanks">Thank you for giving a rating</p>                
                </div>         
                               
                <div class="card-text px-3 offset-md-2">
                    <div class="mb-2 text-left">
                      
                      <p>{{idea.lead_text}}Lorem ipsum dolor sit amet consectetur adipisicing elit. Consequatur architecto eum atque odio deserunt! Eaque velit possimus, repellat quis adipisci at accusamus dolores ex sequi corrupti fugiat delectus asperiores non.</p>
                      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sint suscipit laboriosam unde, vel nemo blanditiis voluptates? Perferendis similique qui labore porro aliquid, nobis quidem odio, quos neque aperiam placeat consectetur.</p>
                    </div>
                    <div class="idea-read-more mb-2">
                      <div v-if="idea.tags">                      
                        <div class="d-flex justify-content-left">
                          <div class="px-1">Tags:</div>
                          <app-tags-list :tags="idea.tags"></app-tags-list>                                  
                        </div> 
                      </div>                    
                    </div>
                  </div>
                  <div class="d-flex justify-content-between align-items-center px-3 mb-3">
                    <!-- <div class="btn-group">
                      <button type="button" class="btn btn-sm btn-outline-secondary">View</button>
                      <button type="button" class="btn btn-sm btn-outline-secondary">Edit</button>
                    </div> -->
                      <app-like 
                        :idea-id="idea.id" 
                        :idea-likes="idea.an_likes"
                        :is-logged-in="isLoggedIn"                                            
                        >
                      </app-like>
                    <small class="text-muted">9 mins</small>
                  </div>
                </div>
              </div>
            </div>            
        </div>
      </div>
<!-- Modal component should be at the bottom: otherwise possible issues with z-index and position fixed of the parent component -->
    <app-delete-idea-confirmation @close="close" v-if="makeModalVisible">
      <template v-slot:header>
        <h3>Warning</h3>
      </template>
      <template v-slot:body>
        <h4>Do you really want to delete this idea?</h4>
      </template>
      <template v-slot:modal-footer>
        <button class="btn btn-sm btn-danger" @click="deleteIdea(idea.slug)">
          Yes,I want to delete this idea
        </button>       
        <button class="btn btn-sm btn-success" @click="close">No</button>
      </template>
    </app-delete-idea-confirmation>
  </div>
</template>

<script>
import AppLoader from '@/components/Loader'
import AppErrorMsg from '@/components/ErrorMsg'
import AppDeleteIdeaConfirmation from '@/components/Modal.vue'
import AppRatingShow from '@/components/RatingShow'
import AppLike from '@/components/Like'
import AppTagsList from '@/components/TagsList'
import {mapState,mapGetters} from 'vuex'
import {actionTypes as singleIdeaActionType} from '@/store/modules/singleIdea'
import {getterTypes as authGetterTypes} from '@/store/modules/auth'




export default {
  name: 'AppIdeaDetail',
  components:{
    AppLoader,
    AppErrorMsg,
    AppDeleteIdeaConfirmation,
    AppTagsList,
    AppLike,
    AppRatingShow
  },
  data(){
    return{
      makeModalVisible: false,
      thxRating:null
      
      // ideaLikes:0 
    }
  },
  computed:{            
        ...mapState({            
            isLoading:state=>state.idea.isLoading,
            idea:state=>state.idea.data,
            error:state=>state.idea.error
        }),
        ...mapGetters({
          currentUser:authGetterTypes.currentUser,
          isLoggedIn:authGetterTypes.isLoggedIn
        }),
        authorIsCurrentUser(){
          // async req with unknown data (anonymous/user/user=== idea author)
          if(!this.currentUser||!this.idea.author){
            return false}
          console.log("calc if current user is the author")  
          return this.currentUser.id === this.idea.author          
        },
        showLike(){
          return this.ideaLikes
        }       
        
  },
  created(){
    this.getOneIdea()
  },
  methods:{
    getOneIdea(){
      console.log("component created")      
      this.$store.dispatch(singleIdeaActionType.getIdea,{slug:this.$route.params.slug})
      .then((resp)=>{
        // console.log("component calling; resp",resp)
        // console.log("with keys",Object.keys(resp))
        if(resp.status ===200){
          console.log("OK 200")
          // this.ideaObj = resp.data
        }else if(resp.status ===404){
          console.log("404 not found")
          this.$router.push({name:'notFound'})
        }
      })      
    },
    async doStar(rateNum){
      console.log(rateNum)      
      console.log("click on start",rateNum);  
      const ratingData = {'rating':rateNum} 
      const ratingInfo = {
                    rating:ratingData,
                    id:this.idea.id
        }; 
      console.log("rating to server",ratingInfo) 
      this.$store.dispatch(singleIdeaActionType.handleRating,ratingInfo)  
      .then((resp)=>{
        if(resp.status===200){
          console.log("dj serv give status 200")
          this.thxRating = true
           setTimeout(()=>{
                 this.thxRating = false
               },1000)
         
        }
      })      
    },      
    showModal(){
      console.log("user wants to delte his idea")
      this.makeModalVisible = true;
    },
    close() {
      console.log("closing modal");
      this.makeModalVisible = false;
    },
    deleteIdea(slug){
      this.makeModalVisible=false
      this.$store.dispatch(singleIdeaActionType.deleteIdea,{slug})
      .then((resp)=>{
        console.log("idea deleted with status 204",resp.status)
        this.$router.push({name:'ideaGeneral'})
      }).catch(err=>console.log("err from component",err))
    },
    
  },
  filters: {
    // Filter full date with (local+) time
    // 2020-07-23 20:41:43.833825
    filterDateTime(item) {
      let initialDate = new Date(item);
      return `
          ${initialDate.getDate()}.${
        initialDate.getMonth() + 1
      }.${initialDate.getFullYear()}-${initialDate.getHours()}:${initialDate.getMinutes()} UTC ${initialDate.getUTCHours()}:${initialDate.getMinutes()}`;
    },
    }    
}
</script>
<style scoped>
.banner{
  height: 300px;
  max-height: 350px;
  background-color: burlywood;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}
.idea-container{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.banner-collection{
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  align-content: center;

}
/* likes */
.click-like{
  cursor: pointer;
  padding:6px;
}

/* box with stars */
.box{
    direction:rtl;
    transition:0.3s all;
}
.box p{
    font-size:20px;
    color:rgb(240, 149, 29);
}
.box p:hover{
    color:black;
    cursor: pointer;
}
.b1:hover ~ p{
    color:black;
}
.b2:hover ~ p{
    color:black;
}
.b3:hover ~ p{
    color:black;
}
.b4:hover ~ p{
    color:black;
}
.b5:hover ~ p{
    color:black;
}

.thanks{
  background-color: rgb(229, 205, 173);
}
</style>
