<template>
  <div class="container">
    <Card>
      <div class="content">

        <div class="header">
          <div class="title">{{ $t('message.login-view.title') }}</div>
          <div class="subtitle">{{ $t('message.login-view.subtitle') }}</div>
        </div>

        <div class="login-form">
          <div class="error" v-show="error">{{ errorMessage }}</div>
          <div class="text-fields">
            <div>
              <input v-bind:class="{'errorInput':error}" class="username"
                   @click="() => error = false" v-model="username" placeholder="Username"/>
            </div>
            <div style="position:relative">
              <input v-bind:class="{'errorInput':error}" class="password"
                     @click="() => error = false" v-model="password" placeholder="Password"
                     :type="inputTypePassword"/>
              <span class="material-icons md-dark passwordIcon"
                    @click="toggleVisibilityPassword">{{visiblePassword}}</span>
            </div>

          </div>
          <div class="submit-field">
            <input v-bind:class="{'validSubmit': validInput, 'errorSubmit':error}" ref="submit" @click="tryLoginSubmit"
                   type="button" value="Continue">
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
import {login, validatePassword, validateUsername} from "../../../api/AuthServices";
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
      errorMessage: "Something went wrong!",
      inputTypePassword: "password",
      visiblePassword: "visibility"
    };
  },
  methods: {
    resetInputFields() {
      this.username = ""
      this.password = ""
    },
    toggleVisibilityPassword(){
      this.inputTypePassword = this.inputTypePassword === "password"  ? "text" : "password"
      this.visiblePassword = this.visiblePassword === "visibility_off" ? "visibility": "visibility_off"
      this.error = false;
    },
    async tryLoginSubmit() {

      if (!validateUsername(this.username) || !validatePassword(this.password, this.password)) {
        this.error = true;
        this.errorMessage = this.$t('message.login-view.errors.provided-credentials-wrong')
        this.resetInputFields()
        return;
      }

      const response = await login(this.username, this.password)
      if (response.error != null) {
        this.error = true
        this.errorMessage = this.$t(`message.login-view.errors.${response.error}`)
        this.resetInputFields()
        return;
      }
      await router.push('/')
    }
  },
})
</script>

<style scoped>
.passwordIcon {
  float: right;
  position: absolute;
  right: 18px;
  top: 13px;
  z-index: 90;
  color: var(--color-main-white);
  width: 24px;
  height: 24px;
  user-select: none;
}

.errorInput {
  border-color: var(--color-close-button) !important;
  background: none;
  color: var(--color-close-button) !important;
}

.error {
  font-size: 18px;
  font-weight: 500;
  border: 2px solid var(--color-close-button);
  color: var(--color-close-button);
  padding: 10px;
  border-radius: 7px;
}

.errorSubmit {
  background: var(--color-close-button) !important;
}

.container {
  height: 100%;
  align-items: center;
  display: flex;
  justify-content: center;
}

.tip {
  background: var(--color-auth-form-background);
  border: none;
  padding: 0;
  margin: 0;
}

.content {
  width: min(70vw, 325px);
  padding: 30px;
  display: grid;
  grid-template-rows: auto auto;
  gap: 30px;
}

.header {
  text-align: left;
  display: grid;
  gap: 7px;
}

.title {
  font-size: 22px;
  font-weight: 800;
}

.subtitle {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-stroke)
}

.login-form {
  display: grid;
  grid-template-rows: auto;
  gap: 30px;
}

.text-fields {
  display: grid;
  gap: 15px;
}

.valid {
  border: 2px solid green !important;
}

.validSubmit {
  background: green !important;
}

.login-form input {
  outline: none;
  font-size: 20px;
  font-weight: 800;
  padding: 10px;
  border-radius: 7px;
  border: none;
  color: var(--color-main-white);
}

.text-fields input {
  background: var(--color-background);
  border: 2px solid var(--color-stroke)
}

.text-fields input:focus {
  border: 2px solid var(--color-main)
}

.submit-field input {
  width: 100%;
  background: var(--color-main);
  color: var(--color-main-white)
}

.submit-field input:hover {
  filter: brightness(120%);
  cursor: pointer;
}


</style>
