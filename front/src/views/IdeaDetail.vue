<template>
    <div class="container-fluid mt-3">
        <section  v-if="idea" class="jumbotron text-center px-2 py-2">
            <div class="container banner">
            <h1 class="jumbotron-heading">Title: {{idea.title}} </h1>
            <div >
                <div class="idea-date  text-center">
                    <span>{{idea.created_at| filterDateTime}}</span>
                </div>             
            </div>
            <div class="banner-collection">
                <div class="author-info d-flex align-items-center justify-content-around">              
                <b-avatar></b-avatar>
                <router-link :to="{name:'profile',params:{id:idea.author}}" class="px-2">
                    {{idea.owner_idea}}
                </router-link>
                </div>
                <template v-if="!isAnonym">
              <div v-if="!authorIsCurrentUser">
                <button type="button" class="btn btn-secondary" @click="addToFollow(idea.author)">
                   Follow
                </button>
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
        </section >
        <section >
    <div v-if="isLoading"><app-loader></app-loader></div>  
    <div v-if="error" :message="error"><app-error-msg></app-error-msg>Ms</div>  
        </section>
    <!-- flash messages: following OK and Failure -->
        <section>
        <div v-if="addToFollowMsg" class="flash-msg px-1 py-2 mb-2 pb-4">Successfully added to Following</div>
        <div v-if="errMsg" class="flash-msg-warning px-1 py-2 mb-2 pb-4">Sorry.Something went wrong.Try to add authore later</div>
        
        </section>
    <div v-if="idea" class="py-2 ">
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
                <div class="d-flex justify-content-between mt-3 px-3 ">                 
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
                      <div v-if="idea.tags.length>0">                      
                        <div class="d-flex justify-content-left">
                          <div class="px-1">Tags:</div>
                          <app-tags-list :tags="idea.tags"></app-tags-list>                                  
                        </div> 
                      </div>                    
                    </div>
                  </div>
                  <div class="d-flex justify-content-between align-items-center px-3 mb-3">
                      <app-like 
                        :idea-id="idea.id" 
                        :idea-likes="idea.an_likes"
                        :is-anonym="isAnonym"                                            
                        >
                      </app-like>
                      <div>  
                        <!-- <div v-if="idea.users_comments>0">
                          <button type="button" class="btn btn-sm btn-outline-secondary" @click="fetchComments(idea.slug)">
                          Show Comments ({{idea.users_comments}})
                        </button>    
                        </div>   -->
                        <p v-if="!idea.users_comments">                 
                          No comments yet
                        </p>                          
                      </div>                     
                    <small class="text-muted">9 mins</small>
                  </div>
                  <div v-if="currentUser">
                  <div class="d-flex justify-content-between align-items-center px-3 mb-3">
                    <div class="">
                      <button type="button" class="btn btn-sm btn-success" @click="showCommentForm">
                        Leave a comment
                      </button>                      
                    </div>                  
                  </div>
                  </div>
              </div>
            </div> 
         </div>
     </div>      
   </div>
   <!-- start comment  form-->
    <div class="mb-5"  :class="startComment?'show-comment-form':'comment-form-invisible'">
          <form @submit.prevent="addComment">  
            <div class="form-group">
              <label for="body">Leave you comment here, please</label>
                <textarea id="body" 
                cols="30" rows="5"
                v-model="commentBody"
                placeholder="Remember, be nice"></textarea>
            </div>           
            <input type="submit" class="">
          </form>
    </div>
<!-- end comment form -->
        <div class="row">
            <div v-if="idea">            
            <app-comm-list  :idea-slug="idea.slug"></app-comm-list>
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
import AppCommList from '@/components/comments/CommList'
import {mapState,mapGetters} from 'vuex'
import {getterTypes as authGetterTypes} from '@/store/modules/auth'
import {actionTypes as commentActionType} from '@/store/modules/comments'
import {actionTypes as followActionType} from '@/store/modules/follow'
import {actionTypes as singleIdeaActionType} from '@/store/modules/singleIdea'

export default {
  name: 'AppIdeaDetail',
  components:{
    AppLoader,
    AppErrorMsg,
    AppDeleteIdeaConfirmation,
    AppTagsList,
    AppLike,
    AppRatingShow,
    AppCommList
  },
  data(){
    return{
      makeModalVisible: false,
      thxRating:null,
      addToFollowMsg:false,
      errMsg:false,
      netWorkErr:false,      
      // comment form (idea in mapState)
      startComment:false,
      commentBody:null,
      //comment err
    }
  },
  computed:{            
        ...mapState({            
            isLoading:state=>state.idea.isLoading,
            idea:state=>state.idea.data,
            error:state=>state.idea.error,
            treeDataComments:state=>state.comments.data,
            commentsErr:state=>state.comments.error,
            commentsisLoading:state=>state.comments.isLoading
        }),
        ...mapGetters({
          currentUser:authGetterTypes.currentUser,
          isLoggedIn:authGetterTypes.isLoggedIn,
          isAnonym:authGetterTypes.isAnonymous
        }),
        authorIsCurrentUser(){
          // button "Follow" will be displayed for all auth-ed users besides idea's author self          
          if(!this.currentUser||!this.idea.author){
            return false}
          // console.log("calc if current user is the author")  
          return this.currentUser.id === this.idea.author          
        },
        // showLike(){
        //   return this.ideaLikes
        // }, 
                 
        
  },
  created(){
    this.getOneIdea()
  },
  methods:{
    getOneIdea(){
      console.log("component created, slug:",this.$route.params.slug)      
      this.$store.dispatch(singleIdeaActionType.getIdea,{slug:this.$route.params.slug})
      .then((resp)=>{
        // console.log("component calling; resp",resp)
        // console.log("with keys",Object.keys(resp))
        if(resp.status ===200){
          // console.log("OK 200")
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
    addToFollow(authorId){
      console.log("adding to following",authorId)
      this.$store.dispatch(followActionType.addToFollowing,{authorId})
      .then((resp)=>{
        console.log("resp",resp)
        if(resp.servDown){
          setTimeout(()=>{
          this.errMsg = false
          },2000)
        }else{
          console.log("resp",resp.status)
          this.addToFollowMsg = true
          setTimeout(()=>{
            this.addToFollowMsg = false
            },4000)
        }
      })
      .catch((err)=>{
        console.log(err)
        this.errMsg = true
        setTimeout(()=>{
          this.errMsg = false
          },2000)
      })
    },
    showCommentForm(){
      console.log("sending comment to ... from ..")
      this.startComment = !this.startComment
    },
    addComment(){
      console.log("adding comment...")
      let commentBody = this.commentBody
      let ideaId = this.idea.id
      console.log("line 364 id of idea is",this.idea.id)
      let commentData = {
        body: commentBody,
        idea:ideaId,
        parent:null,
        }
        console.log("data to store to dispatch",commentData)
        this.$store.dispatch(commentActionType.sendRootComm,commentData)
        .then((resp)=>{
          console.log("resp",resp.status)
          if(resp.servDown){
            this.netWorkErr = true
          }else if(resp.status===201){
            // if comment successfully created: hide comment form and clear comment body
            this.startComment = false
            this.commentBody = null
            // does not work this.$router.push({name:'ideaDetail',params:{slug:this.idea.slug}})
          }else if(resp.status===500){
            this.errMsg = true
          }
        })
        .catch(err=>console.log('final error',err))
    },
    fetchComments(ideaSlug){
      console.log("fetching comments",ideaSlug)
      this.$store.dispatch(commentActionType.fetchCommentList,ideaSlug)
      .then((resp)=>{
        console.log(resp.status)
      })
      .catch(err=>console.log(err))
    }  
    
  },
  filters: {
    // Filter full date with (local+) time
    // 2020-07-23 20:41:43.833825
    filterDateTime(item) {
      let initialDate = new Date(item);
      return `
          ${initialDate.getDate()}.${
        initialDate.getMonth() + 1
      }.${initialDate.getFullYear()} at ${initialDate.getHours()} h :${initialDate.getMinutes()} min
      (Universal Time: ${initialDate.getUTCHours()} h ${initialDate.getMinutes()} min)`;
    },
    }    
}
</script>
<style scoped>
.banner{
  height: 200px;
  max-height: 250px;
  background-color: #e2ede8;
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
/* flash msg at the top when req OK */
.flash-msg{
  height: 40px;
  background-color:#caefde;
  text-align: center;
  font-size: 20px;
}
.flash-msg-warning{
  height: 40px;
  background-color:#eed2c4;
  text-align: center;
  font-size: 20px;
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
/* comment form  */
.comment-form-invisible{
  display: none;
}
.show-comment-form{
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  min-height: 100px;
  max-width: 100%;
  padding: 0.5rem 1rem;
  border:1px solid black;
}
/* comment button */
input[type=submit] {
  background-color: #e2cca8;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
input[type=submit]:hover {
  background-color: #d1860c;
}
input[type=text],  textarea {
  width: 100%; 
  padding: 12px; 
  border: 1px solid #ccc;
  border-radius: 4px; 
  box-sizing: border-box;
  margin-top: 6px; 
  margin-bottom: 16px; 
  resize: vertical;
  outline:none;
  /* for scroll-bar in IE */
  overflow: auto;
  
}
/* textarea focus {background-color:#000;color:#FFF;} */
/* comments to display */

.comment-body{
  border:1px solid black;
  border-radius: 3px; 
}
.left-shift {
  text-align: left;
  padding: 0.2rem 0 0.5rem 0.5rem;
  margin-left: 1rem;
  /* margin-left: 0.5rem; */
  cursor: pointer;
}
.label-wrapper {
  padding-bottom: 10px;
  margin-bottom: 10px;
  border-bottom: 1px solid #ccc;
  cursor: pointer;
}
.comm-deleted{
  background-color:#faf3f4f7;
  border-radius: 3px;
  
  max-width: 100%;
}
</style>
