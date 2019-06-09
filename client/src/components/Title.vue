<template>
  <h2>{{title}}</h2>
</template>

<script>
export default {
  name: 'Title',
  props: {
    title: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  @import url('https://fonts.googleapis.com/css?family=Roboto+Mono&display=swap');

  h2 {
    font-family: 'Roboto Mono', monospace;
    margin: 1em;
    color: #D3D5D4;
  }
</style>
