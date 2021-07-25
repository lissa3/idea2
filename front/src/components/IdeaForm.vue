<template>
    <div>
      <section >
          <h1>Form </h1>
<!-- loader  submit         -->
            <div class="col-xs-12 col-md-10 py-3 text-center offset-md-1">
              <app-loader v-if="isSubmitting"></app-loader>
            </div>
 <!-- errors          -->
        <!-- django server is down -->
            <div class="warn mb-3" v-if="errors.netWorkErr">
              <div class="px-1">{{errors.netWorkErr}}</div>
            </div>      
 <!-- form                   -->
          <b-form
                @submit.prevent="onSubmit"      
                enctype="multipart/form-data"
                novalidate > 
<!-- imported component categories                          -->
                <app-categ-input
                    :setCategNames="categories"
                    :categ="categ"
                    @getCateg="readCategVal">
                   >
                </app-categ-input>
<!-- server errors category  -->                 
                <div class="warn mb-1" v-if="errors.categErr">
                  <ul>
                    <li v-for="err in errors.categErr" :key="err.id">
                      <!-- {{err}} -->
                      Choose a category,please
                      <!-- Invalid pk "0" - object does not exist. -->
                    </li>
                  </ul>
                </div>
                <b-form-group id="input-group-1" label="Title:" label-for="input-1" class="text-left">
                    <b-form-input           
                    id="input-1"
                    v-model.trim="title"
                    ></b-form-input>
                </b-form-group>
<!-- server errors title         -->
                <div class="warn mb-1" v-if="errors.titleErr">
                  <ul>
                    <li v-for="err in errors.titleErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>
<!-- front-side errors title-->      
                <b-form-group id="input-group-2" label="Lead Text:" label-for="input-2" class="text-left">
                    <b-form-input
                    id="input-2"
                    v-model.trim="leadText"
                    ></b-form-input>
                </b-form-group>
<!-- server side leadText errors (incl: Ensure this field has no more than 240 characters)                -->
                <div class="warn mb-1" v-if="errors.leadTextErrr">
                  <ul>
                    <li v-for="err in errors.titleErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>
<!-- front-side errors  leadText-->      
                <b-form-group id="input-group-3" label="Main Text:" label-for="input-3" class="text-left">
                    <!-- <b-form-input          
                    id="input-3"                    
                    v-model.trim="mainText"
                    ></b-form-input> -->
                    <b-form-textarea
                    id="input-3"
                    v-model="mainText"
                    placeholder="What is this idea about..."
                    
                    rows="3"
                    max-rows="6"
                    ></b-form-textarea>
           
                </b-form-group>
<!-- server side leadText errors                 -->
                <div class="warn mb-1" v-if="errors.mainTextErr">
                  <ul>
                    <li v-for="err in errors.mainTextErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>         
<!-- front-side errors  mainText-->      
                <b-form-group id="input-group-4" label="Tags:" label-for="input-4" class="text-left">
                    <b-form-input          
                    id="input-4"
                    v-model.trim = "tags"
                    ></b-form-input>
                </b-form-group>
<!-- server side leadText errors                 -->
                <div class="warn mb-1" v-if="errors.tagsErr">
                    <h5>Tags error: {{errors.tagsErr}}</h5>
                  
                </div>                         
<!-- front-side errors  tags-->             
          <b-form-group id="input-group-5" label="Upload File" inline>
            <div class="file-wrap">
              <label class="file-select mr-sm-2">
                <div class="select-button">
                  <span v-if="thumbnail">Selected File: {{ thumbnail.name }}</span>
                  <span v-else>Select File</span>
                </div>
                <input
                  id="thumbnail"
                  type="file"
                  ref="file"
                  accept=".jpg,.jpeg,.png"
                  @change="onFileChange"
                  @click="clearCheckboxUploadFile"
                />
              </label>
              <span class="clearable-file-input">
                <label class="text-mute">
                  <input
                    id="checkbox_img"
                    v-model="checked"
                    type="checkbox"
                    ref="check"
                    @change="detachFile"
                    name="thumbnail_clear"
                  />
                  Remove file
                </label>
              </span>
            </div>
            <p class="text-mute">Allowed images with extentions: .png,.jpg/.jpeg</p>
            <p>state thumbnail {{thumbnail}}</p>
            <!-- front-side errors upload file-->         
          </b-form-group> 
<!-- server side errors upload file(too big; ext not allowed) -->            
            <div v-if="errors.thumbnailErr">
              <div class="warn mb-1" v-if="errors.thumbnailErr">
                  <ul>
                    <li v-for="err in errors.thumbnailErr" :key="err.id">
                      {{err}}
                    </li>
                  </ul>
                </div>  
            </div>                           
 <!-- front-side errors upload file-->
            <div class="msg mb-2 py-2" v-if="localErr" :class="`${localErr ? 'is-danger' : 'is-success'}`">
                <div class="msg-body" v-if="alertHeavyFile">{{ alertHeavyFile }}</div>
                <div class="msg-body" v-if="formatNotAllowed">{{ formatNotAllowed }}</div>            
            </div>
            <b-button type="submit" variant="primary" class="pull-xs-right btn btn-large btn-success"
            :disabled="isSubmitting">
                Publish Idea
            </b-button>     
          </b-form>
             
      </section>        
    </div>    
</template>                
                
<script>
import AppCategInput from '@/components/categs/CategInput'
import AppValidationErrors from '@/components/ValidationErrors'
import AppLoader from '@/components/Loader'
import tagsHelp from '@/helpers/tagsHelper'
import optimizePhoto from '@/assets/js/resizeIt.js'

export default {
    name:'AppIdeaForm',
    components:{
        AppCategInput,
        AppLoader,
        AppValidationErrors,
        
    },
    props:{
        categories:{
           type:Array,
           required:true

        },
        initialValues:{
            type:Object,
            required:true
        },
        errors:{
            type:Object,
            required:false
        },
        isSubmitting:{
            type:Boolean,
            required:true
        }
    },
    data(){
        return {
            // TODO: categs,author
            categ:this.initialValues.categ,
            title: this.initialValues.title,
            leadText: this.initialValues.leadText,
            mainText: this.initialValues.mainText,                
            featured: this.initialValues.featured,
            tags: this.initialValues.tags,
            
            // upload file vars
            thumbnail: this.initialValues.thumbnail,                 
            checked: false, 
            localErr:false,
            formatNotAllowed:null,
            resizedThumbnail:null,                            
            alertHeavyFile:null,           
        }
    },
    methods:{
        onSubmit(){
            const data = new FormData()
            data.append('categ ', this.categ)
            data.append('title', this.title)
            data.append('lead_text', this.leadText)
            data.append('main_text', this.mainText)            
            // console.log("form component calling ....with a form")
            // console.log(data)
            if(this.tags){
            // clean tag string from #$56 ect
            const cleanTags = tagsHelp.trimInputTag(this.tags);
            console.log("tags string is",cleanTags)
            data.append('tags', cleanTags)         
            }
            if (this.resizedThumbnail) {
            data.append('thumbnail', this.resizedThumbnail)
          } else {
            // user removes attached file so this.thumbnail = ""
            data.append('thimbnail', '')
          }
            this.$emit('ideaSubmit',data)
            // console.log("do you seen me in parent?")
        },
        readCategVal(cat){
            console.log(cat)
            this.categ = cat
        },
        async onFileChange() {
          // clear prev error msg and uncheck state
          this.$refs.check.checked = false
          this.localErr = false
          // this.browserFileUploadMsg = ''
          console.log("initial path to a file",this.$refs.file.value)
          // temp variable for uploaded img to check size && type;
          let img = this.$refs.file.files[0]
          const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg']
          // const MAX_SIZE = 20
          const MAX_SIZE = 2000000
          const tooBig = img.size > MAX_SIZE
          if (allowedTypes.includes(img.type) && !tooBig) {
            // accept image only if type &&size OK; this thumnail will keep the name/size of uploaded img
            this.thumbnail = img
            console.log('check is OK,initial size is:', this.thumbnail.size)
            console.log("path to a file after OK validation",this.$refs.file.value)
            // TODO: css/js nice uploading bar
            // this.browserFileUploadMsg = 'loading this file'
            // resize uploaded image with custom js util (aprox 7-8- times)
            const resizedPhoto = await optimizePhoto(this.thumbnail)
            // resizedPhoto is blob|=> convert it to a file
            this.resizedThumbnail = new File([resizedPhoto], this.thumbnail.name)
            // console.log('created a resized img')
          } else {
            this.localErr = true
            // this.browserFileUploadMsg = tooBig ? `File too large.MAX sise is ${MAX_SIZE / 1000}kB`: `Only images are allowed`
            if (tooBig) {             
              this.alertHeavyFile = `File too large.MAX sise is ${MAX_SIZE / 1000}kB`
              // this.browserFileUploadMsg = `File too large.MAX sise is ${MAX_SIZE / 1000}kB`
            }
            if (!allowedTypes.includes(img.type)) {              
              this.formatNotAllowed = `Only images are allowed`
              // this.browserFileUploadMsg = `Only images are allowed`
            }
          }
          
        },
        clearCheckboxUploadFile(){
          // if upload button clicked|=> intention to upload a (new) file|=> checkbox input gets cleared
          console.log("upload file: make checkbox input clear")
          this.$refs.check.checked = false // boolean
        },
        detachFile(){
          console.log("checkbox clicked")
          
          console.log("detaching file started with intial path:",this.$refs.file.value)
          this.$refs.file.value = '' // path to file on local machine
          console.log("after detachement path is:",this.$refs.file.value)
          this.localErr = false
          // this.thumbnail = null
          this.thumbnail = ''
          this.resizedThumbnail = null
          // this.alertHeavyFile = false;
          // this.formatNotAllowed = false;
        }
    }    
}
</script>
<style scoped>
.warn{
    background-color: cornsilk;
}  
/* style Digital Ocean */
.file-select > .select-button {
  padding: 0.5rem;
  color: white;
  background-color: #84898e;
  border-radius: 0.3rem;
  text-align: center;
  font-weight: bold;
}
/* Don't forget to hide the original file input! */
.file-select > input[type='file'] {
  display: none;
}
/* end digitalOcaen */
.text-mute {
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
}
.is-danger {
  background-color: #c72534c9;
}
.is-success {
  background-color: cadetblue;
}                      
 /* .input-area {
  outline: none;
  border: 1px solid #d8d8d8 !important;
  box-shadow: none !important;
  border-radius: 0 !important;
  background-color: #ffffff;
  height: 150px;
  flex-grow: 1;
  padding: 10px !important;
  font-family: inherit;
  transition: 0.3s;
  font-size: 16px;
  font-weight: 300;
  height: 400px;
  color: #000000;
  letter-spacing: 1px;
  overflow: hidden;
  overflow-y: scroll;
  resize: none;
 }                   */
                

</style>