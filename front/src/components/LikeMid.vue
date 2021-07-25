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
            <!-- <span class="px-1" v-else>{{newLikeVal}}</span> -->
            <span class="px-1" v-else>{{localNewLike.count}}</span>

    </div> 
    <p v-if="needAuthMsg" class="warning">msg: {{needAuthMsg}}</p>
    <p>{{localNewLike}}</p>
   
        
    
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
            likeToToggle:false, 
            initialLikeState:null,        
            newLikeVal:this.ideaLikes,
            likeStatus:null,
            needAuthMsg:null,
            localNewLike:{count:null,initialAction:null}       
        }
    },
    methods:{
        async doLike(){
            // console.log("this local",this.localNewLike)
        // console.log("like now is:",this.likeToToggle)    
        // boolean likeToToggle for serv data 
        this.likeToToggle = !this.likeToToggle
        //local change likes
        if(this.localNewLike.count&&this.localNewLike.initialAction==='+'){
            console.log("count is not null after prev + and going to -")
            this.localNewLike.count -= 1
            this.localNewLike.initialAction = '-'
        }else if(this.localNewLike.count&&this.localNewLike.initialAction==='-'){
            console.log("count is not null after prev - and going to +")
            this.localNewLike.count +=1
            this.localNewLike.initialAction = '+'
        }
        
        const likeInfo = {
                    like:{"like":this.likeToToggle},
                    id:this.id
        };
        this.$store.dispatch(actionType.handleLike,likeInfo)
        .then((servResp)=>{
            if(servResp.status===200){
                this.likeStatus = servResp.data.like
                console.log("user gives plus,server responsed with like",this.likeStatus)
                if(this.likeStatus===true){
                    this.newLikeVal ++ 
                    if(this.localNewLike.count===null){
                        console.log("initial count is null ",this.localNewLike.count)
                        this.localNewLike.initialAction = '+'
                        this.localNewLike.count = this.newLikeVal  
                        console.log("set new vals to local new like",this.localNewLike.count)
                    }
                }else{
                    console.log("going to +++")   
                    this.newLikeVal += this.newLikeVal 
                    if(this.localNewLike.count===null){
                        this.localNewLike.initialAction = '+'
                        this.localNewLike.count = this.newLikeVal 
                    }
                                  
                }                
                
                
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
        async getInitialLikeState(){
            console.log("requesting initial like state")
            this.$store.get(actionType.getLikeState,this.ideaId)
            .then((servResp)=>{
                if(servResp.status===200){
                    this.getInitialLikeState = servResp.data.like
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