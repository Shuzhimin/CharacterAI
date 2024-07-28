<template>
  <div>
    <h3>欢迎<span>{{user}}</span></h3>

  </div>
</template>

<script>
export default {
  name: "Welcome",
  created() {
    this.user=window.sessionStorage.getItem('username')
  },
  data () {
    return{
      user: '',
    }
  }
}
</script>

<style scoped>

</style>
