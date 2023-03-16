<template>
  <div class="profile" @mouseenter="showCard = true" @mouseleave="showCard = false">
    <div class="circle"> {{firstCharName}} </div>
    <div class="card-container">
      <img v-if="showCard" alt="arrow" class="arrow" src="../../assets/pp_arrow.svg"
           width="17" />
      <img v-else alt="arrow" class="arrow" src="../../assets/pp_arrow_side.svg"
           height="17"/>
      <transition name="fade">
        <div class="card" v-if="showCard" @mouseleave="showCard = false" @mouseenter="showCard = true">
          <p style=" margin-top: 16px; margin-bottom: 16px">{{ $t('message.topbar.signInAs') }}
            <b>{{ store.getters["auth/username"] }}</b></p>
          <div class="separator"></div>
          <div class="hoverMouse" @click="logout">{{ $t('message.topbar.logOut') }} <i class="material-icons md-light"
                                                                                       style="font-size: 16px; vertical-align: middle; margin-left: 5px">logout</i>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script lang="ts">
import store from "../../store";
import {defineComponent} from "vue";
import { logout } from "../../api/AuthServices";

export default defineComponent({
  name: "AppearingCard",
  data() {
    return {
      rotation: 0,
      showCard: false
    }
  },
  methods: {
    logout() {
      logout();
      this.$router.push('/')
    }
  },
  computed: {
    store() {
      return store
    },
    rotatedImage() {
      if (this.showCard) {
        this.rotation = 0
      } else {
        this.rotation = 90
      }
      return {
        transform: 'rotate(' + this.rotation + 'deg)' + 'translate(-50%, 50%)'
      }
    },

    firstCharName(): string {
      return this.store.getters["auth/username"].charAt(0).toUpperCase();
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
  transform-origin: center center;
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
  margin-right: 5px;
}

/*.circle::before {*/
/*  content: "U";*/
/*}*/

.separator {
  width: 90px;
  height: 1px;
  background-color: var(--color-lines);
  margin: 0 10px;
}

.hoverMouse {
  cursor: pointer;

}
</style>
