<template>
  <a-row
    class="upload-container"
  >
    <a-upload-dragger
      accept="video/*,audio/*"
      name="file" 
      :multiple="true" 
      action="http://localhost:3000/upload" 
      @change="handleChange"
    >
      <p class="ant-upload-text">Click or drag file to this area to upload</p>
    </a-upload-dragger>
  </a-row>
</template>

<script>
import Vue from 'vue';
import utils from '../utils';

export default {
  name: 'Uploader',
  props: {
    accent: String,
  },
  methods: {
    handleChange(info) {
      const status = info.file.status;
      if (status == 'uploading') {
        this.$notification.info({
          key: 'uploader',
          message: `${info.file.name} file uploading...`,
        });
      }
      if (status === 'done') {
        this.$notification.success({
          key: 'uploader',
          message: `${info.file.name} file uploaded successfully.`,
        });
        this.$socket.emit('transcribe', {
          'fn': info.file.name,
          'accent': this.accent,
        })
      } else if (status === 'error') {
        this.$notification.error({
          key: 'uploader',
          message: info.file.response.msg,
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
  .upload-container {
    margin: 3em;
    height: 4em;
  }
</style>
