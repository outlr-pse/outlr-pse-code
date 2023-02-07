<template>
     <div class="TopBar">
       <img alt="Outlr logo" @click="() => this.$router.push('/')" class="logo" src="../../assets/OutlrLogo.svg" width="125"/>

        <div style = "justify-self: end">
          <div v-if="is_authenticated" style="display: flex; align-items: center">
            <div v-if="this.$route.path !== '/create'" style="display: inline-block">
              <Button text="Create Experiment" :button-type="ButtonType.ACTIVE" :size="[200,40]"
                      @buttonClick="() => this.$router.push('/create')" :text-size="[15,700]" />
            </div>
            <AppearingCard/>
            <div style="width:30px; height:auto; display:inline-block;" />
         </div>

         <div v-else>
           <Button text="Log in" :button-type="ButtonType.TRANSPARENT"  @buttonClick="this.$router.push('/login')"/>
           <div style="width:5px; height:auto; display:inline-block;" />
           <Button text="Sign up" :button-type="ButtonType.OUTLINE" @buttonClick="this.$router.push('/signup')"/>
           <div style="width:15px; height:auto; display:inline-block;" />
         </div>
       </div>
     </div>
</template>

<script lang="ts">
import Button from "../basic/button/Button.vue";
import {ButtonType} from "../basic/button/ButtonType";
import {RouterLink} from "vue-router";
import AppearingCard from "./ProfileCollapsableCard.vue";

export default {
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
  methods: {
    ClickAction() {
      this.buttonStyle = this.buttonStyle === "" ? "createExperimentTopBar" : "";
      console.log("Button Clicked");
    }
  },
  computed: {
    ButtonType() {
      return ButtonType
    },
    is_authenticated() : boolean {
        // return this.$store.getters['auth/is_authenticated'];
        return false;
      },
    rotatedImage() : { transform: string; }{
      return {
        transform: 'rotate(' + this.rotation + 'deg)'
      }
    }
  }
}
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
  grid-template-columns: 1fr 1fr; /* two columns: logo, buttons */
  grid-gap: 10px; /* gap between cells, kann man weglassen */
  align-items: center;
  padding-right: 1rem;
  justify-content: space-between;
  height: var(--top-bar-height);
  width: 100%;
}


</style>