<template>
  <div class="TopBar">
    <img alt="Outlr logo" @click="$router.push('/')" class="logo" src="../../assets/OutlrLogo.svg"
         width="125"/>
    <h1> {{ topbarMessage }} </h1>
    <div style="justify-self: end">
      <div v-if="isAuthenticated" style="display: flex; align-items: center">
        <div v-if="$route.path !== '/create'" style="display: inline-block">
          <Button :text="$t('message.topbar.createExperiment')" :button-type="ButtonType.ACTIVE" :size="[200,40]"
                  @buttonClick="() => $router.push('/create')" :text-size="[15,700]"/>
        </div>
        <AppearingCard/>
        <div style="width:30px; height:auto; display:inline-block;"/>
      </div>

      <div v-else>
        <Button text="Log in" :button-type="ButtonType.TRANSPARENT" @buttonClick="$router.push('/login')"/>
        <div style="width:5px; height:auto; display:inline-block;"/>
        <Button text="Sign up" :button-type="ButtonType.OUTLINE" @buttonClick="$router.push('/register')"/>
        <div style="width:15px; height:auto; display:inline-block;"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Button from "../basic/button/Button.vue";
import {ButtonType} from "../basic/button/ButtonType";
import {RouterLink} from "vue-router";
import AppearingCard from "./ProfileCollapsableCard.vue";
import {defineComponent} from "vue";
import store from "../../store";


export default defineComponent({
  name: "Topbar",
  components: {
    AppearingCard,
    Button,
    RouterLink
  },
  data() {
    return {
      buttonStyle: {
        type: String,
        default: "createExperimentTopBar"
      },
      rotation: {
        type: Number,
        default: 90
      }
    }
  },
  computed: {
    ButtonType() {
      return ButtonType
    },
    store() {
      return store
    },
    isAuthenticated(): boolean {
      return store.getters['auth/isAuthenticated'];
    },

  }
})
</script>

<style scoped>
.logo {
  display: block;
  margin-left: 1rem;
  cursor: pointer;
}

.TopBar {
  position: fixed;
  background-color: var(--color-topbar);
  color: #fff;
  font-size: 14px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr; /* two columns: logo, text and buttons */
  grid-gap: 10px; /* gap between cells, kann man weglassen */
  align-items: center;
  padding-right: 1rem;
  justify-content: space-between;
  height: var(--top-bar-height);
  width: 100%;
  z-index: 1000;
}


</style>