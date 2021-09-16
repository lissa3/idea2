import authAPI from '@/api/auth'

export const mutationTypes = {
  CLEAR_CREDS:'[auth] CLEAR_CREDS',
  PASS_EMAIL_POTENTIAL_USER:'[auth] PASS_EMAIL_POTENTIAL_USER',
  REGISTER_SUCCESS:'[auth] REGISTER_SUCCESS',
  REGISTER_FAILURE:'[auth] REGISTER_FAILURE',

  SET_ACCESS_TOKEN:'[auth] SET_ACCESS_TOKEN',
  SET_CONFIRM:'[auth] SET_CONFIRM',
  SET_REFRESH_TOKEN:'[auth] SET_REFRESH_TOKEN',
  // get a new access token with refresh
  SET_NEW_ACCESS_TOKEN_SUCCESS:'[auth] SUCCESS GET NEW ACCESS TOKEN',
  FETCH_NEW_ACCESS_FAILURE:'[auth] FETCH NEW ACCESS TOKEN FAILURE',
  //login
  SET_LOG_IN:'[auth] SET_LOG_IN',
  SET_LOGIN_SUCCESS:'[auth] SET_LOGIN_SUCCESS',
  SET_LOGIN_FAILURE:'[auth] SET_LOGIN_FAILURE',
  SET_USER:'[auth] SET_USER',
  // current user
  SET_CURRENT_USER:'[auth] GET_CURRENT_USER_START',
  GET_CURRENT_USER_SUCCESS:'[auth] GET_CURRENT_USER_SUCCESS',
  GET_CURRENT_USER_FAILURE:'[auth] GET_CURRENT_USER_FAILURE',
  // reset forgotten password
  SET_EMAIL_CONFIRM_PSW_RESET_FAILURE:'[auth] SET_EMAIL_CONFIRM_PSW_RESET_FAILURE',
  EMAIL_EXIST_PSW_RESET:'[auth] EMAIL_EXIST_PSW_RESET',
  START_CONFIRM_PSW_RESET:'[auth] START_CONFIRM_PSW_RESET',
  RESET_NEW_PSW_SUCCESS:'[auth] RESET_NEW_PSW_SUCCESS',
  RESET_NEW_PSW_FAILURE:'[auth] RESET_NEW_PSW_FAILURE',
  // network-problem
  NETWORK_PROBELM:'[auth] NETWORK_PROBELM',
  STATUS_500:'[auth] STATUS 500 SERVER ERROR',
  INCORRECT_PSW:'[auth] INCORRECT_PSW',
  RESET_NETWORK_PROBELM:'[auth] RESET NETWORK_PROBELM',
  RESET_STATUS_500:'[auth] RESET STATUS 500 SERVER ERROR',
  // delete account
  START_DELETE_ACCOUNT:'[auth] DELETE account',
  DELETE_ACCOUNT_SUCCESS:'[auth] DELETE account success',
  DELETE_ACCOUNT_FAILURE:'[auth] SET_LOGIN_FAILURE',
  

}
export const actionTypes = {
  register:'[auth] register',
  activate:'[auth] activate',
  login:'[auth] login',
  getUser:'[auth] getUser',
  signOut:'[auth] signOut',
  confirmEmailForgottenPsw:'[auth] confirmEmailForgottenPsw',
  setNewPswAfterForget:'[auth] setNewPswAfterForget',
  setNewPswAChange:'[auth] setNewPswAChange',
  deleteAccount:'[auth] delete user account',
  fetchFreshAccessToken:'[auth] fetch new access with refresh token'

}
export const getterTypes = {
  currentUser:'[auth] currentUser',
  isLoggedIn:'[auth] isLoggedIn',
  isAnonymous:'[auth] isAnonymous'
}
const state ={
  // waiting for ....
  isLoading:false,
  // sign up
  accessToken:null,
  refreshToken:null,
  confirmation:false,
  signUpSuccess:false,
  signUpFailure:false,
  // auth via google
  googleAuthSuccess:null,
  googleAuthFail:null,
  // result of login  
  loginFailure:false,
  loginSuccess:false,
  isLogIn:null, // null,false,true,   
  showEmail:null,
  // confirmation sent to email after signUp
  user:null,
  userId:null,
  // reset psw instead of forgotten
  confirmResetPsw:false,
  emailPswResetFailure:false,
  resetPswSuccess:false,
  pswResetFailure:false,
  incorrectEmail:false,
  errEvent:null,

  netWorkErr:false,
  status500:false,
  noRespServer:false

}
const getters = {
  [getterTypes.currentUser]:state=>{
    return state.user||JSON.parse(localStorage.getItem('user'))
  },
  [getterTypes.isLoggedIn]:state=>{
    // scheiden false|null
    // console.log("getter isLoggedIn",Boolean(state.isLogIn))
    return Boolean(state.isLogIn)
  },
  [getterTypes.isAnonymous]:state=>{
    // scheiden false|null
    // console.log("getter isAnonym",state.isLogIn===null)
    return state.isLogIn === null
  }
}
const mutations = {
  [mutationTypes.CLEAR_CREDS](state){
    state.isLogIn=false
    state.accessToken=null
    state.refreshToken=null
    state.user =null
    state.isLogIn = false
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    localStorage.removeItem('userId');
    localStorage.removeItem('profile');
    
  },
  [mutationTypes.PASS_EMAIL_POTENTIAL_USER](state,email) {
    console.log("inside mutation PASS EMAIL POT USER with email",email)
    state.showEmail=email;
  },
  [ mutationTypes.REGISTER_SUCCESS](state){
    state.signUpFailure = true;
    state.isLoading = false
  },
  [ mutationTypes.REGISTER_FAILURE](state){
    state.signUpFailure = true;
    state.isLoading = false
  },
  [mutationTypes.SET_ACCESS_TOKEN](state,access){
    localStorage.setItem("accessToken",access)
    state.accessToken = access
  },
  [mutationTypes.SET_CONFIRM](state){
    state.confirmation = true
  },
  [mutationTypes.SET_LOG_IN](state){
    state.isLogIn = true
  },
  [mutationTypes.SET_LOGIN_SUCCESS](state){
    state.loginSuccess = true
  },
  [mutationTypes.SET_LOGIN_FAILURE](state){
    state.loginFailure = true
  }, 
  [mutationTypes.SET_REFRESH_TOKEN](state,refresh){
    localStorage.setItem("refreshToken",refresh)
    state.refreshToken = refresh
  },
  [mutationTypes.GET_CURRENT_USER_START](state){
    state.isLoading = true
  },
  [mutationTypes.SET_CURRENT_USER](state,payload){
    state.isLoading = false    
    state.user = payload
    state.userId = payload.id    
    localStorage.setItem("user",JSON.stringify(payload))
  },
  [mutationTypes.GET_CURRENT_USER_FAILURE](state){
    state.isLoading = false,
    state.isLogIn = null,
    state.currentUser = null
  },  
  [mutationTypes.START_CONFIRM_PSW_RESET](state){
    state.isLoading = true    
  },
  [mutationTypes.EMAIL_EXIST_PSW_RESET](state,email){
    state.isLoading = false
    state.showEmail = email
  },
  [mutationTypes.SET_EMAIL_CONFIRM_PSW_RESET_FAILURE](state,email){
    state.emailPswResetFailure = true
    state.showEmail = email,
    state.isLoading=false
  },
  [mutationTypes.NETWORK_PROBELM](state){
    state.netWorkErr = true    
    state.isLoading=false
  },
  [mutationTypes.STATUS_500](state){
    state.status500 = true    
    state.isLoading=false
  },
  [mutationTypes.RESET_NETWORK_PROBELM](state){
    state.netWorkErr = false      
  },
  [mutationTypes.RESET_STATUS_500](state){
    state.status500 = false  
    
  },
  [mutationTypes.INCORRECT_PSW](state){
    state.incorrectEmail = true    
    state.isLoading=false
  },
  [mutationTypes.RESET_NEW_PSW_SUCCESS](state){
    state.isLoading = false
    state.resetPswSuccess = true    
  },
  [mutationTypes.RESET_NEW_PSW_FAILURE](state){
    state.pswResetFailure = true    
    state.isLoading=false    
  },  
  [ mutationTypes.START_DELETE_ACCOUNT ](state){
    state.isLoading = true
  },
  [ mutationTypes.DELETE_ACCOUNT_SUCCESS ](state){
    state.isLoading = false   
    
  },
  [ mutationTypes.DELETE_ACCOUNT_FAILURE ](state,err){
    state.isLoading = false
    state.errEvent = err
  },
  [mutationTypes.SET_NEW_ACCESS_TOKEN_SUCCESS](){},
  [mutationTypes.FETCH_NEW_ACCESS_FAILURE](){
    state.noRespServer = true
  }
  
}
const actions = {
    async [actionTypes.register]({commit},creds){
      commit(mutationTypes.RESET_NETWORK_PROBELM)     
      commit(mutationTypes.RESET_STATUS_500)   
      const servResp = {}       
        try{
          const resp = await authAPI.register(creds)        
            //console.log("response is",resp) //.config,.data (f_name,l_name,email),status=201
            servResp.status = resp.status;
            console.log('in store action register status is:',resp.status)
            servResp.email = resp.data.email; 
            servResp.status = 201    
            commit(mutationTypes.PASS_EMAIL_POTENTIAL_USER,resp.data.email); 
            console.log("sending to vue",servResp)            
            return servResp
        }catch(err) {
          // let op: don't set here check console.log(err.status because it can be undefined)
          // console.log("auth sign up err:",err)
          // console.log("auth sign up  err keys:",Object.keys(err))
          // console.dir(err)
          console.log(err)
          commit(mutationTypes.REGISTER_FAILURE)
          if(err.response === undefined){
            // DONE
            commit(mutationTypes.NETWORK_PROBELM)
            servResp.servDown = true  
            return servResp         
          }else if(err.response.status ===400){
            // DONE частично
            console.dir(err)            
            servResp.status = err.response.status
            servResp.emailErr = err.response.data.email            
            servResp.usernameErr = err.response.data.username
            servResp.pswErr = err.response.data.password
            servResp.psw2Err = err.response.data.re_password
            servResp.nonFieldErr = err.response.data.non_field_errors
            // console.log("sent to vue",servResp)
            // console.log("sent to vue keys",Object.keys(servResp))
            return servResp
                        
          }else if(err.response.status ===500){
            commit(mutationTypes.STATUS_500)
            // DONE  
            servResp.status = err.response.status
            console.log("sending to vue page",servResp)
            return servResp
          }else if(err.response.status === 404){
            console.log("page not found")
            servResp.status=404
            return servResp
          }else{
            console.log("Server can't be reach; check your internet connection, please")
            servResp.status = 404
            console.log("sending to vue page",servResp)
            return servResp
          }
        }  
                  
        
  },      
  
  [actionTypes.activate]({commit},creds){
    // endpoint will return only: response status=204, no data
    return new Promise((resolve,reject)=>{
      let status = ""
      authAPI.activate(creds)
      .then((resp)=>{
        // dj server response == 204        
        commit(mutationTypes.SET_CONFIRM);
        //console.log("msg from store: email confirmed")
        status = resp.status
        resolve(status)
      })
      .catch((err)=>{
        //console.log("err during email confirmation");
        status = err.response.status;
        commit('REGISTER_FAILURE')
        reject(status)
      })

    })
  },
  async [actionTypes.login]({commit},creds){
    const servResp = {}
    try{
      const resp = await authAPI.login(creds) 
        commit(mutationTypes.RESET_NETWORK_PROBELM)     
        commit(mutationTypes.RESET_STATUS_500)   
        //console.log("got from server",resp) 
        if(resp.status ===200){   
          console.log("making mutaions in store")     
          commit(mutationTypes.SET_LOGIN_SUCCESS)  
          commit(mutationTypes.SET_ACCESS_TOKEN,resp.data.access)
          commit(mutationTypes.SET_REFRESH_TOKEN,resp.data.refresh)
        }
        console.log("passing resp to component",resp)
        console.log("calling for getUser for info")
        // call for user data (user = {id,first_name,last_name,email})
        servResp.status = resp.status
        servResp.data = resp.data   
        return resp
    }  catch(err){
        console.log("store passes this error to component:",err)           
        commit(mutationTypes.SET_LOGIN_FAILURE)
        if(err.response === undefined){
          // DONE
          console.log("chec mutaion nwp?")
          commit(mutationTypes.NETWORK_PROBELM)
          servResp.servDown = true  
          return servResp         
        }else if(err.response.status ===500){
          commit(mutationTypes.STATUS_500)
          // DONE  
           return resp
        }else{
          localStorage.clear()
          //console.log("login failed and Local storage is cleaned")        
          return err
        }        
        
      }
    
  },  
  async [actionTypes.getUser]({commit}){    
    // data from djoser:userId,
    //console.log("inside getUser")   
    try{
      // commit(mutationTypes.GET_CURRENT_USER_START)   
      const resp= await authAPI.getUser()     
       
          let user = resp.data             
          commit(mutationTypes.SET_CURRENT_USER,user)
          commit(mutationTypes.SET_LOG_IN) 
          commit(mutationTypes.SET_LOGIN_SUCCESS) 
          console.log("passing resp to Menu",resp.status)
          if(resp.status){
            return resp.status     

          }
          else{
            console.log("resp is undefined")
            return resp
          }
        
      }    
      
      catch(err){
        console.log("store line 364, err",err)
        console.log("passing result of access toekn failure to Menu: err:",err)
        commit(mutationTypes.GET_CURRENT_USER_FAILURE)
        // localStorage.clear()
        return err.response.status
      }
    },    
  async [actionTypes.signOut]({commit}){
      //console.log("store starts sign out")
      commit(mutationTypes.CLEAR_CREDS)
      console.log("local storage is clear")
  },
  async [actionTypes.confirmEmailForgottenPsw]({commit},creds){   
    // Sally2020#
    console.log("inside 372 store")
    commit(mutationTypes.START_CONFIRM_PSW_RESET) 
    const servResp = {}    
    try{
      let email = {"email":creds.email}
      console.log("to server email",creds)         
      const resp = await authAPI.confirmEmailPswForget(email)
      console.log("resp in auth.js",resp) 
      commit(mutationTypes.EMAIL_EXIST_PSW_RESET,email)
      /* if email exists in db=> resp.status=204,data="" statusText="No content" */     
      return resp 

    }catch(err){
      console.log("where are my mutations?",err)
      console.dir(err)
      // commit(mutationTypes.PASS_EMAIL_POTENTIAL_USER,null)
      commit(mutationTypes.SET_EMAIL_CONFIRM_PSW_RESET_FAILURE,creds.email)
      if(err.response === undefined){
        commit(mutationTypes.NETWORK_ERROR)
        // console.log("err resp",err.response)
        servResp.servDown = true
      }
      else{
        commit(mutationTypes.INCORRECT_PSW)
        servResp.status = err.response.status        
        servResp.currentPsw = err.response.data.email,
        servResp.nonFieldErr = err.response.data.non_field_errors
      }
      localStorage.clear()
      return servResp
    }

  },
  async [actionTypes.setNewPswAfterForget]({commit},creds){
    // Sally2020#
    commit(mutationTypes.START_CONFIRM_PSW_RESET) 
    const payload = {
      "new_password":creds.psw,
      "re_new_password":creds.psw2,
      "uid":creds.uid,
      "token":creds.token,
    };    
    try{
      const resp = await authAPI.requestNewPsw(payload)
          
      commit(mutationTypes.RESET_NEW_PSW_SUCCESS)
      console.log("resp success after forget",resp) 
      return resp
       
    }catch(err){
      commit(mutationTypes.RESET_NEW_PSW_FAILURE)
      console.log("my arrorz:",err)
      
    }
  },
  //requestChangePsw
  async [actionTypes.setNewPswAChange]({commit},creds){
    // Sally2020#
    // console.log("line 300 with creds",creds)
    commit(mutationTypes.START_CONFIRM_PSW_RESET)
    const servResp = {}      
    const payload = {
        "new_password":creds.newPsw,
        "re_new_password":creds.newPsw2,
        "current_password":creds.currentPsw           
    }   
    try{      
      // console.log("payload is",payload) 
      const resp = await authAPI.requestChangePsw(payload)               
      commit(mutationTypes.RESET_NEW_PSW_SUCCESS)      
      // console.log("status is",resp.status) 
      servResp.status = resp.status
      // console.log("resp park:",servResp)
      return servResp
       
    }catch(err){
      commit(mutationTypes.RESET_NEW_PSW_FAILURE)
      // console.log("store auth.js err",Object.keys(err))
      console.dir(err)
      if(err.response === undefined){
        console.log("err resp",err.response)
        servResp.servDown = true

      }else{
        servResp.status = err.response.status
        servResp.newPsw =err.response.data.new_password,
        servResp.newPsw2 = err.response.data.re_new_password,
        servResp.currentPsw = err.response.data.current_password,
        servResp.nonFieldErr = err.response.data.non_field_errors
      }
      console.log("from store err obj",servResp)
      return servResp
      
    }
  },
  async [actionTypes.deleteAccount]({commit},{psw}){
    console.log("store starts to delete account")
    const servResp = {}  
    try{      
      console.log("try to del block")         
      const resp = await authAPI.deleteAccount({"current_password":psw})      
      commit(mutationTypes.DELETE_ACCOUNT_SUCCESS)
      servResp.status = resp.status
      return servResp 
      
      // console.log("resp in auth.js",resp) 
      /* if email exists in db=> resp.status=204,data="" statusText="No content" */     

    }catch(err){
      commit(mutationTypes.DELETE_ACCOUNT_FAILURE,err)      
      if(err.response === undefined){
        // DONE
        commit(mutationTypes.NETWORK_PROBELM)
        servResp.servDown = true  
        return servResp         
      }else if(err.response.status ===400){
        // DONE частично
        // console.dir(err)            
        servResp.status = err.response.status             
        servResp.pwsErr = err.response.data.current_password
        
        // console.log("sent to vue",servResp)
        // console.log("sent to vue keys",Object.keys(servResp))
        return servResp
                    
      }else if(err.response.status ===401){
        // DONE частично
        // console.dir(err)            
        servResp.status = err.response.status             
        // console.log("sent to vue",servResp)
        // console.log("sent to vue keys",Object.keys(servResp))
        return servResp
                    
      }else if(err.response.status ===500){
        commit(mutationTypes. STATUS_500)
        // DONE  
        servResp.status = err.response.status
        console.log("sending to vue page",servResp)
        return servResp
      }else if(err.response.status === 404){
        console.log("page not found")
        servResp.status=err.response.status
        return servResp
      }
    
    }
    
},
  async [actionTypes.fetchFreshAccessToken]({commit},refresh){
    try{
      
      console.log('store func line 531 asking for a new access token with refresh')
      // console.log(authAPI.getNewAccessToken)
      const resp= await authAPI.getNewAccessToken({refresh:refresh})
      if(resp.status === 200){          
        let newAccess = resp.data.access  
        console.log("line 525 data",newAccess)           
        commit(mutationTypes.SET_ACCESS_TOKEN,newAccess)        
        commit(mutationTypes.SET_NEW_ACCESS_TOKEN_SUCCESS) 
        return resp      
        }  
      

    }catch(err){
      commit(mutationTypes.FETCH_NEW_ACCESS_FAILURE) 
      console.log('error during fetching new access token')
    }

  }
  
} 

export default {
  state,
  getters,  
  mutations,
  actions
  
}