<template>
  <span style="font-size:medium; font-weight:500;"> Select your .csv file, upload it and then click "Continue"</span>
  <q-uploader
    label="Upload a .csv file"
    url="http://127.0.0.1:5000/upload"
    style="width: 100%"
    accept=".csv"
    @uploaded="uploaded"
    :max-files="1"
    :style="{backgroundColor: 'transparent'}"
  />
</template>

<script>
export default {
  setup () {
    return {};
  },
  emits: ['finished'],
  methods: {
    uploaded ({ files, xhr }) {
      console.log("File Uploaded");
      let res = JSON.parse(xhr.response);
      const data = res.data
      this.$emit("finished", {
        data: data,
        fileName: files[0].name
      });
      console.log("Emitted finish event");
    }
  },
};
</script>
