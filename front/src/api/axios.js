import axios from 'axios'
let baseUrl = 'http://127.0.0.1:8000'


axios.defaults.baseURL=baseUrl

axios.interceptors.request.use(config=>{
    const token = localStorage.getItem('accessToken')
    const authorizationToken = token? `JWT ${token}`: null

    // console.log(authorizationToken)

    // console.log(authorizationToken)

    config.headers.Authorization = authorizationToken
    return config
})

// axios.interceptors.response.use((resp)=>{
//         return resp
//     },
//     function(error){
//         const originalRequest = error.config
//         originalRequest._retry = false
//         if(error.response.status ===401 &&originalRequest.url ==="/auth/jwt/refresh/"){
//             // console.log("refresh is not fresh any more");
//             window.location.href = '/login';
//         }
//         if(error.response.status ===401&&!originalRequest._retry){
//             originalRequest._retry = true
//             return axios.post('/auth/jwt/refresh/',{'refresh':localStorage.getItem('refreshToken')})
//             .then(res=>{
//                 if(resp.status ===200){
//                     // put access token to LS
//                     localStorage.setItem('accessToken',resp.data.access)
//                     // change auth header
//                     axios.defaults.headers.common['Authorization'] = `JWT ${resp.data.access}}` 
//                     // return origina req with axios
//                     return axios(originalRequest)
//                 }
//             })
//         }else{
//             window.location.href = '/login/';
//         }
//     }
// )



export default axios

