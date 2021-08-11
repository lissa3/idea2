<template>  
    <div class="tree-menu">
      <div :style="indent"  class="label-wrapper">  
        <div class="row"> 
            <div class=" col-md-12 d-flex  justify-content-left">   
<!--if not deleted  -->
                <div v-if="body" class="col-md-12 ">
                  <div>
                    <div class="row">
                      <div class="col-md-6 d-flex  justify-content-left">
                      <p class="pl-1">Written by:</p> 
                      <template v-if="currentUser&&currentUser.id==user_id">
                        <div class="pl-1 ml-4"><b-icon-pencil></b-icon-pencil></div>
                        <div class="pl-1 ml-4"><b-icon-trash></b-icon-trash></div>
                      </template>               
                      <p class="pl-1 mr-2"><strong>{{author}}</strong></p>
                      </div> 
                      <div class="col-md-6 d-flex justify-content-right">            
                         <p >Date <strong>{{created|filterDateTime}}</strong></p>
                      </div>
                    </div>
                    <div><strong>Msg:</strong> {{body}}</div>
                </div>
                </div>
<!--comment deleted == block else  -->
                <div v-else>
                  <div class="px-2 py-2 comm-deleted mt-2">Note is deleted</div>    
                </div>             
          </div>
        </div>  
      </div> 
      <!-- class="col-md-6 px-1 text-right" -->
      <tree-menu
              v-for="node in children"
              :key="node.id"
              :children="node.children"
              :body="node.body"
              :depth="depth + 1"
              :author="node.author_comment" 
              :created="node.created_at"
              :updated="node.updated_at"
              :reply-to-id="node.reply_to_id"
              :idea-id="node.idea_id"          
              :user-id="node.user_id" 
                            
            >
            </tree-menu>
     
        
        
    </div> 
      
</template>
<script>
import {mapGetters} from 'vuex'
import {getterTypes} from '@/store/modules/auth'
export default {
  props: ['body', 'children', 'depth','id','author',
          'created','updated','replyToId','userId',],
  
  name: "tree-menu",
  computed: {
    indent() {
      // console.log("indent "),this.depth
      return { transform: `translate(${this.depth * 25}px)` };
    },
     ...mapGetters({
          currentUser:getterTypes.currentUser,
          // isLoggedIn:getterTypes.isLoggedIn,
          // isAnonym:getterTypes.isAnonymous
        }),

    
  },
  data() {
    return { // showChildren: false,
     };
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
      (UTC: ${initialDate.getUTCHours()} h ${initialDate.getMinutes()} min)`;
    },
    }    
};
</script>

<style scoped>
.tree-menu .label-wrapper {
  padding-bottom: 10px;
  margin-bottom: 10px;
  border-bottom: 1px solid #ccc;
  cursor: pointer;
}
.left-shift {
  text-align: left;
  padding: 0.2rem 0 0.5rem 0.5rem;
  margin-left: 1rem;
  /* margin-left: 0.5rem; */
  cursor: pointer;
}
.comment-body{
  border:1px solid black;
  border-radius: 3px; 

}
.tree-menu .label-wrapper {
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
</style>>
