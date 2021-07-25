<template>
  <div class="about">
    <p>Temp msg:This is an error msg block</p>
    <p v-if="errorSingleIdea">Sorry, PAGE NOT FOUND</p>
  </div>
</template>

<script>
import {mapState} from 'vuex'
export default {
  name:'AppErrorMsg',
  props:{
        message:{
            type:String,
            required:false
        }
    },
  computed:{            
        ...mapState({            
            errorSingleIdea:state=>state.idea.error
        })
  },
}
</script>
