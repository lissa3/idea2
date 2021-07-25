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
/* .container {
    width: 600px;
    height: 350px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: inline-flex;
}  */

</style>
