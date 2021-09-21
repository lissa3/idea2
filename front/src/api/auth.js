import axios from '@/api/axios'
import simpleAPI from '@/api/plainAxios'

const register = (creds)=>{
    return axios.post('/auth/users/',creds)
}
const activate = (creds)=>{
    return axios.post('/auth/users/activation/',creds)
}
const login = (creds)=>{
    return axios.post('/auth/jwt/create/',creds)
}

// req by Menu mounted
const getUser = ()=>{
    return axios.get('/auth/users/me/')
}


// req to get a new access token each 15 min
const getNewAccessToken = (refreshToken)=>{
    return axios.post('/auth/jwt/refresh/',refreshToken)
}
// link for new psw instead og forgotten
const confirmEmailPswForget = (creds)=>{
    return axios.post('/auth/users/reset_password/',creds)
}
const requestNewPsw = (creds)=>{
    return axios.post('/auth/users/reset_password_confirm/',creds)
}
// link to change current psw 
const requestChangePsw = (creds)=>{
    return axios.post('/auth/users/set_password/',creds)
}

const getProfile = (id)=>{
    // public access profile
    return simpleAPI.get(`/api/v1/profile-info/${id}/`)
}

const profileOwnerAction = (unid)=>{
    // private access to profile section in Menu
    return axios.get(`/api/v1/profile-owner/${unid}/`)
}

const profileOwnerEdit = (unid,profileData)=>{
    // private access to edit profile 
    return axios.patch(`/api/v1/profile-owner/${unid}/`,profileData)
}

const deleteAccount = (unid)=>{    
    return axios.delete(`api/v1/profile-owner/${unid}/`)
}

// redirect_uri: http://localhost:8000/google
//http://localhost:8000
const registerGoogle = ()=>{
    console.log("api auth prepares url to send ")
    let url = 'http://localhost:8000'
    return simpleAPI.get(`/auth/o/google-oauth2/?redirect_uri=${url}/google`)
}
const googleAuth = async (state,code)=>{
    if(state&&code&& !localStorage.getItem('accessToken')){
        const config = {
            headers:{
                'Content-Type':'application/x-www-form-urlencoded'
            }
        }
        const details = {
            'state':state,
            'code':code
        }
        const formBody = Object.keys(details).map(key=> encodeURIComponent(key)+'='+encodeURIComponent(details[key])).join('&')
        try{
            
            const resp = await axios.post(`/auth/o/google-oauth2/${formBody}`,config);
            console.log("resp is",resp)
            if(resp.data.access){
                console.log("google gives me an access token")
            }
        }catch(err){
            console.log("signing up with google is failed")
        }
    }
}


export default {
    activate,
    confirmEmailPswForget,
    deleteAccount,
    getUser,
    getNewAccessToken,
    getProfile,
    googleAuth,
    login,
    profileOwnerAction,
    profileOwnerEdit,
    requestNewPsw,
    requestChangePsw,
    register,
    registerGoogle,
    

}    