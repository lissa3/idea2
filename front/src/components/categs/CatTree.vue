<template>
  <div>
    <div>
      <div v-for="node in treeData" :key="node.id">
        <div v-if="node.children && node.children.length" class="left-shift">
          <!-- <div v-if="tree.children.length > 0" class="left-shift"> -->
           
          <app-node-tree
            :name="node.name"
            :children="node.children"
            :depth="0"
            :slug="node.slug"            
          ></app-node-tree>
          <!-- :depth otherwise a string will be passed to a child component -->
        </div>
        <div class="left-shift" v-else>
          <!-- <div @click="getCatIdeas(node.slug)">{{ node.name }}</div> -->
           <router-link :to="{name:'categ',params:{slug:node.slug}}" class="categ">
                <b-badge variant="secondary" class="categ px-2 mx-1">{{node.name}}</b-badge>          
            </router-link> 
        </div>
        <!-- <router-link v-for="categ in categs" :key="categ.id" :to="{name:'categ',params:{slug:categ.slug}}" class="categ">
                <b-badge variant="secondary" class="categ px-2 mx-1">{{categ.name}}</b-badge>          
            </router-link>  -->
      </div>
    </div>
  </div>
</template>
<script>
import AppNodeTree from "@/components/categs/NodeTree.vue";

export default {
  components: { AppNodeTree },
  props: ["treeData"], 
  data(){
    return {
      
    }
  }, 
  methods: {    
     
    // async getCatIdeas(catSlug) {
    //   // gives a list of ideas for a specific category
    //   try{
    //    console.log("getting categ idea",catSlug)
    //   }
    //   catch(err){
    //     console.log("store: error in category ideas");
    //   }
    // },
    
  },
  created(){
    // console.log("Cat Tree component is created")
  }
};
</script>

<style scoped>
.left-shift {
  text-align: left;
  padding: 0.2rem 0 0.5rem 0.5rem;
  margin-left: 0.5rem;
  cursor: pointer;
}
/* .zoo{
  transform: translate(25px);
  eq: translate(25px, 0) = only in horizontal direction
} */
</style>>