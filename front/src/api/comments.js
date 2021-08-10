import axios from '@/api/axios'
import simpleAPI from '@/api/plainAxios'

const sendRootComment = (commentData)=>{
    // need auth when create a comment
    // console.log("api line 6",commentData)
    return axios.post('/api/v1/ideas-collection/comments/',commentData)
}

const fetchAllComments = (ideaSlug)=>{
    // need auth when create a comment
    return simpleAPI.get(`/api/v1/idea/comments/${ideaSlug}`)
}

export default {
    sendRootComment,
    fetchAllComments
}
