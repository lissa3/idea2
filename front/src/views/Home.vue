<template>
  <div class="home">
    <app-banner></app-banner>  
  </div>
</template>

<script>

import AppBanner from '@/components/Banner'
// import {mapGetters} from 'vuex'
// import {getterTypes} from '@/store/modules/auth'


export default {
  name: 'AppHome',
  components:{
    AppBanner
  },
 
    // computed:{
    //      ...mapGetters({
    //     currentUser:getterTypes.currentUser,
    //     //isLoggedIn:getterTypes.isLoggedIn,
    //     // isAnonymous:getterTypes.isAnonymous,
        
    //     }),
    //     getUnid(){
    //         console.log(this.currentUser.unid)
    //         console.log('url line 48:',`/api/v1/feed-ideas/${this.currentUser.unid}/`)
    //         return this.currentUser.unid
    //     }
    // },
  
  
  
}
</script>
