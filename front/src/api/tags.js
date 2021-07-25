import simpleAPI from '@/api/plainAxios'

const getTags = ()=>{    
    // console.log("simple API for tags firing")
    return simpleAPI.get(`/api/v1/tags/`)
}
const getByTagName = (tagSlug)=>{    
    console.log("simple API for tags name firing")
    return simpleAPI.get(`/api/v1/tags-name/${tagSlug}`)
}


export default {    
    getTags,
    getByTagName
    

}    