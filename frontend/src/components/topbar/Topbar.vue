<template>
  <div class="TopBar">
    <img alt="Outlr logo" @click="logoClick()" class="logo" src="../../assets/OutlrLogo.svg"
         width="125"/>
    <h1> {{ topbarMessage }} </h1>
    <div style="justify-self: end">
      <div v-if="isAuthenticated" style="display: flex; align-items: center">
        <div v-if="$route.path !== '/create'" style="display: inline-block">
          <ButtonComponent :text="$t('message.topbar.createExperiment')" :button-type="ButtonType.ACTIVE" :size="[200,40]"
                  @buttonClick="() => $router.push('/create')" :text-size="[15,700]"/>
        </div>
        <AppearingCard/>
        <div style="width:30px; height:auto; display:inline-block;"/>
      </div>

      <div v-else>
        <ButtonComponent :text="$t('message.topbar.logIn')" :button-type="ButtonType.TRANSPARENT" @buttonClick="$router.push('/login')"/>
        <div style="width:5px; height:auto; display:inline-block;"/>
        <ButtonComponent :text="$t('message.topbar.signUp')" :button-type="ButtonType.OUTLINE" @buttonClick="$router.push('/register')"/>
        <div style="width:15px; height:auto; display:inline-block;"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import ButtonComponent from '../basic/button/ButtonComponent.vue'
import { ButtonType } from '../basic/button/ButtonType'
import AppearingCard from './ProfileCollapsableCard.vue'
import { defineComponent } from 'vue'
import store from '../../store'

export default defineComponent({
  name: 'Topbar',
  components: {
    AppearingCard,
    ButtonComponent
  },
  data () : {

  } {
    return {

    }
  },
  computed: {
    ButtonType () {
      return ButtonType
    },
    store (): any {
      return store
    },
    isAuthenticated (): boolean {
      return store.getters['auth/isAuthenticated']
    },
    topbarMessage (): string {
      let msg:string = ''
      const path = this.$route.path
      if (path === '/') {
        msg = ''
      } else if (path === '/create') {
        msg = this.$t('message.topbar.createAnExperiment')
      } else if (path === '/login') {
        msg = this.$t('message.topbar.logIn')
      } else if (path === '/register') {
        msg = this.$t('message.topbar.signUp')
      } else if (path === '/dashboard') {
        msg = this.$t('message.topbar.dashboard')
      } else if (path.startsWith('/experiment/')) {
        msg = 'Experiment Result'
      } else {
        msg = '. __ .'
      }
      return msg
    }
  },
  methods: {
    logoClick() {
      if(this.isAuthenticated){
        this.$router.push('/dashboard')
      } else {
        this.$router.push('/')
      }
    }
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
