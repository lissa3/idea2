<template>
  <!-- section render all comments users_comments-->
<div class="row" v-if="treeData">
  <div class="col-md-11 py-3" v-for="node in treeData" :key="node.id">
    <div v-if="node.children&&node.children.length" class="left-shift">
     
      <div >        
          <app-node-tree      
          :body="node.body"
          :children="node.children"
          :depth="0" 
          :author="node.author_comment" 
          :created="node.created_at"
          :updated="node.updated_at"
          :reply-to-id="node.reply_to_id"
          :idea-id="node.idea_id"      
          :user-id="node.user_id"          
        ></app-node-tree>
        
      </div> 
    </div>
    <div v-else class="left-shift">
     <div class="label-wrapper">
        <div class="row">
          <div v-if="node.body" class="col-md-12"> 
            <div class="row">              
              <div class=" col-md-6 d-flex  justify-content-left">       
                  <p class="pl-1">Written by:</p>                
                  <p class="pl-1 mr-2"><strong>{{node.author_comment}}</strong></p>
                  <template v-if="currentUser&&currentUser.id==node.user_id">
                    <div class="pl-1 ml-4"><b-icon-pencil></b-icon-pencil></div>
                    <div class="pl-1 ml-4"><b-icon-trash></b-icon-trash></div>
                  </template>
              </div> 
              <div class="col-md-6 px-1 text-right">Date <strong>{{node.created_at|filterDateTime}}</strong>
              </div>
            </div>

            <p class="px-1"><strong>Msg:</strong> {{node.body}}</p>         
        </div>       
        <div v-else>
          <div class="px-2 py-2 comm-deleted">Note is deleted</div>         
        </div>
        </div>      
    </div> 
    </div>    
   
      
  </div>
</div>
</template>
<script>
import AppNodeTree from "@/components/comments/NodeTree.vue";
import {mapGetters} from 'vuex'
import {getterTypes} from '@/store/modules/auth'
export default {
  components: { AppNodeTree },
  props: {
      treeData:{
        type:Array,
        required:false
        },
      // currentUser:{
      //   type:Object||null,
      //   required:false
      //   },
      // ideaId:{
      //   type:Number,
      //   required :true
      // }  

        }, 
  computed:{
     ...mapGetters({
          currentUser:getterTypes.currentUser,
          // isLoggedIn:getterTypes.isLoggedIn,
          // isAnonym:getterTypes.isAnonymous
        }),
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
};
</script>
<style scoped>
.label-wrapper {
  padding-bottom: 10px;
  margin-bottom: 10px;
  border-bottom: 1px solid #ccc;
  cursor: pointer;
}
</style>
