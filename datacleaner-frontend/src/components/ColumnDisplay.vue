<!--ColumnDisplay component is responsible for the operation selection boxes for each column in the selection steps-->
<template>
  <q-expansion-item
    expand-separator
    :icon="column.type == 'NUMERIC' ? '123' : 'abc'"
    :label="column.name"
    :caption-lines="2"
    
    :header-style="{textAlign: 'center'}"
    :caption="'Total values: ' + column.total_values + ' | Unique values: '
      + column.unique_values + ' | Empty values: ' + column.empty_values"
  >
    <q-card
      class="text-black q-pa-sm q-ml-xl q-mr-xl"
      style="background: transparent"
    >
      <!-- Radio buttons for operation type selection: Clean, ignore or remove column -->
      <q-card-section>
        <div class="row text-center">
          <div
            class="q-ml-lg text-left col-12"
          >
            <div>
              <q-radio
                v-model="strategyModel"
                val="Clean"
                label="Clean column"
              />
              <q-radio
                v-model="strategyModel"
                val="Nothing"
                label="Make no changes"
              />
              <q-radio
                v-model="strategyModel"
                val="Remove"
                label="Remove column"
              />
            </div>
            <!-- Cleaning operations selection -->
            <div v-if="strategyModel=='Clean'"> 
              Null values handling strategy: <q-select
                outlined
                ref="null_values"
                v-model="nullModel"
                :options="nullOptions"
                label="Null handling strategy"
              />
              <div
                class="q-pa-md"
                style="max-width: 300px"
              >
                <q-input
                  v-if="nullModel?.includes('custom') && column.type == 'NUMERIC'"
                  v-model="nullCustomValue"
                  mask="#########"
                  filled
                  autogrow
                />
                <q-input
                  v-if="nullModel?.includes('custom') && column.type != 'NUMERIC'"
                  v-model="nullCustomValue"
                  mask="NNNNNNNNNN"
                  filled
                  autogrow
                />
              </div>
              <br>
              <div
                v-if="column.type == 'NUMERIC'"
              >
                Outliers handling strategy:    
                <q-select
                  outlined
                  v-model="outliersModel"
                  :options="outliersOptions"
                  label="Outlined"
                />
                <div
                  class="q-pa-md"
                  style="max-width: 300px"
                >
                  <q-input
                    v-if="outliersModel?.includes('Remove')"
                    v-model="deviationsNumber"
                    mask="##"
                    filled
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import { ref } from 'vue'

export default {
    props: {
        column: { type: Object, required: true },
    },
    emits: ['onChange'],
    watch: {
      nullModel(newValue) {
        this.state.nullModel = newValue
        this.$emit('onChange', this.state)
      },
      outliersModel(newValue) {
        this.state.outliersModel = newValue
        this.$emit('onChange', this.state)
      },
      strategyModel(newValue) {
        this.state.strategyModel = newValue
        this.$emit('onChange', this.state)
      },
      nullCustomValue(newValue) {
        this.state.nullCustomValue = this.column.type == "NUMERIC" ? parseInt(newValue) : newValue
        this.$emit('onChange', this.state)
      },
      deviationsNumber(newValue) {
        this.state.deviationsNumber = parseInt(newValue)
        this.$emit('onChange', this.state)
      }
    },
    created () {
    this.nullOptions = this.getNullOptions(this.$props)
    },
    methods: {
      getNullOptions: function(props) {
        // Logic of which cleaning coices are presented to the user
          const baseOptions = [`Ignore`]
          if (props.column.empty_values > 0) { 
            baseOptions.push(`Remove ${props.column.empty_values} row values corresponding to the empty values.`)
            baseOptions.push(`Fill all ${props.column.empty_values} empty values with a custom value.`)
            if (props.column.type == 'NUMERIC') {
              baseOptions.push(`Fill all ${props.column.empty_values} empty values with the column average.`)
          }
          }
          return baseOptions;
      }
    },
    setup (props) {
      return {
        strategyModel: ref('clean'),
        nullModel: ref(null),
        outliersModel: ref(null),
        deviationsNumber: ref(null),
        plotsModel: ref(null),
        nullOptions: [],
        nullCustomValue: ref(null),
        outliersOptions: ['Remove above # deviations', "Ignore"],
        state: {
          "name": props.column.name,
          "type": props.column.type,
          "strategyModel": 'clean',
          "nullModel": '',
          "nullCustomValue": '',
          "outliersModel": '',
          "deviationsNumber": '',
          "plotsModel": ''
        }
      }
    }
};
</script>