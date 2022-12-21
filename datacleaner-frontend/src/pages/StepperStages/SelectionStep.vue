<template>
  <div style="text-align: center;">
    <span style="font-size:1.5em">Select your cleaning strategy for each column </span><br>
    <q-icon
      name="abc"
      size="2.5em"
    /> - String column  |
    <q-icon
      name="123"
      size="2.5em"
    /> - Numeric column
  </div><br>

  <q-separator /> <br>
  <div
    v-for="col in data.data"
    :key="col.name"
    class="col-lg-4 col-md-6 col-xs-12 q-pr-md q-pb-md"
  >
    <ColumnDisplay
      @on-change="updateColumnState"
      :column="col"
    />
  </div>
</template>

<script>
import ColumnDisplay from "src/components/ColumnDisplay.vue";

export default {
    props: {
        data: { type: Object, required: true },
    },
    setup() {
        return {
          columnsState: {}
        };
    },
    emits: ['columnStrategyChange'],
    methods: {
      updateColumnState (value) {
        this.columnsState[value.name] = value
        this.$emit('columnStrategyChange', this.columnsState)
      }
    },
    components: { ColumnDisplay }
};
</script>
