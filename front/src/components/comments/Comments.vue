<template>
    <div>
        <section class="row">                   
            <div v-if="isLoading" class="col-md-12">
                <app-loader></app-loader>
            </div>

            <div class="col-md-12" v-if="isLoggedIn">
                <h5>Write your comment</h5>
                <app-comment-form
                submitLabel="Write"
                :clean-form = "cleanForm"
                @addRootComment="addRootComment">
                </app-comment-form>
            </div>        
            <div  class="comment-list ml-2 col-md-12">
                <div class="section-comments">
                    <h4>Comments</h4>                
                    <div v-if="warning" class="warning px-1 py-1">{{warning}}</div>                         
                </div>                              
                <app-comment 
                v-for="comment in getRootComms"
                :key="comment.id"
                :comment="comment"
                :parent-id="comment.id"
                :active-comment="activeComment"                
                :comments="comments"
                :depth=1
                @replyComment="replyComment"
                @updateComment="updateComment"
                @commEdit="handleEdit"
                @commReply="handleReply"
                @commDelete="handleDelete"
                @handleCancel="handleCancel"                
                ></app-comment>                               
            </div>
            <div v-if="error">Smth went wrong</div>                 
        </section>
    </div>    
</template>

<script>
import AppCommentForm from '@/components/comments/CommentForm.vue'
import AppComment  from '@/components/comments/Comment'
import AppLoader from '@/components/Loader'
import {actionTypes} from '@/store/modules/comments'
import {mapState} from 'vuex'
import {mapGetters} from 'vuex'
import {getterTypes} from '@/store/modules/auth'

export default {
    name:'AppCommentList',
    components:{       
        AppLoader, 
        AppComment,
        AppCommentForm,
               
    },
    data(){
        return {
            activeComment:null,
            cleanForm:false,
            warning:'',            
        }
    },
    props:{        
        ideaId:{
            type:Number,
            required:true
        },
        ideaSlug:{
            type:String,
            required:true
        },
        currentUser:{
            type:Object,
            required:false
        }        
    },
    created(){       
      this.$store.dispatch(actionTypes.fetchCommentList,this.ideaSlug)
        
    },
    methods:{
        // methods to set active comment 
        handleReply(commId){           
            this.activeComment={id:commId,type:'replying'}
            //console.log("parent sets type",this.activeComment.type)
        },
        handleEdit(commId){            
            this.activeComment={id:commId,type:'editing'}
            //console.log("parent sets type",this.activeComment.type)
        },
        handleDelete(commId){
            this.activeComment={id:commId,type:'deleting'}
            //console.log("parent delete comm ",commId)
            this.deleteComment(commId)
        },
        handleCancel(){
            console.log("parent caught cancel signal")
            this.activeComment = null
        }, 
        
        replyComment(replyComment){
            console.log("adding reply com")        
            console.log("line 99 data",replyComment)
            console.log("parent is(line 100",replyComment.parent)            
            let commentData = {
                body: replyComment.body,
                idea:this.ideaId,
                parent:replyComment.parent,
                }
                console.log("data",commentData)
                this.$store.dispatch(actionTypes.sendRootComm,commentData)
                .then((resp)=>{
                console.log("resp",resp)
                this.activeComment = null
                console.log("replied done, active comment null")
                })
                .catch(err=>console.log(err))    
        },       
        addRootComment(data){
            console.log("adding root comment...")        
            // let user = this.currentUser
            console.log("line 92 data",data)            
            let commentData = {
                body: data.body,
                // user: user,
                idea:this.ideaId,
                parent:null,
                }
                console.log("data",commentData)
                this.$store.dispatch(actionTypes.sendRootComm,commentData)
                .then((resp)=>{
                console.log("resp",resp)
                    if(resp.status===201){
                        console.log("successfully created a new comment")
                        this.activeComment=null
                        this.cleanForm = true
                        console.log("add root comment done, active comment null")
                    }
                    
                    })
                .catch(err=>console.log(err))        
        },
        updateComment(data){
            console.log("edit comm line 118 comments.vue",data) 
            this.$store.dispatch(actionTypes.editComm,data)
                .then((resp)=>{
                console.log("resp",resp)
                if(resp.status===403){
                    console.log("permission denied")
                    this.warning = "Permission denied"
                }
                    this.activeComment=null
                    console.log("update comment done, active comment null")
                })
                .catch(err=>console.log(err))        
        }, 
        deleteComment(commId){
            console.log("sending request to th edj server to delete com",commId)
            this.$store.dispatch(actionTypes.deleteComm,commId)
            .then((resp)=>{
                console.log(resp.status)
            })
            .catch(err=>console.log(err))
        }       
    },    
    computed:{
        ...mapState({
            isLoading: state=> state.comments.isLoading,
            error: state=>state.comments.error,
            comments:state=>state.comments.data,
            fladToRednder:state=>state.comments.flagRerender

        }),
         ...mapGetters({        
            isLoggedIn:getterTypes.isLoggedIn,        
        // foo: gT.fooProfile
        }),
        getRootComms(){
            // console.log(this.comments.filter(comm=> comm.parent === null))
            // console.log("length root:",this.comments.length)
            if(this.comments){
                return  this.comments.filter(comm=> comm.parent === null)

            }else{
                return []
            }        
        },    
    },
    
}

</script>
<style scoped>
.section-comments {
  text-align: left;
  text-decoration: none;
  list-style: none;
  padding-left: 1rem;
  margin-left: 1rem;
}
.warning{
    background-color: rgb(240, 228, 230);
    max-height: 150px;
    max-width: 100%;
    border-bottom-color: red;  

}

</style>