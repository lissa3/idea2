<template>
    <div class="container">
      <div class="flash-msg"></div>
        <div class="row mx-auto  my-5 main-login">            
            <div class="col col-md-10 col-sm-6 py-3" > 
              <b-form @submit.prevent="onSubmit"> 
<!-- email  -->
                <b-form-group
                  id="input-group-1"
                  label="Email"
                  label-for="input-1"
                  description="We'll never share your email with anyone else."
                >               
                  <b-form-input
                    id="input-1"
                    v-model.trim="email"
                    autocomplete="on"
                    type="email"
                    placeholder="Enter email"
                    :class="{ 'is-invalid warning': this.$v.email.$error }"
                    @blur="$v.email.$touch()"           
                  ></b-form-input>                                            
<!-- front-side errors email-->            
                <b-form-invalid-feedback v-if="emailRequired" 
                  >{{ fieldRequired }}
                </b-form-invalid-feedback>
                <b-form-invalid-feedback v-if="inValidEmail" 
                  >This field should be a valid email</b-form-invalid-feedback>
            </b-form-group>                  
<!-- server errors: email errors -->
                <div class="warn mb-1" v-if="emailErr">
                  <ul>
                    <li v-for="err in emailErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>
<!-- password-->
                <b-form-group id="input-group-2"  
                label="Password" label-for="input-2" class="mb-2">
                <div class="row border" >                
                <div class="col-md-10">
                  <b-form-input
                    id="input-2"
                    :type="showPassword ? 'text' : 'password'"
                    @blur="$v.psw.$touch()"
                    :class="{ 'is-invalid warning': this.$v.psw.$error }"                      
                    v-model.trim="psw"
                     autocomplete="off"
                    placeholder="Enter password"          
                  ></b-form-input>
                </div>
                <div class="col-md-2 border-0 pt-1 point-it">
                  <span><b-icon-eye @click="toggleShowPws" /></span>
                  
                </div>  
                </div>
<!-- front side password errors -->
                <b-form-invalid-feedback v-if="pswRequired" class="invalid-feedback"
                  >{{ fieldRequired }}
                </b-form-invalid-feedback>
                </b-form-group>   
<!-- server errors: password errors -->
                <div class="warn mb-1" v-if="pswErr">
                  <ul>
                    <li v-for="err in pswErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>   
<!-- server errors: non-field errors -->
                <div class="warn mb-1" v-if="nonFieldErr">
                  <ul>
                    <li v-for="err in nonFieldErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>
                <!-- django server is down -->
                <div class="warn mb-3" v-if="netWorkErr">
                  <div class="px-1">Sorry. Our server has temporary problems.Please try to login later</div>
                </div>
                <div class="warn mb-3" v-if="unAuthorized">
                  <div>{{unAuthorized}}</div>
                </div>
                <div class="warn mb-3" v-if="finalErr">
                  <div>Something went wrong during login session.</div>
                </div>
                <div class="flesh-msg mb-3" v-if="successMsg">
                  <div>{{successMsg}}</div>
                </div>
                <b-row >
                  <b-col cols="6">
                    <b-button type="submit" 
                    :disabled="formInValid" variant="success">Submit</b-button>
                  </b-col >       
                </b-row>
            <p class="mt-3">Not registed?<span class="mute-link"><router-link :to='{name:"signup"}'>  Sign Up</router-link></span>  </p>
        <p class="mt-3">Forgot your password?<span><router-link :to="{name:'resetForgotPsw'}"> Reset password</router-link></span></p>    
        
           
            </b-form> 
        <!-- <p class="mt-3">Not registed?<span class="mute-link"><router-link :to='{name:"signup"}'>Sign Up</router-link></span>  </p>
        <p class="mt-3">Forgot yout password?<span class="mute-link"><a href="#">Here</a></span></p> -->
      </div>
    </div>
  </div>         
</template>

<script>

import {required, email}  from "vuelidate/lib/validators";
import {actionTypes} from '@/store/modules/auth'
export default {
    name:'AppLogin',
     data(){
      return {
        user:{},
        email:'',
        psw:'',        
        status:'',        
        emailErr:null,
        pswErr:null,
        nonFieldErr:null,
        netWorkErr:null,
        unAuthorized:null,
        finalErr:false,
        successMsg:'',
        // front valid 
        fieldRequired: "This field is required",
        // toggle password visiabilty
        showPassword: false, 
      } 
    },
     validations: {
    email: { required, email },
    psw: { required },
    },
    computed:{
      formInValid() {
      return this.$v.$invalid;
    },
    pswRequired() {
      return this.$v.psw.$dirty && !this.$v.psw.required;
    },
    emailRequired() {
      return this.$v.email.$dirty && !this.$v.email.required;
    },
    inValidEmail() {
      return this.$v.email.$dirty && !this.$v.email.email;
    },
    },
     methods:{
       onSubmit(){
         let data={email:this.email,password:this.psw}
         // first request to get tokens
         this.$store.dispatch(actionTypes.login,data)
         .then((resp)=>{  
           console.log("got resp from store:",resp)
           if(resp.status ===200){
             console.log("Login comp and status 200")
           this.$store.dispatch(actionTypes.getUser)
           .then((resp)=>{ 
              console.log("do smth with this resp",resp)
              if(resp){
                console.log("status",resp.status)
                this.successMsg = "Success in login"
                setTimeout(()=>{
                 this.$router.push({name:"home"})
               },2000)
              }             
                                      
             }).catch((err)=>{
               console.log(err)
             })            
           }else if(resp.response.status === 401){
             // No active account found with the given credentials
             console.log(Object.keys(resp.response.data))
             this.unAuthorized = resp.response.data.detail 
             // serv.msg: No active account found with given creds( email OK,psw incorrect or both)          
           }else if(resp.response.status === 400){
             // This field (email/psw) may not be blank (user sent empty form)
             this.emailErr=resp.response.data.email
             this.pswErr=resp.response.data.password             
           } else{
             this.netWorkErr = 'Network Error; no response from the server'
           }        
         }) 
         .catch((err)=>{   
           // user banned?        
             console.log("catch in login component")
             console.dir(err) 
             alert("A server/network error occured.Sorry about this - we will get it fixed shortly. ");
                          
           })          
       },
       toggleShowPws() {
      this.showPassword = !this.showPassword;
    },
     }  
}
</script>
<style scoped>
.warn {
  background-color: rgb(240, 194, 194);
  border-radius: 3px;
}
.warn ul li{
  list-style-type:none;
}
.flesh-msg{
  background-color: darkgoldenrod;
}
.main-login {

  padding:2rem;
  background-color: blanchedalmond;
  box-shadow: 0 0 10px 10px rgba(0,0,0,.05);
  border-radius: 0.5rem;
} 
.point-it{
  cursor: pointer;
  background-color: white;
  margin-left: 0px;
  text-align: center;
}
.border{
  display: flex;
  margin: 0px;
  
}
.border .col-md-10 {
  padding-left:0px;
}


</style>