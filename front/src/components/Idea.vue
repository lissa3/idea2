<template>
    <div class="container">        
        <div v-if="isLoading"><app-loader></app-loader></div>
        <div  v-if="ideasToDisplay" class="wrapper">            
            <div class="row main-row" v-for="idea in ideas" :key="idea.id">
                <div   class="col-lg-4 col-md-12 col-sm-12">
                    <div class="idea-img mb-2">
                        <div v-if="idea.thumbnail">                            
                            <img  :src="idea.thumbnail" alt="img idea" class="img-fluid">
                        </div>
                        <div v-else>
                            <img src="@/assets/logo.png" alt="img" class="img-fluid">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm-12 mb-2">
                            <ul class="list-group list-group-horizontal ul-cls">
                                <li class="list-group-item">
                                    <b-icon icon="bookmark-heart-fill"></b-icon>
                                    
                                </li>
                                <!-- <li class="list-group-item tooltip"> -->
                                <li class="list-group-item">
                                    <b-icon icon="person-fill"></b-icon>
                                    <!-- <span class="tooltiptext">See author profile</span> -->
                                </li>
                                <li class="list-group-item">
                                    <b-icon icon="envelope"></b-icon>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-lg-8 col-md-12 col-sm-12">
                <div class="idea-title mb-1 mt-1">
                    <h3>
                       <router-link :to="{ name: 'ideaDetail',params:{slug:idea.slug} }"
                       class="link">{{idea.title}}-id={{idea.id}}</router-link>
                    </h3>
                </div> 
                <div class="idea-title mb-2">
                    <router-link :to="{name:'profile',params:{id:idea.author}}" class="link">
                        <p>By <strong>{{idea.owner_idea}}</strong></p>
                    </router-link>
                </div> 
                <div>Featured: {{idea.featured}}</div>
                <div class="idea-title mb-2 ">
                    <div>
                        <p v-if="idea.avg_rate">
                        <strong>Rating: {{idea.avg_rate}}</strong>
                        </p>
                        <p v-else>
                            <strong>No rating yet</strong>
                        </p>
                    </div>
                </div> 
                <div class="idea-title mb-2">
                    <div>
                       <app-rating-show :rating="idea.avg_rate"></app-rating-show>
                    </div>
                </div> 
                <div class="mb-2">
                    <div class="row">
                        <div class="col-lg-9 col-md-9 col-sm-9">
                           <div class="idea-date mb-2">
                            <span>{{idea.created_at| filterDateTime}}</span>
                            </div>
                        </div>                       
                        <app-like 
                            :idea-id="idea.id"         
                            :idea-likes="idea.an_likes"  
                            :is-anonym="isAnonym"                         
                            > 
                        </app-like>                        
                    </div>
                </div>                
                <div class="idea-main-text mb-2">
                    <p>{{idea.lead_text}}</p>
                </div>
                <div class="idea-read-more mb-2">
                    <router-link :to="{ name: 'ideaDetail',params:{slug:idea.slug} }"
                       class="idea-link">
                        <button class="btn btn-outline-dark">
                        Read More
                        </button>                       
                    </router-link>
                </div>
                <div class="idea-read-more mb-2">
                   <div v-if="idea.tags">                      
                        <div class="d-flex justify-content-left">
                          <div class="px-1">Tags:</div>
                          <app-tags-list :tags="idea.tags"></app-tags-list>                                  
                        </div> 
                      </div>                        
                </div>
              </div>
            </div>
        </div>        
        <div v-if="!ideasToDisplay">{{notFoundMsg}}</div>        
        <div v-if="ideasToDisplay">
            <div >
                <div class="col-lg-8 col-md-12 col-sm-12 pagination">
                    <app-pagination  
                    :currentPage="currentPage" 
                    :total="total"
                    :limit="limit"
                    :url="baseUrl"
                    :next="next"
                    :prev="prev">
                    </app-pagination>           
                </div>
            </div>
        </div>
    </div>    
</template>
<script>

// import {parseUrl} from 'query-string'
import {stringify, parseUrl} from 'query-string'
import {mapState,mapGetters} from 'vuex'
import {actionTypes} from '@/store/modules/ideas'

import {getterTypes as authGetterTypes} from '@/store/modules/auth'



// import {actionTypes as singleIdeaActionType} from '@/store/modules/singleIdea'
import {limit} from '@/helpers/vars'
import  AppPagination from '@/components/Pagination'
import AppLoader from '@/components/Loader'
import AppTagsList from '@/components/TagsList'
import AppLike from '@/components/Like'
import AppRatingShow from '@/components/RatingShow'

export default {
    name:'AppIdea',
    data(){
        return{
            notFoundMsg:"Sorry. Nothing found at this moment",
            ideaLikes:0 
        }
    },
    components:{
         AppPagination,
         AppLoader,
         AppTagsList,
         AppLike,
         AppRatingShow
    },
    props:{
        apiUrl:{
            type:String,
            required:true
        }
    },
    computed:{                  
        ...mapState({
            ideas:state=>state.ideas.data,
            total:state=>state.ideas.count,
            isLoading:state=>state.ideas.isLoading,
            error:state=>state.ideas.error,
            prev:state=>state.ideas.prev,
            next:state=>state.ideas.next          
        }),
        ...mapGetters({
           isLoggedIn:authGetterTypes.isLoggedIn,
           isAnonymous:authGetterTypes.isAnonymous
        }),
        baseUrl() {
        //  console.log("route.path is",this.$route.path)
         return this.$route.path
        },
        currentPage() {
            // console.log("rout query page",this.$route.query.page)
            return Number(this.$route.query.page || '1')
        },
        limit(){
            return limit
        },
        offset() {
         return this.currentPage * limit - limit
        }, 
        ideasToDisplay(){
            return this.total>0                
        },
        isAnonym(){
            return this.isAnonymous
        }        
                  
    },    
    watch: {
        currentPage() {
            // console.log("watcher here; see changes")
            this.fetchIdeas()
        },
         baseUrl(){
            // console.log("watcher base url; see changes")
            this.fetchIdeas()
        }
    },     
    created(){
        this.fetchIdeas()   
        // console.log("islogged?",this.isLoggedIn)    
    },
    methods:{
        fetchIdeas(){
            // console.log("looking for idease...")
            const parsedUrl = parseUrl(this.apiUrl)
            // console.log("step 1 parsed url:",parsedUrl)
            // console.log("parsedUrl",parsedUrl)
            // console.log("parsedUrl.url:   ",parsedUrl.url)
            // console.log("parsedUrl.query:  ",parsedUrl.query)

            const stringifiedParams = stringify({
                limit,
                offset: this.offset,
                ...parsedUrl.query
            })
            const apiUrlWithParams = `${parsedUrl.url}?${stringifiedParams}`
            
            // console.log("calling store func for request")           
            //this.$store.dispatch(actionTypes.getIdeas, {apiUrl: this.apiUrl})       
            this.$store.dispatch(actionTypes.getIdeas, {apiUrl: apiUrlWithParams})
            //.then((resp)=>{
            //    console.log("Ok")
                // console.log("resp.data",resp.data)
           // })
            // .catch(err=>console.log("getIdea error",err))       
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
      }.${initialDate.getFullYear()}-${initialDate.getHours()}:${initialDate.getMinutes()} UTC ${initialDate.getUTCHours()}:${initialDate.getMinutes()}`;
    },
    }    
}
</script>
<style>
.main-row{
    margin:8%;
    background-color: blanchedalmond;
    box-shadow: 0 0 10px 10px rgba(0,0,0,.05);
    border-radius: 0.5rem;
}
.idea-img   >   img{
    width:100%;
    height:100%;
    /* transform: translateY(-30px); */
    object-fit: cover;
    border-radius:0.5rem;
    box-shadow: 0 0 8px 3px rgba(0,0,0,.3);

}
.idea-date span{
    color:#962c51;
}
.ul-cls{
    justify-content: center;
}
.ul-cls li{
    cursor: pointer;
}
.idea-title >h3{
    font-weight: 400;
    font-style: normal;
}
.idea-main-text{
    font-style: normal;
    line-height: 2;
}
/* tooltip */
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;
  
  /* Position the tooltip */
  position: absolute;
  z-index: 1;
  top: -5px;
  left: 105%;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
/* .idea-link{
    text-decoration:none;
    cursor: pointer;
    color:rgb(38, 44, 38)

}
.idea-link:hover{
    text-decoration:none;
    cursor: pointer;
    color:rgb(185, 221, 185)

} */
/* likes */
.click-like{
  cursor: pointer;
  padding:6px;
}
.link{
  color:black;
  text-decoration:none;
}
.link:hover{
  color:rgb(33, 98, 84);
}
</style>