import getCommentAPI from '@/api/comments'

export const actionTypes = {
    sendRootComm:'[comments] Send root comment',
    fetchCommentList:'[comments] Get all comments'
   
}

export const mutationTypes = {
    LOADING_COMMENT_FORM:'[comm] Load comm form',
    SEND_COMMENT_SUCCESS:'[comm] Sent comm form success',
    SEND_COMMENT_FAILURE:'[comm] Sent comm form failure',

    LOADING_COMMENTS_START:'[comm] Load comments start',
    FETCH_COMMENTS_SUCCESS:'[comm] Fetch comments success',
    FETCH_COMMENTS_FAILURE:'[comm] Fetch comments failure',
    
}
const state ={
    isLoading:false,
    data:null,
    error:null

}  

const mutations = {
    [mutationTypes.LOADING_COMMENT_FORM](state){
        state.isLoading = true
        
    },
    [mutationTypes.SEND_COMMENT_SUCCESS](state,payload){
        state.isLoading = false,
        state.data = payload
    },
    [mutationTypes.SEND_COMMENT_FAILURE](state,error){
        state.isLoading = false
        state.error = error
    },
    [mutationTypes.LOADING_COMMENTS_START](state){
        state.isLoading = true        
    },
    [mutationTypes.FETCH_COMMENTS_SUCCESS](state,payload){
        state.isLoading = false,
        state.data = payload
    },
    [mutationTypes.FETCH_COMMENTS_FAILURE](state,error){
        state.isLoading = false
        state.error = error

    }
}
const actions = {
    async [actionTypes.sendRootComm]({commit},commentData){ 
        console.log(actionTypes.sendRootComm)
        commit(mutationTypes.LOADING_COMMENT_FORM);  
        try{
          // commit(mutationTypes.GET_CURRENT_USER_START)   
        //   console.log("trying to fetch cats")
        const resp= await getCommentAPI.sendRootComment(commentData) 
        console.log("resp",resp)
        }catch(err){
            console.log(err)
        }        
    },    
    async [actionTypes.fetchCommentList]({commit},ideaSlug){         
        commit(mutationTypes.LOADING_COMMENTS_START);  
        try{          
            const resp= await getCommentAPI.fetchAllComments(ideaSlug) 
            // console.log("resp results: ",resp.data.results)
            commit(mutationTypes.FETCH_COMMENTS_SUCCESS,resp.data)
            return resp
        }catch(err){
            console.log(err)
            commit(mutationTypes.FETCH_COMMENTS_FAILURE,err)
        }        
    }    
}
    

export default {
    state,
    actions,
    mutations,
    
    
  }

