import fetchTags from '@/api/tags'

export const actionTypes = {
    getTags:'[tags] Get tags',
    // ideasByTagName:'[tags] Get by tag name'
}

export const mutationTypes = {
    LOADING_TAGS:'[tags] Load tags',
    GET_TAGS_SUCCESS:'[tags] Set list tags',
    GET_TAGS_FAILURE:'[tags] Fail list tags',
    
}
const state ={
    isLoading:false,
    data:null,
    error:null
}
const mutations = {
    [mutationTypes.LOADING_TAGS](state){
        state.isLoading = true
        state.data = null
    },
    [mutationTypes.GET_TAGS_SUCCESS](state,payload){
        state.isLoading = false,
        state.data = payload
    },
    [mutationTypes.GET_TAGS_FAILURE](state,error){
        state.isLoading = false
        state.error = error

    }
}
const actions = {
    async [actionTypes.getTags]({commit}){    
        // data from djoser:userId,
        // console.log("inside getTags") 
        commit(mutationTypes.LOADING_TAGS);  
        try{
          // commit(mutationTypes.GET_CURRENT_USER_START)   
          const resp= await fetchTags.getTags()
        //   console.log("got tags",resp.data)
          if(resp.status === 200){ 
            // console.log("got tags is OK")                        
            commit(mutationTypes.GET_TAGS_SUCCESS,resp.data) 
            // commit(mutationTypes.GET_TAGS_FAILURE,err=null)           
            return resp.data      
            }
          }
          catch(err){
              // console.log("can't fetch tags",err)
            commit(mutationTypes.GET_TAGS_FAILURE,err)
            
          }
        },
}




export default {
    state,
    actions,
    mutations,
    
    
  }
