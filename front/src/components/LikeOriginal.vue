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
   
        
    
</div>
</template>

<script>
import {actionTypes as singleIdeaActionType} from '@/store/modules/singleIdea'
export default {
    name:'Like',
    props:{
        id:{
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
            likeToToggle:false,         
            newLikeVal:this.ideaLikes,
            likeStatus:null,
            needAuthMsg:null        
        }
    },
    methods:{
        async doLike(){
        // console.log("like now is:",this.likeToToggle)    
        // boolean likeToToggle for serv data 
        this.likeToToggle = !this.likeToToggle
        const likeInfo = {
                    like:{"like":this.likeToToggle},
                    id:this.id
        };
        this.$store.dispatch(singleIdeaActionType.handleLike,likeInfo)
        .then((servResp)=>{
            if(servResp.status===200){
                this.likeStatus = servResp.data.like
                if(this.likeStatus===true){
                    this.newLikeVal ++                    
                }else{
                    this.newLikeVal = this.newLikeVal -1                
                }                
                // console.log("to parent from child",{id:this.id,like:this.likeStatus})
                // this.$emit('zoo',{id:this.id,like:this.likeStatus})
                this.likeStatus = !this.likeStatus
            }else if(servResp.status === 401){
                console.log("you are not auth-ed????")
                this.needAuthMsg = 'You need to be auth-ed to like'                 
                setTimeout(()=>{
                    this.needAuthMsg = null
               },1000)
            }
          })
          .catch(err=>console.log("err in like",err))
      
    }, 

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