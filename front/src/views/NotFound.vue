<template>  
    <div class="bg"> 
      
          <h1>Sorry. Page not found</h1>        
        
       
    </div>  
</template>

<script>
export default {
  name: "notFound",
  // mounted() {
  //   setTimeout(this.goHome, 3500);
  // },
  methods: {
    goHome() {
      this.$router.push("/");
    },
    // goTo(direction){
    //   this.$router.push({name:direction});
    //   },
  },
};
</script>
<style  scoped>
body, html {
  height: 100%;
  margin: 0;
}

.bg {
  /* The image used */
  /* background-image: url("../assets/kon.jpg"); */

  /* Full height */
  height: 100vh; 

  /* Center and scale the image nicely */
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.bg > h1 {
  font-size: 100px;
  margin-bottom: 20px;
  color: #fff;
}


</style>