<template>
  <a-row
    class="upload-container"
  >
    <a-upload-dragger
      accept="video/*,audio/*"
      name="file"
      :multiple="false"
      action="http://localhost:3000/upload"
      @change="handleUpload"
    >
      <p class="ant-upload-text">Click or drag file to this area to upload</p>
    </a-upload-dragger>
  </a-row>
</template>

<script>

const UploadStatus = {
  UPLOADING: 'uploading',
  DONE: 'done',
  ERROR: 'error',
};

export default {
  name: 'Uploader',
  props: {
    accent: String,
  },
  methods: {
    handleUpload(ctx) {
      const { file } = ctx;
      const { status, name, response } = file;
      const { message } = response;

      if (status === UploadStatus.UPLOADING) {
        this.$notification.info({
          key: 'uploader',
          message: `${name} file uploading...`,
        });
      }

      if (status === UploadStatus.DONE) {
        this.$notification.success({
          key: 'uploader',
          message: `${name} file uploaded successfully.`,
        });

        this.$socket.emit('transcribe', {
          filename: name,
          accent: this.accent,
        });
      } else if (status === UploadStatus.ERROR) {
        this.$notification.error({
          key: 'uploader',
          message,
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
