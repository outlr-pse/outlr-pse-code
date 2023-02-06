<template>
     <div class="TopBar">
       <img alt="Outlr logo" @click="() => this.$router.push('/')" class="logo" src="../assets/OutlrLogo.svg" width="125"/>

        <div style = "justify-self: end">
          <div v-if="is_authenticated" style="display: flex; align-items: center">
            <div v-if="this.$route.path !== '/create'" style="display: inline-block">
              <Button  @click="() => this.$router.push('/create')" :style-classes=buttonStyle text="Create Experiment" />
           </div>
           <div class="circle"/>
         </div>

         <div v-else>
           <Button text="Log in" :button-type="ButtonType.TRANSPARENT"  @buttonClick="this.$router.push('/login')"/>
           <div style="width:2px; height:auto; display:inline-block;" />
           <Button text="Sign up" :button-type="ButtonType.OUTLINE" @buttonClick="() => this.$router.push('/signup')"/>
         </div>
       </div>
     </div>
</template>

<script>
import Button from "./basic/button/Button.vue";
import {ButtonType} from "./basic/button/ButtonType";
import {RouterLink} from "vue-router";

export default {
  name: "Topbar",
  computed: {
    ButtonType() {
      return ButtonType
    }
  },
  components: {
    Button,
    RouterLink
  },
  methods: {
    push() {
      this.$router.push('/login')
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
  background-color: rgb(47, 41, 58, 0.95);
  color: #fff;
  font-size: 18px;
  display: grid;
  grid-template-columns: 1fr 1fr; /* two columns: logo, buttons */
  grid-gap: 10px; /* gap between cells, kann man weglassen */
  align-items: center;
  padding-right: 1rem;
  justify-content: space-between;
  height: var(--top-bar-height);
  width: 100%;
}

.circle {
  width: var(--top-bar-circle-size);
  height: var(--top-bar-circle-size);
  line-height: var(--top-bar-circle-size);
  border-radius: 50%;
  text-align: center;
  font-size: 23px;
  display: inline-block;
  background-color: var(--color-main);
  margin-left: 40px;
  margin-right: 7px;
}

.circle::before {
  content: "U";
}
</style>