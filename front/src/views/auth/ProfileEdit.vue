<template>
  <div class="container py-md-5 py-4">    
    <div class="row">
      <!-- <div class="long">       -->
       <div class="col col-md-10 py-2 mx-auto">
        <div v-if="profile" class="card mb-3 p-2" style="width: 56rem;" >
        <h1>Change your profile,</h1>   
        <div class="card-body">
<!-- form -->
          <b-form               
          @submit.prevent="onSubmit"
          ref="profileSubmitForm"
          enctype="multipart/form-data">
<!-- website -->
          <b-form-group id="input-group-1" label="Your Web Site:" label-for="input-1">
                <b-form-input
                  id="input-1"
                  v-model="website"
                  placeholder="Enter website address"                  
                ></b-form-input>
          </b-form-group>    
<!-- front  website errors -->
<!-- <p >Errs:{{servResp}}</p> -->
<!-- backend website errors   -->              
          <div v-if="servResp.websiteErrs">
                <ul>
                  <li class="warning" v-for="err in servResp.websiteErrs" :key="err.id">
                    {{ err }}
                  </li>
                </ul>
          </div>              
<!-- bio -->
          <b-form-group id="input-group-2" label="Bio :" label-for="input-2">
            <b-form-input
              id="input-2"
              placeholder="Bio"
              v-model.trim="bio"                                      
            ></b-form-input>
          </b-form-group>
<!-- front side bio errors -->
<!-- server bio errors -->
          <div v-if="servResp.bioErrs">
              <ul>
                <li class="warning" v-for="err in servResp.bioErrs" :key="err.id">
                  {{ err }}
                </li>
              </ul>
          </div>
<!-- (profile) image  -->
                <b-form-group id="input-group-5" label="Upload File">
                  <div class="file-wrap">          
                  <label class="file-select mr-sm-2">
                    <div class="select-button">
                      <span v-if="image">Current file File: {{imageLink}}</span>
                      <span v-else>Select File</span>
                    </div>   
                  <input
                    id="image"
                    type="file"
                    ref="file"
                    accept=".jpg,.jpeg,.png"
                    @change="onFileChange"
                    @click="clearCheckboxUploadFile"                     
                  />
                  </label>
                  <span class="clearable-file-input">
                      <label class="text-mute">Remove file
                      <input
                        id="checkbox_img"
                        type="checkbox"
                        ref="check"
                        v-model="checked"
                        name="image_clear"
                        @change="detachFile"
                      />
                      </label>
                  </span>                        
                  </div>
                  <p class="text-mute">Allowed images with extentions: .png,.jpg/.jpeg</p> 
<!-- front-side errors upload file-->
                   <div class="msg" v-if="browserFileUploadMsg" :class="`${localErr?'is-danger':'is-success'}`">
                      <div class="msg-body">{{browserFileUploadMsg}}</div>
                  </div>  
<!-- server side errors upload file(too big; ext not allowed) -->
                  <!-- <div v-if="servImgErrs">
                    <ul>
                      <li class="warning" v-for="err in servImgErrs" :key="err.id">
                        {{ err }}
                      </li>
                    </ul>
                  </div> -->
                </b-form-group>
                <b-button type="submit" class="btn btn-secondary"
                  >Edit It</b-button>                                
                </b-form>
<!-- general errors          -->                 
<!-- django server is down or err-500 -->
          <div class="warning mb-3 mt-3" v-if="servResp.netWorkErr">
            <div class="px-1">{{servResp.netWorkErr}}</div>
          </div>                 
        </div>
      </div>
      </div>
    <!-- </div> -->
    </div>  
  </div>
</template>
              
            
<script>
import {mapGetters} from 'vuex'
import {getterTypes} from '@/store/modules/auth'
import {actionTypes} from '@/store/modules/profile'

import {mapState} from 'vuex'
export default {
  name:'ProfileEdit',
  data(){
      return {     
        bio:'',
        checked:false,
        image:'',
        website:'',
        servResp:{
          status:null,
          bioErrs:null,
          imageErrs:null,
          websiteErrs:null,          
          netWorkErr:null,          
        },
      }
    },
  computed:{
      ...mapState({            
            profile:state=>state.profile.data,
            isLoading:state=>state.profile.isLoading,
            error:state=>state.profile.error,
                      
        }),       
        ...mapGetters({
          currentUser:getterTypes.currentUser,
        }),   
    
  },
  methods:{
      onSubmit(){
        // console.log('editing profile')
        const unid = this.currentUser.unid
        const profileData = new FormData()
        // console.log(unid,this.website,this.bio)
        profileData.append('bio',this.bio)
        profileData.append('website',this.website)        
        this.$store.dispatch(actionTypes.editPersonalInfo,{unid,profileData})
        .then((resp)=>{
          console.log("from store resp",resp)
          if(resp.status ===200){
            this.$router.push({name:'accountProfile',params:{unid:unid}})
          }else if(resp.servDown){
            this.servResp.netWorkErr = 'Sorry. Our server is enduring some problems.Please try later'
          }else if(resp.status === 500){
             this.servResp.netWorkErr = 'A server/network error occured.Sorry about this - we will get it fixed shortly.'
          }else{
            console.log("errror 400?",resp.status)
            this.servResp.status = resp.status
            this.servResp.websiteErrs = resp.websiteErr
            this.servResp.imageErrs = resp.imageErr
            this.servResp.bioErrs = resp.bioErr
            
          }
        }).catch((err)=>{
          console.log("final error",err)
        })
      },
      detachFile(){
        console.log('detaching file')
      },
      onFileChange(){
        console.log('file changing')
      },
      clearCheckboxUploadFile(){
        console.log('clear checkbox upload')
      }
    },
    created(){
      // console.log("create and got profile",this.profile)
      let src = this.profile
      this.website = src.website
      this.bio= src.bio
      this.image=src.image
    
  }    
}
</script>
<style scoped>

body {
  height: 100vh;
  margin: 0; padding: 0;

  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;

  font-family: 'Nunito', sans-serif;
  background-color: blanchedalmond;
  /* color: rgb(50, 50, 50); */
}
.warning{
  background-color: #e4b1b6;
  border-radius: 5px;
  padding:5px 10px;
}
/* style Digital Ocean */
.file-select > .select-button {
  padding: 0.5rem;
  /* color: white; */
  background-color: #d8dee4;
  border-radius: 0.3rem;
  text-align: center;
  font-weight: bold;
}
/* Don't forget to hide the original file input! */
.file-select > input[type='file'] {
  display: none;
}
/* end digitalOcaen */

/* .text-mute {
  font-size: 16px;
}
.file-wrap {
  display: flex;
  justify-content: space-around;
  padding: 0.5rem;
}
.msg {
  border-radius: 6px;
  color: white;
} */

  

</style>
