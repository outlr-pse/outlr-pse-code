<template>
  <div class="home">
    <div class="homeLogo">
      <img alt="Outlr logo" style="width: 40em" src="../../assets/OutlrLogo.png"/>
      <h1>{{ $t('message.landingPage.slogan') }}</h1>
    </div>

    <div v-if="isAuthenticated" class="dashboard">
        <Button  @buttonClick="redirect('dashboard')" :button-type="ButtonType.DARKPURPLENAVIGATETODASHBOARD"
                 :text="$t('message.landingPage.navigateDashboard')" :size="[543,90]" :text-size="[25, 400]" start-icon="expand_more"/>
    </div>


    <div v-else class="signUp">
      <Button style="display: inline-block; margin-top: 30px" @buttonClick="redirect('register')"
              :button-type="ButtonType.DARKPURPLESIGNUP" :text="$t('message.landingPage.signUp')" :size="[140,70] " />
      <div style="width: 40px; height:auto; display:inline-block;" />
     <Button style="display: inline-block; cursor: not-allowed"  :button-type="ButtonType.OUTLINE" :text="$t('message.landingPage.tryItOut')" :size="[140,70]" />
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
  margin-bottom: 5vh;
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
    }
  },
  computed : {
    ButtonType() {
      return ButtonType
    },
    isAuthenticated() : boolean {
      return store.getters['auth/isAuthenticated'];
    }
  }
})

</script>