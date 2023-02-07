<template>
  <div class="container">
    <Card>
      <div class="content">

        <div class="header">
          <div class="title">{{ $t('message.login-view.welcome') }}</div>
          <div class="subtitle">{{ $t('message.login-view.login') }}</div>
        </div>

        <div class="login-form">
          <div class="form">
            <div class="error" v-show="error">{{errorMessage}}</div>
            <div class="text-fields">
              <input @click="() => error = false" v-model="username" placeholder="Username"/>
              <input @click="() => error = false" v-model="password" placeholder="Password" type="password"/>
            </div>
            <div class="submit-field">
              <Button class="buttonStyling" @buttonClick="tryLoginSubmit" text="Submit"></Button>
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
import {login, validatePassword, validateUsername} from "../../../api/AuthServices";
import {defineComponent} from "vue";
import router from "../../../router";

export default defineComponent({
  name: "Login",
  components: {Tip, Button, Card},
  data: () => {
    return {
      username: "",
      password: "",
      error: false,
      errorMessage: "Something went wrong!"
    };
  },
  methods: {
    async tryLoginSubmit() {
        const response = await login(this.username, this.password)
        if (response.error != null) {
          this.error = true;
          return;
        }
        await router.push('/dashboard')
    }
  }
})
</script>

<style scoped>

.title {
  color: var(--color-text);
  font-weight: bold;
  font-size: 18px;
}

.subtitle {
  color: var(--color-default-text-textbox);
  font-weight: bold;
}

.content {
  padding: 0 1vw;
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
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  margin: 2vw 0;
}

.text-fields input {
  font-size: 16px;
  color: var(--color-text);
  font-weight: 1000;
  background: none;
  border: 1px solid var(--color-stroke);
  border-radius: 7px;
  padding: 7px;
  margin-bottom: 0;
  margin-top: 1.5vw;
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
  margin: 1.5vw;
}

.buttonStyling{
  color: var(--color-text)
}

</style>