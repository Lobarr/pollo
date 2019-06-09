<template>
  <div id="app">
    <a-layout class="app-container">
      <a-layout-content class="app-content">
        <a-row
          align="middle"
          justify="center"
          type="flex"
        >
          <Title title="Pollo - Video / Audio Transcriber" />
        </a-row>
        <a-row class="accent-container">
          <a-select defaultValue="en-US" style="width: 120px" @change="handleAccentChange" v-model="accent">
            <a-select-option value="en-GB">en-GB</a-select-option>
            <a-select-option value="en-US">en-US</a-select-option>
          </a-select>
          <a-button icon="reload" id="redo-button" @click="handleRedo"></a-button>
        </a-row>
        <Uploader :accent="accent" />
        <Transcribed :body="bot" :loading="loading"/>
      </a-layout-content>
    </a-layout>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue';
import Vue from 'vue';
import VueSocketIO from 'vue-socket.io';
import Antd from 'ant-design-vue';
import { Uploader, Title, Transcribed } from './components';
import { notification, emit } from './utils';

Vue.use(Antd)

Vue.mixin({
  notification,
  emit,
});

Vue.use(new VueSocketIO({
    debug: true,
    connection: 'http://localhost:3000',
}));

export default {
  name: 'app',
  sockets: {
    status({ status, msg }) {
      this.$notification[status]({
        key: 'status',
        message: msg,
      });
      if (status === 'info' && msg === 'Transcribing') {
        this.loading = true;
      } else {
        this.loading = false;
      }
    },

    transcribe({ msg }) {
      this.bot = msg;
      this.loading = false;
    }
  },
  components: {
    Title,
    Uploader,
    Transcribed,
  },
  data()  {
    return {
      accent: 'en-GB',
      bot: `Hi, I'm your transcriber bot for today. Let me show you how smart I am :)`,
      loading: false,
    }
  },
  methods: {
    handleAccentChange(accent) {
      this.accent = accent;
    },

    handleRedo() {
      location.reload();
    }
  }
};
</script>

<style lang="scss">
  .app-container {
    height: 100vh;
    width: 100vw;
    .app-content {
      background-color: #5F758E;
      margin: 3em;
      border: 1px solid teal;
      border-radius: 1em;
      .accent-container {
        margin: 3em;
      }
    }
    #redo-button {
      margin-left: 0.5em;
    }
  }
</style>
