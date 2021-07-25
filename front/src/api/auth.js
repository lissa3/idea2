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

// getAPI = with Authorization JWT header
const getUser = ()=>{
    return axios.get('/auth/users/me/')
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

const registerGoogle = ()=>{
    console.log("api auth prepares url to send ")
    let url = 'http://localhost:8080'
    return axios.get(`/auth/o/google-oauth2/?redirect_uri=${url}/google`)
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
const getProfile = (id)=>{
    // access not private
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


export default {
    register,
    activate,
    login,
    getUser,
    registerGoogle,
    googleAuth,
    confirmEmailPswForget,
    requestNewPsw,
    requestChangePsw,
    getProfile,
    profileOwnerAction,
    profileOwnerEdit
    

}    