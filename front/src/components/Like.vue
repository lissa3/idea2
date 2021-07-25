<template>

<div class="list-group list-group-horizontal">
    <div :class="{'btn':true,'btn-sm':true,
                'disabled':!isLoggedIn, 
                'btn-outline-secondary':likeToToggle,
                'btn-outline-success':!likeToToggle}"
         @click="doLike" :disabled="!isLoggedIn">
        <div class="click-like">
          <div class="px-1 ">Like &nbsp; <b-icon-heart-fill></b-icon-heart-fill><span class="px-1"></span></div>

        </div>
    </div>
    <div class="px-2 zoo">
            <span class="px-1" v-if="likeStatus===null">{{ideaLikes}}</span>
            <span class="px-1" v-else>{{newLikeVal}}</span>
            
    </div> 
    <p v-if="needAuthMsg" class="warning">msg: {{needAuthMsg}}</p>
    <!-- <p>{{localNewLike}}</p> -->
   
        
    
</div>
</template>

<script>
import {actionTypes} from '@/store/modules/singleIdea'
export default {
    name:'Like',
    props:{
        ideaId:{
            type:Number,
            required:true
        },
        ideaLikes:{
            type:null||Number,
            // required:true
        },
        isLoggedIn:{
            type:Boolean,
            required:true
        }
    },
    data(){
        return{        
            likeToToggle:null, 
            initialLikeState:null,        
            newLikeVal:this.ideaLikes,
            likeStatus:null,
            needAuthMsg:null,
            localNewLike:{count:null,initialAction:null}       
        }
    },
    methods:{
        async doLike(){
            // console.log("initial like",this.likeToToggle)
            this.likeToToggle = !this.likeToToggle
            // console.log("dus i send != state of like",this.likeToToggle)
            const likeInfo = {
                        like:{"like":this.likeToToggle},
                        id:this.ideaId
            };
            this.$store.dispatch(actionTypes.handleLike,likeInfo)
            .then((servResp)=>{
                if(servResp.status===200){
                    this.likeStatus = servResp.data.like
                    console.log("dj server confirms data in db",this.likeStatus)
                    if(this.likeStatus===true){
                        // console.log("like plus: +=")   
                        this.newLikeVal ++                   
                    }else{
                        // console.log("minus like:-=")
                        this.newLikeVal -= this.newLikeVal                                            
                    }  
                    // this.likeStatus = !this.likeStatus             
                    
                    
                }else if(servResp.status === 401){
                    console.log("you are not auth-ed????")
                    this.needAuthMsg = 'You need to be auth-ed to like'                 
                    setTimeout(()=>{
                        this.needAuthMsg = null
                },1000)
                }        
            }).catch(err=>console.log("err in like",err))        
        
            },
        async getInitialLikeState(){
            // console.log("requesting initial like state",this.ideaId)
            this.$store.dispatch(actionTypes.getLikeState,this.ideaId)
            .then((servResp)=>{
                if(servResp.status===200){
                    this.likeToToggle = servResp.data.like
                }
            })
            .catch(err=>console.log(err))
        } 

    },
    created(){
        this.getInitialLikeState()
    }
}
         

</script>
<style scoped>
.click-like{
  cursor: pointer;
  padding:3px;
  
}
.zoo{
    display: flex;
    flex-direction: column;
    justify-content: center;

}
.warning{
    background-color: coral;
    border-radius: 5px;
    padding: 3px 10px;
}
</style>