<template>
    <div>
        <section >                  
            <div v-if="tags" class="tag-list">
                <!-- <div v-for="tag in tags" :key="tag.id">
                        <h6 class="px-1 tag" @click="showIdeasForTag(tag)"><b-badge variant="success">{{tag}}</b-badge></h6>
                </div>  -->
                <router-link v-for="tag in tags" :key="tag.id" :to="{name:'ideasByName',params:{name:tag}}" class="tag">
                    <b-badge variant="secondary" class="tag px-2 mx-1">{{tag}}</b-badge>          
                </router-link>                 
                                        
            </div>            
        </section>       
    </div>    
</template>                
                
<script>
export default {
    name:'AppTagsList',
    props:{
        tags:{
        required:true,
        type:Array
      },
    },
    // methods:{
    //     showIdeasForTag(tag){
    //         console.log("user wants ideas for the tag with name",tag)

    //     }
    // }  
   
}
</script>
<style scoped>
.tag-list{
    display: flex;
    flex-direction: row;
    justify-content: right;
    flex-wrap: wrap;
    
}
.tag{
    color:rgb(238, 236, 232)

}
.tag:hover{
    cursor: pointer;
}

</style>