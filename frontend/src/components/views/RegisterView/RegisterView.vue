<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css">
  <div class="container">
    <Card>
      <div class="content">

        <div class="header">
          <div class="title">{{ $t('message.register-view.title') }}</div>
          <div class="subtitle">{{ $t('message.register-view.subtitle') }}</div>
        </div>

        <div class="login-form">
            <div class="error" v-show="error">{{errorMessage}}</div>
            <div class="text-fields">
              <input v-bind:class="{'valid': usernameInput(username), 'errorInput':error}" class="username" @input="usernameInput" @click="() => error = false" v-model="username" placeholder="Username"/>
              <input v-bind:class="{'valid': passwordInput(passwordInput), 'errorInput':error}" class="password" @input="passwordInput" @click="() => error = false" v-model="password" placeholder="Password" type="password"/>
              <input v-bind:class="{'valid': passwordRepeatedInput(passwordRepeated), 'errorInput':error}" class="passwordRepeated" @input="passwordRepeatedInput" @click="() => error = false" v-model="passwordRepeated" placeholder="Re-enter Password" type="password"/>
            </div>
            <div class="submit-field">
              <input v-bind:class="{'validSubmit': validInput}" ref="submit" @click="tryRegisterSubmit" type="button" value="Create account">
            </div>
        </div>
      </div>
    </Card>
  </div>
</template>


<script lang="ts">
import Card from "../../basic/Card.vue";
import Button from "../../basic/button/Button.vue";
import Tip from "../../basic/Tip.vue";
import {register, validatePassword, validateUsername} from "../../../api/AuthServices";
import {defineComponent} from "vue";
import router from "../../../router";
import store from "../../../store";

export default defineComponent({
  name: "Register",
  components: {Tip, Button, Card},
  data: () => {
    return {
      withValidInput: [false, false, false],
      username: "",
      password: "",
      passwordRepeated: "",
      error: false,
      errorMessage: "Something went wrong!"
    };
  },
  methods: {
    usernameInput(event:any){
      let isValid = validateUsername(this.username)
      this.withValidInput[0] = isValid;
      return isValid
    },
    passwordInput(event:any){
      let isValid = validatePassword(this.password);
      this.withValidInput[1] = isValid;
      return isValid;
    },
    passwordRepeatedInput(event:any){
      let isValid = this.passwordRepeated === this.password && this.withValidInput[1];
      this.withValidInput[2] = isValid;
      return isValid;
    },
    resetInputFields() {
      this.username = ""
      this.password = ""
      this.passwordRepeated = ""
      for (let i=0; i < this.withValidInput.length; i++) {
        this.withValidInput[i] = false
      }
    },
    async tryRegisterSubmit() {

      if (!validateUsername(this.username) || !validatePassword(this.password)
        ||  this.password != this.passwordRepeated) {
          this.error = true;
          this.errorMessage = this.$t('message.register-view.errors.provided-credentials-wrong')
          this.resetInputFields()
          return;
        }

      const response = await register(this.username, this.password)
      if (response.error != null) {
        this.error = true
        this.errorMessage = this.$t(`message.register-view.errors.${response.error}`)
        this.resetInputFields()
        return;
      }
      await router.push('/')
    }
  },
  computed: {
    validInput() {
      for (let i=0; i < this.withValidInput.length; i++) {
        if (!this.withValidInput[i]) {
          return false
        }
      }
      return true;
    }
  }
})
</script>

<style scoped>
.errorInput{
  border-color: var(--color-main) !important;
  background: none;
  color: var(--color-main)!important;
}

.container{
  height:100%;
  align-items: center;
  display: flex;
  justify-content: center;
}

.tip{
  background:var(--color-auth-form-background);
  border: none;
  padding: 0;
  margin:0;
}

.content {
  width: min(70vw, 325px);
  padding: 30px;
  display:grid;
  grid-template-rows: auto auto;
  gap:30px;
}

.header{
  text-align: left;
  display:grid;
  gap: 7px;
}

.title{
  font-size: 22px;
  font-weight: 800;
}

.subtitle{
  font-size:20px;
  font-weight: 700;
  color: var(--color-stroke)
}

.login-form{
  display: grid;
  grid-template-rows: auto;
  gap: 30px;
}

.error{
  font-size:18px;
  font-weight: 500;
  border: 2px solid var(--color-main);
  color:var(--color-main);
  padding: 10px;
  border-radius: 7px;
}

.text-fields{
  display:grid;
  gap:15px;
}

.valid{
  border: 2px solid green !important;
}

.validSubmit{
  background: green !important;
}

.login-form input{
  outline:none;
  font-size:20px;
  font-weight: 800;
  padding: 10px;
  border-radius: 7px;
  border:none;
}

.text-fields input{
  background: var(--color-background);
  border: 2px solid var(--color-stroke);
  color:var(--color-main-white);
}

.text-fields input:focus{
  border: 2px solid var(--color-main)
}

.submit-field input{
  width:100%;
  background: var(--color-main);
  color:var(--color-main-white)
}

.submit-field input:hover{
  filter: brightness(120%);
  cursor: pointer;
}




</style>
