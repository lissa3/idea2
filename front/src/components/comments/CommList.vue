<template>
    <div>
        <section >                   
            <div v-if="isLoading"><app-loader></app-loader></div>        
            <div  class="comment-list">
                <div class="section-comments">Comments:</div>
                <app-comm-tree :treeData="comments"></app-comm-tree>                       
            </div>
            <div v-if="error">Smth went wrong</div>            
        </section>
        
    </div>    
</template>
<script>

import AppCommTree from '@/components/comments/CommTree'
import AppLoader from '@/components/Loader'
import {actionTypes} from '@/store/modules/comments'
import {mapState} from 'vuex'
export default {
    name:'AppCommentList',
    props:{
        // ideaId:{
        //     type:Number,
        //     required:true
        // },
        ideaSlug:{
            type:String,
            required:true
        },
        // currentUser:{
        //     type:Object,
        //     required:false
        // }
    },
    components:{
        AppCommTree,
        AppLoader,
        
    },
    created(){       
      this.$store.dispatch(actionTypes.fetchCommentList,this.ideaSlug)    
    },    
    computed:{
        ...mapState({
            isLoading: state=> state.comments.isLoading,
            error: state=>state.comments.error,
            comments:state=>state.comments.data

        })
    }
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

</style>