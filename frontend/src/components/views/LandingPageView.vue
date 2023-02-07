<template>
  <div class="home">
    <div class="homeLogo">
      <img alt="Outlr logo" style="width: 100%" src="../../assets/OutlrLogo.svg"/>
      <h1>Effective subspace outlier analysis</h1>
    </div>

    <div v-if="isAuthenticated" class="dashboard">
        <Button  @buttonClick="redirect('dashboard')" :button-type="ButtonType.DARKPURPLENAVIGATETODASHBOARD"
                 text="Navigate to Dashboard" :size="[543,90]" :text-size="[25, 400]" start-icon="expand_more"/>
    </div>


    <div v-else class="signUp">
      <Button style="display: inline-block" @buttonClick="redirect('register')"
              :button-type="ButtonType.DARKPURPLESIGNUP" text="Sign up" :size="[140,70] " />
      <div style="width: 40px; height:auto; display:inline-block;" />
     <Button style="display: inline-block; cursor: not-allowed"  :button-type="ButtonType.OUTLINE" text="Try it out" :size="[140,70]" />
    </div>

  </div>
</template>

<style scoped>
.home {
  display: grid;
  grid-template-areas:
      "."
      "logo"
      "logo"
      "signup"
      "dashboard";
  grid-template-rows: 1fr 1fr 1fr  1fr 1fr;
  background-image: url(../../assets/Gradient.svg);
  background-size: cover;
}

.homeLogo {
  grid-area: logo;
  align-self: end;
  justify-self: center;
}

.signUp {
  grid-area: signup;
  justify-self: center;
}

.dashboard {
  grid-area: dashboard;
  align-self: end;
  justify-self: center;
  margin-bottom: 20px;
}
</style>

<script lang="ts">
import Button from "../../components/basic/button/Button.vue";
import router from "../../router";
import store from "../../store";
import {defineComponent} from "vue";
import {ButtonType} from "../basic/button/ButtonType";

export default defineComponent( {
  name: "LandingPageView",
  components: {Button},
  data(){
    return{
      buttonStyle: "",
    }
  },
  methods: {
    redirect(path: string) {
      router.push('/' + path)
    },
    logout() {
      store.dispatch('auth/logout')
    }
  },
  computed : {
    ButtonType() {
      return ButtonType
    },
    isAuthenticated() : boolean {
        // return store.getters['auth/is_authenticated'];
      return true;
    }
  }
})

</script>