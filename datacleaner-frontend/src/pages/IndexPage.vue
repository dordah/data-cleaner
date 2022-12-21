<template>
  <div
    class="row"
  >
    <div class="col-3" />
    <div class="q-pa-md bg-image">
      <q-img
        style="z-index: -1; opacity: 0.7"
        src="https://i0.wp.com/www.estidia.eu/wp-content/uploads/2018/04/Savin-NY-Website-Background-Web.jpg?ssl=1"
        class="fullscreen"
      />
      <div class="q-pa-md">
        <!-- Entering animation -->
        <main>
          <div class="col-2 hero">
            <div class="col col-md-6 text-h4 text-weight-bold">
              <hr>
              <transition
                appear
                @before-enter="beforeEnter"
                @enter="enter"
              >
                <span style="font-family: 'Roboto', serif;">
                  Automatically clean and analyze your datasets.
                </span>
              </transition>
            </div>
            <transition
              appear
              @before-enter="beforeEnter2"
              @enter="enter2"
            >
              <div class="col-6 col-md-6 text-h5 text-weight-thin">
                Upload your dataset in CSV or XLS format and watch as the magic
                happens...
              </div>
            </transition>
            <hr>
          </div>
        </main>
        <!-- End of entering animation -->
        <!-- Stepper - responsible for going through the stages of data cleaning, from uploading the file to receiving the cleaned data.
             <q-stepper> is the main object while <q-step> are individual steps
             Each <q-step> uses a dedicated component for its specific step.   
        -->
        <q-stepper
          v-model="step"
          ref="stepper"
          color="teal-10"
          active-color="primary"
          style="background-color: 'white';"
          animated
          keep-alive
        >
          <q-step
            :name="1"
            title="Upload your CSV file"
            icon="settings"
            :done="step > 1"
          >
            <upload-step @finished="getUploadInitialStats" />
          </q-step>

          <q-step
            :name="2"
            title="Select cleaning strategy"
            icon="create_new_folder"
            :done="step > 2"
          >
            <selection-step
              :data="columnData"
              @column-strategy-change="updateStrategy"
            />
          </q-step>

          <q-step
            :name="3"
            title="Summary"
            icon="assignment"
          >
            <summary-step
              :data="strategyData"
              :filename="fileName"
            />
          </q-step>
          <!-- Stepper navigation -->
          <template #navigation>
            <q-stepper-navigation>
              <q-btn
                @click="step !== 3 ? (fileUploaded? $refs.stepper.next() : alert = true) : $router.go('/')"
                color="primary"
                :label="step === 3 ? 'Finish' : 'Continue'"
              />

              <q-btn
                v-if="step > 1"
                flat
                color="primary"
                @click="$refs.stepper.previous()"
                label="Back"
                class="q-ml-sm"
              />
            </q-stepper-navigation>
          </template>
        </q-stepper>
        <!-- End of stepper -->

        <!-- Quotes on cleanliness -->
        <div class="row row-md-6 text-h6 text-weight-bold">
          <transition
            appear
            @before-enter="beforeEnter"
            @enter="enter"
          >
            <blockquote>
              <p>
                Get out! Get out and leave your captivity,
                <br>
                    where everything you touch is unclean.
                <br>
                Get out of there and purify yourselves,
                <br>
                    you who carry home the sacred objects of the Lord.
              </p>
              <small>Isaiah 52:11</small>
            </blockquote>
          </transition>
          <transition
            appear
            @before-enter="beforeEnter"
            @enter="enter"
          >
            <blockquote>
              <p>No data is clean, but most is useful.</p>
              <small>Dean Abbot</small>
            </blockquote>
          </transition>
        </div>
        <!-- End of quotes on cleanliness -->
        <!-- Alert in case user didn't upload a file-->
        <div>
          <q-dialog v-model="alert">
            <q-card>
              <q-card-section>
                <div class="text-h6">
                  File not uploaded
                </div>
              </q-card-section>

              <q-card-section class="q-pt-none">
                Please upload a file using the "upload" button in the top right corner after adding a file before proceeding.
              </q-card-section>

              <q-card-actions align="right">
                <q-btn
                  flat
                  label="OK"
                  color="primary"
                  v-close-popup
                />
              </q-card-actions>
            </q-card>
          </q-dialog>
        </div>
        <!-- End of alert -->
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import gsap from "gsap"
import UploadStep from "./StepperStages/UploadStep.vue";
import SelectionStep from "./StepperStages/SelectionStep.vue";
import SummaryStep from "./StepperStages/SummaryStep.vue";

export default {
  components: { UploadStep, SelectionStep, SummaryStep },
  setup () {
    // Animation related functions
   const beforeEnter = (el) => {
      console.log('before enter - set initial state')
      el.style.transform = 'translateY(-60px)'
      el.style.opacity = 0
    }

    const enter = (el) => {
      console.log('starting to enter - make transition')
      gsap.to(el, {
        duration: 1,
        y: 0,
        opacity: 1,
      })
    }
    const beforeEnter2 = (el) => {
      console.log('before enter - set initial state')
      el.style.transform = 'translateX(-100%)'
      el.style.opacity = 0
    }

    const enter2 = (el) => {
      console.log('starting to enter - make transition')
      gsap.to(el, {
        ease: "easeInEaseOut",
        duration: 2,
        x: 0,
        opacity: 1,
      })
    }
  // End of animation related functions
    return {
      // Component data
      step: ref(1),
      columnData: null,
      strategyData: null,
      fileName: null,
      fileUploaded: false,
      alert: ref(false),
      beforeEnter,enter,beforeEnter2,enter2
    };
  },
  methods: {
    // getUploadInitialStats updates the main component with the uploaded file after the user uploaded the file.
    getUploadInitialStats (data) {
      this.columnData = data;
      this.fileName = data.fileName;
      this.fileUploaded = true;
    },
    // updateStrategy updates the main component with the strategy the user chooses in step 2
    updateStrategy (data) {
      this.strategyData = data;
    }
  },
};
</script>

