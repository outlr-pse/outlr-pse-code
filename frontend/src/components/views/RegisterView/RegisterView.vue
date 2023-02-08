<template>
  <div class="container">
    <Card>
      <div class="content">

        <div class="header">
          <div class="title">{{ $t('message.register-view.title') }}</div>
          <div class="subtitle">{{ $t('message.register-view.subtitle') }}</div>
        </div>

        <div class="login-form">
          <div class="form">
            <div class="error" v-show="error">{{errorMessage}}</div>
            <div class="text-fields">
              <input @click="() => error = false" v-model="username" placeholder="Username"/>
              <input @click="() => error = false" v-model="password" placeholder="Password" type="password"/>
              <input @click="() => error = false" v-model="passwordRepeated" placeholder="Re-enter Password" type="password"/>
            </div>
            <div class="submit-field">
              <input class="buttonStyling" @click="tryRegisterSubmit" type="button" value="Create account">
            </div>
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
import {login, register, validatePassword, validateUsername} from "../../../api/AuthServices";
import {defineComponent} from "vue";
import router from "../../../router";
import store from "../../../store";

export default defineComponent({
  name: "Login",
  components: {Tip, Button, Card},
  data: () => {
    return {
      username: "",
      password: "",
      passwordRepeated: "",
      error: false,
      errorMessage: "Something went wrong!"
    };
  },
  methods: {
    async tryRegisterSubmit() {
      if (!validateUsername(this.username) || !validatePassword(this.password, this.password)
        ||  this.password != this.passwordRepeated) {
          this.error = true;
          return;
        }

      const response = await register(this.username, this.password)
      if (response.error != null) {
        this.error = true;
        return;
      }
      console.log(store.getters["auth/isAuthenticated"])
      console.log(store.getters["auth/username"])
      await router.push('/')
    }
  }
})
</script>

<style scoped>

.title {
  color: var(--color-text);
  font-weight: bold;
  font-size: 22px;
}

.subtitle {
  color: var(--color-default-text-textbox);
  font-weight: bold;
  font-size: 20px;
}

.content {
  padding: 0 1vw;
  max-width: max(35vh, 300px);
}

.error {
  margin-top: 1vw;
  border-radius: 7px;
  padding: 7px;
  border: 1px solid red;
  color: red;
}

.header {
  text-align: left;
  padding: 1vw 0;
  height: 20%
}

.login-form {
  border-top: 1px solid var(--color-stroke);
  height: 65%;
  padding: 0 1vw;
}

.container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%
}

.text-fields {
  display: grid;
  grid-template-rows: 1fr 1fr 1fr;
  grid-row-gap: 1vw;
  margin: 2vw 0;
}

.text-fields input {
  font-size: 18px;
  color: var(--color-text);
  font-weight: 1000;
  background: none;
  border: 1px solid var(--color-stroke);
  border-radius: 7px;
  padding:10px;
}

.form {
  display: flex;
  justify-content: space-evenly;
  flex-direction: column;
  padding: 0;
  height: 100%;
}

.login-form {
  padding: 0 1vw;
}

.submit-field {
  color: var(--color-text);
  margin-bottom: 1vw;
}

.buttonStyling{
  color: var(--color-text);
  font-size:20px;
  width:100%;
  padding:10px;
  background: var(--color-main);
  border-radius: 7px
}

</style>
