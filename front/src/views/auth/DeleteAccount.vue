<template>
    <div class="container">
        <div class="messages row mb-2 mt-4">
        <div v-if="errorMsg" class="errorMsg col-md-12">
            Error message: {{errorMsg}}
            <b-icon icon="exclamation-circle-fill" variant="danger"></b-icon>        
        </div>      
            
        <div v-if="successMsg" class="successMsg col-md-12">
            <b-icon icon="three-dots" animation="cylon" font-scale="4"></b-icon>  {{successMsg}} 
            <b-icon icon="exclamation-circle-fill" variant="info"></b-icon>
        </div>
        </div>
         <div class="row">            
            <div class="col col-md-10" >
                <div class='container'>
                    <div v-if="isLoading"><app-loader></app-loader></div>
                    <div class="wrapper">
                        <h1>To delete your account you need to enter your password:</h1>                        
                        <b-form @submit.prevent="requestDeleteAccount">
<!-- current password -->
                            <b-form-group id="input-group-2" class="required">          
                                <label id="input-group-2" class="control-label">Current password</label> 
                                <div class="row border">
                                    <div class="col-md-10 sync">
                                    <b-form-input
                                        id="input-2"
                                        class="search-text"
                                        autocomplete="off"
                                        v-model.trim="currentPsw"
                                        :type="showPassword ? 'text' : 'password'"
                                               
                                    >
                                    <!-- @blur="$v.currentPsw.$touch()"
                                        :class="{ 'is-invalid warning': this.$v.currentPsw.$error }"    -->
                                    </b-form-input>
                                    </div>
                                    <div class="col-md-2  pt-1 point-it">
                                    <span ><b-icon-eye @click="toggleShowPws" /></span>
                                </div>
                                </div>
<!--psw front side errors  -->
                           <!-- <b-form-invalid-feedback v-if="currentPswRequired" 
                            >{{ fieldRequired }}
                            </b-form-invalid-feedback>     -->
<!--psw serv side errors  -->
                            <div class="errMsg" v-if="servErr.currentPsw">
                                
                            </div>
                            <div class="warn" v-if="servErr.currentPsw">
                                <ul>
                                    <li v-for="pswErr in servErr.currentPsw" :key="pswErr.id">
                                        {{pswErr}}
                                    </li>
                                </ul>
                            </div>     

                        </b-form-group>

<!-- django server is down -->
{{servErr}}
                        <div v-if="servErr.servDown" class="warn col-md-12 mb-3">
                            Error message: {{servDownMsg}}
                            <b-icon icon="exclamation-circle-fill" variant="danger"></b-icon>        
                        </div>  
                        <div class="errorMsg col-md-12 mb-3" v-if="tokenExp">
                        <div class="px-1">{{unauthMsg}}</div>
                        </div>
<!-- buttons group -->
                    <b-row class="text-center mt-4">
                        <b-col cols="6">
                            <b-button type="submit"  variant="success">Submit</b-button>
                            <!-- <b-button type="submit"  variant="success" :disabled="formInValid">Submit</b-button> -->
                        </b-col >
                        <b-col cols="6">
                            <b-button  @click="goTo('Home')" variant="primary">Home</b-button>
                        </b-col>
                    </b-row>    
                </b-form>  
<!--go home!--  -->
               
            </div>                    
          </div> 
        </div>
      </div>
    </div>
</template>
<script>
import {actionTypes} from '@/store/modules/auth'
import {mapState} from 'vuex'
import AppLoader from '@/components/Loader'
export default {
    name:'AppDeleteAccount',
    components:{         
         AppLoader
    },
    data(){
        return{
            successMsg:"",
            errorMsg:"",
            currentPsw:'',            
            //front-side vars/errors
            //fieldRequired: "This field is required",
            // toggle password visiabilty
            showPassword: false,            
            // server side err's
            servErr:{servDown:false},
            servDownMsg:'Sorry. Our server"s exper temp problems.Try again a little bit later',            
            tokenExp:false,
            unauthMsg:'Sorry your login session is expired.Please login agaon',                     
            
        }
    },
    // validations: {
    //     currentPsw:{required},
    //     newPsw: {
    //     required,
    //     minLength: minLength(8),
    //     maxLength: maxLength(128),
    //     },
        
    // },
    computed:{
        ...mapState({
            isLoading:state=>state.auth.isLoading,                                       
           
        }),
        // formInValid() {
        //     return this.$v.$invalid
        // },        
        // currentPswRequired() {
        // return this.$v.currentPsw.$dirty && !this.$v.currentPsw.required;
        // },        
    },
    methods:{
        requestDeleteAccount(){           
            this.$store.dispatch(actionTypes.deleteAccount,{
                currentPsw:this.currentPsw,                
            })
            .then((resp)=>{
                // also for servErr's
                console.log("in  vue",resp)
                // console.log(Object.keys(resp))
                if(resp.servDown){
                    console.log("dj serv is down, see rr?")
                    this.servErr.servDown = true
                }else if(resp.status === 204){
                    console.log("account deleted, re-directing to home");
                    this.successMsg = "Your account has been deleted"
                    setTimeout(()=>{
                        this.$router.push({name:"home"});  
                                         
                    },5000)
                     
                }else if(resp.status===401){
                    console.log("status 401 unauth-ed",resp.status)                                      
                    this.tokenExp = true                
                   
                }else if(resp.status===400){
                    console.log("status 400 calling",resp.status)
                    // let msg = resp.pswErr
                     this.servErr.currentPsw = resp.pswErr                  
                }
            }).catch((err)=>{
                // incorrect psw => page not found 404 !
                console.log(Object.keys(err))
                console.log("final err",err)
                this.errorMsg = "Something went wrong during password change. Be sure that you use a correct password" 
                
            })            
        },
        toggleShowPws() {
        this.showPassword = !this.showPassword;
        },       
    }
}
</script>

<style scoped>
.successMsg{
    background-color: rgb(192, 219, 164);
    height: 50px;
}

.warn {
  background-color: rgb(240, 194, 194);
  padding:3px 10px;
  border-radius: 3px;
  /* height: 50px; */
}
.control-label::after{
    content: " *";
    color: red;
}
.border{
  display: flex;
  margin: 0px;
  border-color: transparent;
}
.border .col-md-10 {
  padding-left:0px;
}
.col-md-10 >input{
    border-color: transparent;
    border-radius: 5px;
}
/* input .search-txt */
/* .search-txt {
    background: rgba(255,255,255,0.4);
    border: 1px solid rgba(128,128,128,0.4);
    border-radius: 15px;
    outline: none;
    float:left;
    padding: 0 10px;
    color:#000;
    font-size: 20px;
    transition:0.4s;
    line-height: 40px;
    width:200px;
    margin-right: .3rem;
}

.search-txt[type=password] {
  -webkit-transition: background-color .35s ease-in-out;
  transition: background-color .35s ease-in-out;
  -webkit-transition:width .35s ease-in-out;
  transition: width .35s ease-in-out;
}
.search-txt[type=password]:focus {
  width: 250px;
  background-color: rgba(255,255,255,0.6);
  border-color:gray;
} */

</style>