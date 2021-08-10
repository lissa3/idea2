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

    NETWORK_PROBELM:'[Comment] NETWORK_PROBELM',
    STATUS_500:'[Comment] STATUS 500 SERVER ERROR',
    
}
const state ={
    isLoading:false,
    data:null,
    error:null,
    servErrs:{
        status:null,       
        netWorkErr:null,
        status500:null
      },

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
    },
    [mutationTypes.NETWORK_PROBELM](state){
        state.netWorkErr = true  
        state.servErrs.netWorkErr=true 
    },
    [mutationTypes.STATUS_500](state){
        state.err500 = true  
        state.servErrs.status500=true  
    },    
}
const actions = {
    async [actionTypes.sendRootComm]({commit},commentData){ 
        const serResp = {}
        commit(mutationTypes.LOADING_COMMENT_FORM);  
        try{          
        const resp= await getCommentAPI.sendRootComment(commentData) 
        commit(mutationTypes.SEND_COMMENT_SUCCESS)
        serResp.status = 201
        return serResp
        
        }catch(err){
            commit(mutationTypes.SEND_COMMENT_FAILURE,err)
            if(err.response ===undefined){
                commit(mutationTypes.NETWORK_PROBELM)
                servResp.servDown = true  
                return servResp  
            }else if(err.response.status===500){
                commit(mutationTypes.STATUS_500)
                serResp.status =err.response.status
                return serResp
            }else{
                serResp.status=err.response.status
                servResp.body=err.response.body
                return servResp
            }
            
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

