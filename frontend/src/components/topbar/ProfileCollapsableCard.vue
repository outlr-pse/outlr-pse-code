<template>
  <div class="profile" @mouseenter="showCard = true" @mouseleave="showCard = false">
    <div class="circle"/>
    <div class="card-container">
      <img alt="arrow" @click="() => $router.push('/')" class="arrow" src="../../assets/pp_arrow.svg"
           width="13" :style="rotatedImage"/>
      <transition name="fade">
        <div class="card" v-if="showCard" @mouseleave="showCard = false" @mouseenter="showCard = true">
          <p style=" margin-top: 16px; margin-bottom: 16px">Signed in as <b>{{ store.getters["auth/username"] }}</b></p>
          <div class="separator"></div>
          <a href="./logout">Logout <i class="material-icons md-light"
                                       style="font-size: 16px; vertical-align: middle; margin-left: 5px">logout</i></a>
        </div>
      </transition>
    </div>
  </div>
</template>

<script lang="ts">
import store from "../../store";
import {defineComponent} from "vue";

export default defineComponent({
  name: "AppearingCard",
  data() {
    return {
      rotation: {
        type: Number,
        default: 90
      },
      showCard: false
    }
  },

  computed: {
    store() {
      return store
    },
    rotatedImage(): { transform: string } {
      return {
        transform: 'rotate(' + this.rotation + 'deg)'
      }
    }
  }
})
</script>


<style scoped>

.profile {
  margin-left: 15px;
  display: flex;
  align-items: center
}

a {
  text-decoration: none;
  color: inherit;
}

.card-container {
  position: relative;
  margin-left: 15px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .8s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.card {
  display: block;
  position: absolute;
  top: calc(var(--top-bar-height) / 2 - 10px);
  left: -100px;
  right: 0;
  bottom: 0;
  width: 110px;
  height: 110px;
  background-color: rgb(47, 41, 58, 0.70);
  z-index: 100;
  border-radius: 12px;
  border: 1px solid var(--color-stroke);
  font-size: 14px;
  transition: all 0.25s ease-in-out;
}


.arrow {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translate(-50%, 50%);
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

.separator {
  width: 90px;
  height: 1px;
  background-color: var(--color-lines);
  margin: 0 10px;
}
</style>
