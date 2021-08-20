<template>
    <div>
        <div class="mb-5 mx-auto" >
            <!-- <p>submit label</p>{{submitLabel}}-->
            <p>creaning the form: {{cleanForm}}</p>
          <form @submit.prevent="onSubmit" >  
            <div class="form-group">
              <label for="body">Comment</label>
                <textarea id="body" 
                cols="30" rows="5"
                class="border  w-100 h-20 my-2"
                v-model="body"   
                placeholder="Remember, be nice">
                </textarea>
            </div> 
            <div class="d-flex justify-content-around">
            <button class="btn btn-success" type="submit"
            :disabled="isTextareaDisabled">{{submitLabel}}</button>           
            
            <button class="btn btn-primary" @click="handleCancel">Cancel</button>
            </div>   
                    
            
            <!-- <div v-if="hasCancelButton">
                <button>Cancel</button>
            </div> -->
          </form>
           
    </div>
    </div>
</template>
<script>
export default {
    name:'CommentForm',
    props:{
        cleanForm:{
            type:Boolean
        },        
        hasCancelButton:{
            type:Boolean
        },
        initialBody:{
            type:String
        },
        parentId:{
            type:Number||null
        },
        submitLabel:{
            type:String,
            required:true
        },
        success:{
            type:Boolean
        }
        
    },
    data(){
        return{
            body:this.initialBody
        }
    },
    methods:{
        onSubmit(){
            // this.handleSubmit(this.text)
            console.log("form says:start submit ")            
            if(this.submitLabel==='Edit'){
                let commentData = {
                    body:this.body                
                }
                console.log("line 67 - form - sends to comment data",commentData)
                this.$emit('updateComment',commentData)

            }else if(this.submitLabel==='Reply'){
                let commentData = {
                body:this.body,
                parent:this.parentId
                }
                this.$emit('reply',commentData)
            }else{
                let commentData = {
                body:this.body,
                parent:null
                }
                this.$emit('addRootComment',commentData)
                if(this.cleanForm){
                    console.log("form tries to clean body")
                    this.body = ""
                    console.log("body clean")
                }
            }
            
        },
        handleCancel(){
            console.log('edit is canceled')
            this.$emit('handleCancel')
        }
    },
    computed:{
        getBodyText(){
            return this.initialBody
        },
        isTextareaDisabled(){
            return false
            // return this.body.length===0
        },
        cleaning(){
            return this.cleanForm
        }
    },
    watch: {
        cleaning() {
            // console.log("watcher here; see changes")
            this.body=''
        },
    }
}
</script>
<style scoped>
.zoo{
    height: 30px;
    width: 30px;
    background-color: burlywood;

}
.mio{
    opacity: 0.7;
}
</style>