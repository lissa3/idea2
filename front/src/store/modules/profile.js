import profileAPI from '@/api/auth'

const state = {
    data:null,
    // profileOwner:null,
    isLoading:false,
    error:null,
    err500:null,
    netWorkErr:null  
     
}


export const mutationTypes = {
    START_PROFILE_LOADING:'[profile private] Load profile start',
    GET_PROFILE_SUCCESS:'[profile private] Get profile success',
    GET_PROFILE_FAILURE:'[profile private] Get profile failure',
    
    CHANGE_PROFILE_LOADING:'[profile private] Edit profile start',
    CHANGE_PROFILE_SUCCESS:'[profile private] Edit profile success',
    CHANGE_PROFILE_FAILURE:'[profile private] Edit profile failure',
    NETWORK_PROBELM:'[profile private] Edit NETWORK_PROBELM', 
    STATUS_500:'[profileprivate] Edit STATUS 500 SERVER ERROR',  

}
export const actionTypes = {
    retrieveProfile:'[profile] Get profile',
    showPersonalInfo:'[profile] Owner profile',   
    editPersonalInfo:'[profile] Edit personal profile'   
    
}
const mutations = {
    [mutationTypes.START_PROFILE_LOADING](state){
        state.isLoading = true
        // let op: all prev data will be out|=> met een schone lei beginnen
        // state.data = null
      },
    [mutationTypes.GET_PROFILE_SUCCESS](state,payload){
        state.isLoading = false
        state.data = payload
        localStorage.setItem("profile",JSON.stringify(payload))
    }, 
    [mutationTypes.GET_PROFILE_FAILURE](state,error){
        // at this point I don't know what errors I'll get
        state.isLoading = false
        state.error=error
        state.data = null
    },
    [mutationTypes.CHANGE_PROFILE_LOADING](state){
        state.isLoading = true
        // let op: all prev data will be out|=> met een schone lei beginnen
        // if state.data = null |=> no data  in case of errors
      },
    [mutationTypes.CHANGE_PROFILE_SUCCESS](state,payload){
        state.isLoading = false
        state.data = payload
    }, 
    [mutationTypes.CHANGE_PROFILE_FAILURE](state,error){
        // at this point I don't know what errors I'll get
        state.isLoading = false
        state.error=error
    },
    [mutationTypes.NETWORK_PROBELM](state){
        state.netWorkErr = true    
        state.isLoding=false
    },
    [mutationTypes.STATUS_500](state){
        state.err500 = true    
        state.isLoading=false
    }, 
}
const actions = {
    async [actionTypes.retrieveProfile]({commit},id){
        console.log("store dispatching get profile,id",id)       
        commit(mutationTypes.START_PROFILE_LOADING);
        try{
        //    console.log(profileAPI.getProfile ) 
           const resp = await profileAPI.getProfile(id)            
            console.log("response getProfile is",resp)
            commit(mutationTypes.GET_PROFILE_SUCCESS,resp.data)                        
            return resp            

        } catch(err){
            commit(mutationTypes.GET_PROFILE_FAILURE,err)
            return err
        }          
    },
    async [actionTypes.showPersonalInfo]({commit},unid){
        console.log("store dispatching get profile,id",unid)       
        commit(mutationTypes.START_PROFILE_LOADING);
        try{
        //    console.log(profileAPI.getProfile ) 
           const resp = await profileAPI.profileOwnerAction(unid)            
            console.log("response getProfile is",resp)
            commit(mutationTypes.GET_PROFILE_SUCCESS,resp.data)                        
            return resp            

        } catch(err){
            commit(mutationTypes.GET_PROFILE_FAILURE,err)
            return err
        }          
    },
    async [actionTypes.editPersonalInfo]({commit},{unid,profileData}){
        // console.log("store dispatching get profile,id",unid)       
        commit(mutationTypes.CHANGE_PROFILE_LOADING);
        const servResp = {}
        try{
        //    console.log(profileAPI.getProfile ) 
           const resp = await profileAPI.profileOwnerEdit(unid,profileData)            
            console.log("response edit profile",resp)
            commit(mutationTypes.CHANGE_PROFILE_SUCCESS,resp.data)   
            servResp.status = resp.status
            servResp.data = resp.data                     
            return resp            

        } catch(err){
            console.dir(err)
            // commit(mutationTypes.CHANGE_PROFILE_FAILURE,err)   
            if(err.response===undefined){
                // commit(mutationTypes.NETWORK_PROBELM)
                servResp.servDown = true 
                return servResp                 
            }else if(err.response.status === 500){
                // commit(mutationTypes. STATUS_500)
                // DONE  
                servResp.status = err.response.status
                console.log("500 error gets sent to vue page",servResp)
                return servResp
            } else{        
                console.log("line 119 calling",err.response.status)
                servResp.status = err.response.status
                servResp.imgErr = err.response.data.image
                servResp.bioErr = err.response.data.bio
                servResp.websiteErr = err.response.data.website
                // commit(mutationTypes.CHANGE_PROFILE_FAILURE,err)  
                return servResp
            }
          

            
            
        }          
    },
    

}

export default {
    state,    
    mutations,
    actions,
    // getters
    
  }
