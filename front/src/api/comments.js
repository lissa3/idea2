import axios from '@/api/axios'
import simpleAPI from '@/api/plainAxios'

const sendRootComment = (commentData)=>{
    // need auth when create a comment
    // console.log("api line 6",commentData)
    return axios.post('/api/v1/ideas-collection/comments/',commentData)
}

const editComment = (commentId,commentData)=>{
    // need auth when create a comment
    // console.log("api line 6",commentData)
    return axios.patch(`/api/v1/ideas-collection/comments/${commentId}/`,commentData)
}

const deleteComment = (commentId)=>{
    // need auth when create a comment
    // console.log("api line 6",commentData)
    return axios.delete(`/api/v1/ideas-collection/comments/${commentId}/`)
}

const fetchAllComments = (ideaSlug)=>{
    // need auth when create a comment
    return simpleAPI.get(`/api/v1/idea/comments/${ideaSlug}/`)
}

export default {
    editComment,
    deleteComment,
    fetchAllComments,
    sendRootComment,
}
