<template>
  <div style="text-align: center">
    <div class="row">
      <div class="col-4" />
    </div>
    
    <q-btn
      color="primary"
      id="dlButton"
      label="DOWNLOAD CLEAN DATA"
      size="xl"
      @click="submit"
    />
  </div>
</template>


<script>
import axios from "axios";

export default {
    props: {
        data: { type: Object, required: true },
        filename: {type: String, required: true}
    },
    setup() {
        return {
            
        };
    },
    methods: {
        submit() {
            const stringified = JSON.stringify(this.data)
            const res = axios({
                method: 'post',
                url: 'http://127.0.0.1:5000/clean',
                data: JSON.stringify({'filename': this.filename, 'data': this.data}),//{'data': this.data, 'filename': this.filename},
                headers: { 'Content-Type': 'application/json' },
                responseType: 'blob'
            }).then((response) => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'clean_' + this.filename);
                document.body.appendChild(link);
                link.click();
            })
            console.log(res)
            
            
        }

    },
    components: {} 
};
</script>
