<template>  
    <div class="tree-menu">
      <div :style="indent" @click="toggleChildren(id)" class="label-wrapper">  
        <div class="d-flex justify-content-between"> 
            <div class="d-flex flex-row">       
                <p class="px-1">Written by:</p>
                <p class="px-1"><strong>{{author}}</strong></p>
            </div> 
            <p class="px-1">Date <strong>{{created|filterDateTime}}</strong></p>
        </div>
        <div>
          <strong>Msg:</strong> {{body}}         
        </div>        
      </div> 
      <div v-if="showChildren">     
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
    </div>    
</template>
<script>

export default {
  props: ['body', 'children', 'depth','id','author',
          'created','updated','replyToId','userId','ideaId',''],
  name: "tree-menu",
  computed: {
    indent() {
      // console.log("indent "),this.depth
      return { transform: `translate(${this.depth * 25}px)` };
    },
  },
  data() {
    return {
      showChildren: false,
       
    };
  },
  methods: {    
    async toggleChildren(id) {
      // console.log("show children")
      this.showChildren = !this.showChildren;      
      
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
      }.${initialDate.getFullYear()} at ${initialDate.getHours()} h :${initialDate.getMinutes()} min
      (Universal Time: ${initialDate.getUTCHours()} h ${initialDate.getMinutes()} min)`;
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
</style>>
