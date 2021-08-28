<template>
  <div id="app">  
    
    <Menu></Menu>  
    <router-view/>
  </div>
</template>

<script>
import Menu from '@/components/Menu'
export default {
  name:'App',
  components:{
    Menu
  }
}
</script>

<style>
html, body { 
  height: 100%;}
.full-page{ 
  height: 100vh;
  width: 100vw;
}
.container-fluid{
    height:100vh;
  }

.container, .row.justify-content-center.align-items-center {
  height: 100%;
  min-height: 100%;
} 
.warn {
  background-color: rgb(240, 194, 194);
  border-radius: 3px;
  padding:5px 10px;
}
/* .container {
    width: 600px;
    height: 350px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: inline-flex;
}  */
/* comment form  */
.comment-form-invisible{
  display: none;
}
.show-comment-form{
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  min-height: 100px;
  max-width: 100%;
  padding: 0.5rem 1rem;
  border:1px solid black;
}
/* comment button */
input[type=submit] {
  background-color: #e2cca8;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
input[type=submit]:hover {
  background-color: #d1860c;
}
input[type=text],  textarea {
  width: 100%; 
  padding: 12px; 
  border: 1px solid #ccc;
  border-radius: 4px; 
  box-sizing: border-box;
  margin-top: 6px; 
  margin-bottom: 16px; 
  resize: vertical;
  outline:none;
  /* for scroll-bar in IE */
  overflow: auto;
  
}
/* textarea focus {background-color:#000;color:#FFF;} */
/* comments to display */

.comment-body{
  border:1px solid black;
  border-radius: 3px; 
}

</style>
