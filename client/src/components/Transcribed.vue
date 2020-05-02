<template>
  <a-row class="transcribed-container">
    <a-comment>
      <a slot="author">Bot</a>
      <a-avatar
        icon="user"
        alt="Bot"
        slot="avatar"
        shape="square"
      />
      <div class="loading-container">
        <a-spin v-if="loading" />
      </div>
      <p slot="content" v-show="!loading">{{body}}</p>
    </a-comment>
  </a-row>
</template>

<script>
export default {
  name: 'Transcribed',
  props: {
    body: String,
    loading: Boolean,
  },
};
</script>

<style lang="scss" scoped>
  .transcribed-container {
    background-color: white;
    margin: 3em;
    padding: 1em;
    border-radius: 0.6em;
    min-height: 40%;
    max-height: 50%;
    overflow: scroll;
    .loading-container {
      text-align: center;
    }
  }
</style>
