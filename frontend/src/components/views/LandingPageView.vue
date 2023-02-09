<template>
  Landing page
  <Button @click="logout()" text="Logout"></Button>
</template>

<script lang="ts">
import Button from "../basic/button/Button.vue";
import {logout} from "../../api/AuthServices";

export default {
  name: "LandingPageView",
  methods: {logout},
  components: {Button}
}
</script>

<style scoped>

</style>