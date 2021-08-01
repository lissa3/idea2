<template>
  <div class="container-fluid">
      <b-jumbotron header="Ideas" lead="Join us" class="text-center jum-tron">
        <p>World of ideas runs the world</p>
        
        <b-btn variant="success" href="#">Ideas</b-btn>
      </b-jumbotron>
    <!-- <div class="wrapper">
      <div class="bg"> Gold </div>
      <div class="fg"> Gold </div>
    </div> -->
    
  </div>
</template>
<script>
export default {
  name:'AppBanner'
}
</script>
<style scoped>
.jum-tron{
    height:300px;
}
.jumbotron{
    padding:1rem;
}
/* :root {
  --gold: #ffb338;
  --light-shadow: #77571d;
  --dark-shadow: #3e2904;
}
body {
  margin: 0;
}
* {
  box-sizing: border-box;
}

.wrapper {
  background: radial-gradient(#272727, #1b1b1b);
  display: grid;
  grid-template-areas: 'overlap';
  place-content: center;
  text-transform: uppercase;
  height: 100vh;
}
.wrapper > div {
  background-clip: text;  
  -webkit-background-clip: text;
  color: #363833;
  font-family: 'Poppins', sans-serif;
  font-weight: 900;
  font-size: clamp( 3em, 18vw, 15rem);
  grid-area: overlap;
  letter-spacing: 1px;
  -webkit-text-stroke: 4px transparent;
}
div.bg {
  background-image: repeating-linear-gradient( 105deg, 
    var(--gold) 0% , 
    var(--dark-shadow) 5%,
    var(--gold) 12%);
  color: transparent;
  filter: drop-shadow(5px 15px 15px rgb(180, 150, 150));
  transform: scaleY(1.05);
  transform-origin: top;
}
div.fg{
  background-image: repeating-linear-gradient( 5deg,  
    var(--gold) 0% , 
    var(--light-shadow) 23%, 
    var(--gold) 31%);
  color: #cbd3e2;
  transform: scale(1);
} */

</style>
