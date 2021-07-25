<template>
    <div class="container-fluid">
      <h3 class="mb-4 text-center">This is a main idea place</h3>
        <div class="row py-3">
          <div class="col col-md-2 py-3">
            <section class="categs-space">
              <app-categs></app-categs>
            </section>
          </div>
          <div class="col col-md-8 py-3">
            <app-idea :api-url="apiUrl"></app-idea>
          </div>
          <div class="col col-md-2 py-3">
            <section class="tags-space">             
            <app-tags></app-tags>
            </section>
          </div>
        </div>      
    </div>
</template>
<script>
import AppIdea from '@/components/Idea'
import AppTags from '@/components/Tags'
import AppCategs from '@/components/categs/Categs'

export default {
    name:'AppIdeaGeneral',
    components:{
        AppIdea,
        AppTags,
        AppCategs,        
    },
    computed:{
      sortBy() {
        // console.log("params are",this.$route.params.sort)
        return this.$route.params.sort
    },
      filterBy() {
        // console.log("params are",this.$route.params.featured)
        return this.$route.params.featured
    },
    apiUrl(){           
          // return `/api/v1/ideas-collection/ideas/?ordering=${this.sortBy}`
          return `/api/v1/ideas-collection/ideas/?ordering=${this.sortBy}&featured=${this.filterBy}`
    }
  }    
}
</script>
<style scoped>
.row > div{
  border:1px solid black;
}
</style>