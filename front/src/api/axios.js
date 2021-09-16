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
//     async function(error){
//         console.log("starting interceptors line 29")
//         const originalRequest = error.config
//         originalRequest._retry = false
//         if(typeof error.reponse ==='undefined'){
//             console.log("error.reponse undefined line 33 interceptor")
//             // alert(
//             //         'A server/network error occurred. ' +
//             //             'Looks like CORS might be the problem. ' +
//             //             'Sorry about this - we will get it fixed shortly.'
//             //     );
//             // return Promise.reject(error);
            
//         }
//         if (error.response.status === 401&&!originalRequest._retry &&originalRequest.url ===  '/auth/jwt/refresh/'){		   originalRequest._retry = true
//             console.log("refresh is not fresh any more");
// 			window.location.href = '/login/';
// 			return Promise.reject(error);
// 		}
//         refreshToken = localStorage.getItem('refreshToken')
        
//         if(refreshToken){
//             console.log("LS has a refresh token")
//             if(error.response.status ===401&&!originalRequest._retry){
//                 originalRequest._retry = true
                
//                 const now = Math.ceil(Date.now()/1000)
//                 console.log("now is ",now)
//                 const tokenRefreshPayload = JSON.parse(atob(refreshToken.split('.')[1]));
//                 const expTerm = tokenRefreshPayload.exp
//                 console.log("exp term: ",expTerm)
//                 if(expTerm>now){
//                     return axios.post('/auth/jwt/refresh/',{'refresh':refreshToken})
//                     .then((resp)=>{
//                         console.log("sending refresh & asking for new access token ==200?",resp.status)
//                         const newAccessToken = resp.data.access
//                         localStorage.setItem('accessToken',newAccessToken)
//                         this.$store.commit(mutationTypes.SET_ACCESS_TOKEN(resp.data.access ))      
//                         this.$store.commit(mutationTypes.SET_NEW_ACCESS_TOKEN_SUCCESS) 
//                         axios.defaults.headers['Authorization'] = 'JWT ' + response.data.access
//                         originalRequest.headers['Authorization'] = 'JWT ' + response.data.access;
//                         return axios(originalRequest)
//                     })
//                     .catch((err)=>{
//                         console.log("line 59 error")
//                     })
//                 }

//             }
//             else{
//                 console.log('Refresh token is expired', tokenParts.exp, now);
//                 window.location.href = '/login/';
//                 // option N2
                   //localStorage.removeItem('accessToken');
                  //window.location.reload(true);
//             }
//         }
//         else{
//             console.log('Refresh token not available.');
// 				window.location.href = '/login/';
//         }       
//     }
// )



export default axios

