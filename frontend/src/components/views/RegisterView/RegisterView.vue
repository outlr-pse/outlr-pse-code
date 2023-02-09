<template>
  <div class="container">
    <Card class="container-card">
      <div class="content">
        <div class="header">
          <div class="title">{{ $t('message.register-view.title') }}
            <span v-bind:class="{'errorInput':error}" class="material-icons md-dark icon" @mouseenter="showTip = true"
                  @mouseleave="showTip = false"> info </span>
            <transition name="fade">
              <Card class="card" v-if="showTip" @mouseenter="showTip = true" @mouseleave="showTip = false">
                {{ $t('message.register-view.requirements') }}
              </Card>
            </transition>
          </div>


          <div class="subtitle">{{ $t('message.register-view.subtitle') }}</div>
        </div>

        <div class="login-form">
          <div class="error" v-show="error">{{ errorMessage }}</div>
          <div class="text-fields">
            <!--            <div>-->
            <input v-bind:class="{'valid': usernameInput(username), 'errorInput':error}" class="username"
                   @input="usernameInput" @click="() => error = false" v-model="username" placeholder="Username"/>
            <!--            </div>-->
            <div style="position:relative">
              <input v-bind:class="{'valid': passwordInput(passwordInput), 'errorInput':error}" class="password"
                     @input="passwordInput" @click="() => error = false" v-model="password" placeholder="Password"
                     :type="inputTypePassword"/>
              <span class="material-icons md-dark passwordIcon"
                    @click="toggleVisibilityPassword">{{ visiblePassword }}</span>
            </div>
                         <div style="position:relative">
            <input v-bind:class="{'valid': passwordRepeatedInput(passwordRepeated), 'errorInput':error}"
                   class="passwordRepeated" @input="passwordRepeatedInput" @click="() => error = false"
                   v-model="passwordRepeated" placeholder="Re-enter Password" :type="inputTypePasswordRepeated"/>
                        <span class="material-icons md-dark passwordIcon" @click="toggleVisibilityPasswordRepeated">{{visiblePasswordRepeated}}</span>
                         </div>
          </div>
          <div class="submit-field">
            <input v-bind:class="{'validSubmit': validInput, 'errorSubmit':error}" ref="submit"
                   @click="tryRegisterSubmit" type="button" value="Create Account">
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
      errorMessage: "Something went wrong!",
      showTip: false,
      visiblePassword: "visibility",
      inputTypePassword: "password",
      visiblePasswordRepeated: "visibility",
      inputTypePasswordRepeated: "password",
    };
  },
  methods: {
    usernameInput(event: any) {
      let isValid = validateUsername(this.username)
      this.withValidInput[0] = isValid;
      return isValid
    },
    passwordInput(event: any) {
      let isValid = validatePassword(this.password);
      this.withValidInput[1] = isValid;
      return isValid;
    },
    passwordRepeatedInput(event: any) {
      let isValid = this.passwordRepeated === this.password && this.withValidInput[1];
      this.withValidInput[2] = isValid;
      return isValid;
    },
    resetInputFields() {
      this.username = ""
      this.password = ""
      this.passwordRepeated = ""
      for (let i = 0; i < this.withValidInput.length; i++) {
        this.withValidInput[i] = false
      }
    },
    async tryRegisterSubmit() {

      if (!validateUsername(this.username) || !validatePassword(this.password)
          || this.password != this.passwordRepeated) {
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
    },
    toggleVisibilityPassword() {
      this.inputTypePassword = this.inputTypePassword === "password" ? "text" : "password"
      this.visiblePassword = this.visiblePassword === "visibility_off" ? "visibility" : "visibility_off"
    },
    toggleVisibilityPasswordRepeated() {
      this.inputTypePasswordRepeated = this.inputTypePasswordRepeated === "password" ? "text" : "password"
      this.visiblePasswordRepeated = this.visiblePasswordRepeated === "visibility_off" ? "visibility" : "visibility_off"
      this.error = false
    }
  },
  computed: {
    validInput() {
      for (let i = 0; i < this.withValidInput.length; i++) {
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

input {
  width: 325px;
  margin: 0 50px;
}

.card {
  position: absolute;
  margin: 0;
  top: 82%;
  left: 95%;
  width: 95%;
  z-index: 91;
  background: var(--color-topbar);
  font-weight: 400;
  font-size: 16px;
  white-space: break-spaces;
}

.passwordIcon {
  float: right;
  position: absolute;
  /*top: 0.8rem;*/
  /*right: 0.8rem;*/
  /*padding: 0.5rem;*/
  right: 60px;
  top: 19px;
  z-index: 90;
  color: var(--color-default-text-textbox);
  width: 24px;
  height: 24px;
  user-select: none;
}

.passwordIcon:hover {
  cursor: pointer;
}

.icon {
  color: var(--color-main);
  width: auto;
  text-align: right;
  margin: 0;
}

.errorInput {
  border-color: var(--color-close-button) !important;
  background: none;
  color: var(--color-close-button) !important;
}

.errorSubmit {
  background: var(--color-close-button) !important;
}

.error {
  font-size: 18px;
  font-weight: 500;
  border: 2px solid var(--color-close-button);
  color: var(--color-close-button);
  padding: 10px;
  border-radius: 7px;
  margin: 0 50px;
}

.container {
  height: 100%;
  align-items: center;
  display: flex;
  justify-content: center;
}

.container-card {
  width: 450px;
  background: var(--color-auth-form-background);
  border: none;
  padding: 0;
  margin: 0;
}

.content {
  display: grid;
  grid-template-rows: auto auto;
  gap: 30px;
  max-width: 100%;

}

.header {
  margin: 50px 50px 0 50px;
  text-align: left;
  display: grid;
  gap: 7px;
}

.title {
  font-size: 22px;
  font-weight: 800;
  display: flex;
  justify-content: space-between;
  position: relative;
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
  /*margin: 0 50px;*/
}

.text-fields {
  display: grid;
  gap: 15px;
}

.valid {
  border: 2px solid var(--color-running) !important;
}

.validSubmit {
  background: var(--color-running) !important;
}

.login-form input {
  outline: none;
  font-size: 20px;
  font-weight: 800;
  padding: 14px;
  border-radius: 7px;
  border: none;
}

.text-fields input {
  background: var(--color-background);
  border: 2px solid var(--color-stroke);
  color: var(--color-main-white);
}

.text-fields input:focus {
  border: 2px solid var(--color-main)
}

.submit-field {
  margin: 0 4px 50px 4px;
}

.submit-field input {
  background: var(--color-main);
  color: var(--color-main-white);
}

.submit-field input:hover {
  filter: brightness(120%);
  cursor: pointer;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}


</style>
