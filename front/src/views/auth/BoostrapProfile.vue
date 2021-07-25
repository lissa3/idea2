<template> 
  <section class="row min-vh-100">
      <main >
      <!-- <main :style="{ background: back }"> -->

  <div class="card">

    <!-- <img class="avatar" :src="picture"> -->

    <div class="infos">
      <div class="name capitalize">
        {{ profile.name }}
      </div>
      <div class="birth">
        <i class="fas fa-fw fa-birthday-cake"></i> birth 
      </div>
      <div class="email">
        <i class="fas fa-fw fa-envelope"></i> email 
      </div>
      <div class="phone">
        <i class="fas fa-fw fa-phone"></i> phone 
      </div>
      <div class="nationality capitalize">
        <i class="fas fa-fw fa-globe-americas"></i> nationality
      </div>
    </div>

  </div>

  <div class="refresh">
    <i class="fas fa-fw fa-random"  data-text="Random"></i>
    <i class="fas fa-fw fa-venus"  data-text="Female"></i>
    <i class="fas fa-fw fa-mars" data-text="Male"></i>
  </div>

  <div class="copy">
    <!-- Made with <a href="https://uinames.com/">UI Names API</a> and <a href="https://fr.vuejs.org/">Vue.js</a> -->
  </div>

</main>
  </section> 
</template>
            
<script>
// import {actionTypes} from '@/store/modules/profile'
import {mapState} from 'vuex'
export default {
  name:'ProfileDetail',
  computed:{
      ...mapState({
            
            profile:state=>state.profile.data,
            isLoading:state=>state.ideas.isLoading,
            error:state=>state.ideas.error,
                      
        }),
    noImgShow(){      
      return this.profile.image===null   
     
        
      }
    
  }
}
</script>
<style scoped>
.custom-wrap{
  background-color: blanchedalmond;
} 

body {
  height: 100vh;
  margin: 0; padding: 0;

  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;

  font-family: 'Nunito', sans-serif;
  color: rgb(50, 50, 50);
}
main {
    height: 100%;
    width: 100%;

    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: row;
}
.card {
      width: 470px;
      min-height: 185px;
      display: flex;

      padding: 10px;
      border-radius: 5px;
      /* box-shadow:  */
      background: rgba(255, 255, 255, .8);
}
.avatar {
        width: 100px;
        height: 100px;
        margin-right: 10px;
        border-radius: 50%;
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
        border: 4px solid rgba(255, 255, 255, .5);
}
.infos {
        flex: 1 1 auto;
        display: flex;
        flex-direction: column;
}
/* */

.refresh {
      display: flex;
      flex-direction: column;

      margin-left: 40px;
}
i {
        position: relative;
        height: 40px;
        width: 40px;
        margin: 10px 0;
        font-size: 110%;
        line-height: 40px;
        background: rgba(255, 255, 255, .8);
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);;
        border-radius: 50%;
        cursor: pointer;

        transition: background .2s ease-in-out, box-shadow .2s ease-in-out;
}
i:hover {
          background: white;
          box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);;
}
i::after {
    opacity: 1;
}
        

i::after {
          content: attr(data-text);
          position: absolute;
          /* left: calc(100% + #{$global_gap}); */
          top: 50%;
          transform: translateY(-50%);
          font-size: 80%;
          font-family: 'Nunito', sans-serif;
          line-height: initial;
          background: white;
          padding: 4px;
          border-radius: 1000px;
          box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
          pointer-events: none;
          opacity: 0;
          transition: opacity .2s ease-in-out;
      


@media only screen and (max-width: 800px) {
    main {
      flex-direction: column !important;
      font-size: 80%;

      .card {
        max-width: 80%;
        width: auto;
        min-height: 150px;
      }

      .refresh {
        flex-direction: row;

        margin-left: 0;
        margin-top: 30px;

        i {
          margin: 0 10px;

          &:after {
            display: none;
          }
        }
      }
    }
  }
}
.copy {
    position: absolute;
    bottom: 0; right: 0;
    padding: 2px;
    color: white;
}
    a {
      color: inherit;
    }
  

</style>
