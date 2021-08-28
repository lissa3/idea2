const getFileNameFromUrl = (urlName)=>{
    console.log("url",urlName)
    const arr= urlName.split('\/')
    console.log("arr is",arr)
    return arr[arr.length-1]
         
    
        
}
export default getFileNameFromUrl