<template>
  <q-page
    class="q-pa-md items-start q-gutter-md"
    style="background: rgb(16 16 19); color white"
  >
    <div style="color: #746e6e" v-if="!this.$store.state.showcase.folder">
      <q-page class="flex flex-center">
        <q-icon name="fas fa-file-alt" size="400px" />
      </q-page>
    </div>

    <div style="color: white">
      <div v-for="name in this.$store.state.showcase.folder" v-bind:key="name">
        <q-card :style="get_new_file(get_time(name))">
          <q-card-section style="color: #03a9f4">
            {{ get_format(get_time(name)) }}
            <div class="column items-end">
              <q-icon
                name="fas fa-trash-alt"
                size="30px"
                style="color: #6d7275"
                @click="delete_file(name)"
              />
            </div>
          </q-card-section>

          <q-card-section>
            <div
              class="row"
              v-for="n_file in Object.values(name)[0]"
              v-bind:key="n_file"
            >
              {{ n_file }}
            </div>
          </q-card-section>

          <q-card-action class="column items-end">
            <div style="margin: 10px" class="row">
              <q-btn
                style="background: green; margin-right: 10px"
                label="open"
                @click="(open = true), (files = name), (read = false)"
              />
            </div>
          </q-card-action>
          <q-dialog full-width v-model="open">
            <q-card>
              <q-card-section
                class="scroll"
                style="height: 500px; background: #181b1f; color: white"
              >
                <div
                  v-for="name_f in Object.values(files)[0]"
                  v-bind:key="name_f"
                >
                  <h6
                    class="row"
                    style="margin: 1px; color: #03a9f4"
                    @click="download(Object.keys(files)[0], name_f)"
                  >
                    <div style="color: #4caf50">»</div>
                    <div style="margin-left: 10px; color: #c4c4c4">
                      <div v-if="Object.values(files)[0].length === 1">
                        {{ read_txt(files, name_f) }}
                      </div>
                      <div v-else>{{ (get_txt = "") }}</div>
                      {{ name_f }}
                    </div>
                  </h6>
                  <br />

                  <div
                    v-if="get_txt"
                    style="color: #00bcd4"
                    @click="read = true"
                  >
                    read . . .
                  </div>

                  <div v-if="read">
                    <div
                      style="color: green"
                      v-for="line in get_txt"
                      v-bind:key="line"
                    >
                      {{ line }}
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </q-dialog>
        </q-card>
        <br />
      </div>

      <q-page-sticky :offset="fabPos">
        <div
          direction="up"
          :disable="draggingFab"
          v-touch-pan.prevent.mouse="moveFab"
        >
          <q-btn
            round
            icon="upload"
            id="add_btn"
            @click="addPopup = true"
            style="
              position: absolute;
              bottom: 50px;
              right: 10px;
              background: #3f51b5 !important;
            "
          />
        </div>
      </q-page-sticky>

      <q-page-sticky :offset="fabPos">
        <div
          direction="up"
          :disable="draggingFab"
          v-touch-pan.prevent.mouse="moveFab"
        >
          <q-btn
            round
            icon="edit"
            id="add_btn"
            @click="addText = true"
            style="
              position: absolute;
              bottom: 100px;
              right: 10px;
              background: #3f51b5 !important;
            "
          />
        </div>
      </q-page-sticky>

      <q-dialog v-model="addText">
        <q-card style="width: 100%">
          <q-card-section style="background: rgb(16, 16, 19)">
            <q-editor
              v-model="text"
              class="q_edit_bg_color"
              style="background-color: #292828fa; color: white"
              :definitions="{}"
              :toolbar="[['bold', 'italic', 'strike', 'underline']]"
            />
            <br />
            <q-btn
              :disable="text ? false : true"
              style="width: 100%; background: #115488; color: white"
              @click="uploadText(text)"
            >
              <div v-if="this.$store.state.showcase.status_upload">
                <q-spinner-ios color="white" size="1em" />
              </div>
              <div v-else>add text</div>
            </q-btn>
          </q-card-section>
        </q-card>
      </q-dialog>

      <q-dialog v-model="addPopup">
        <q-card>
          <q-card-section style="background: rgb(16, 16, 19); color: white">
            <div class="q-pa-md">
              <q-uploader
                style="width: 200px"
                url=""
                @added="file_selected"
                multiple
                dark
                class="color_head_upload"
              >
                <template v-slot:list="scope">
                  <q-list separator dark>
                    <q-item v-for="file in scope.files" :key="file.__key">
                      <q-item-section>
                        <q-item-label class="full-width ellipsis">
                          {{ file.name }}
                        </q-item-label>

                        <q-item-label caption>
                          Status: {{ file.__status }}
                        </q-item-label>

                        <q-item-label caption>
                          {{ file.__sizeLabel }} / {{ file.__progressLabel }}
                        </q-item-label>
                      </q-item-section>

                      <q-item-section v-if="file.__img" thumbnail class="gt-xs">
                        <img :src="file.__img.src" />
                      </q-item-section>

                      <q-item-section top side>
                        <q-btn
                          class="gt-xs"
                          size="12px"
                          flat
                          dense
                          round
                          icon="delete"
                          @click="scope.removeFile(file)"
                        />
                      </q-item-section>
                    </q-item>
                  </q-list>
                </template>
              </q-uploader>
              <br />

              <q-btn
                style="width: 100%; background: #115488"
                @click="uploadFile()"
              >
                <div v-if="this.$store.state.showcase.status_upload">
                  <q-spinner-ios color="white" size="1em" />
                </div>
                <div v-else>Upload</div>
              </q-btn>
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script>
import { ref } from "vue";
import moment from "moment";
import { api } from "boot/axios";
import { Notify } from "quasar";

export default {
  setup() {
    var open = ref(false);
    var files = ref(null);

    var fabPos = ref([18, 18]);
    var draggingFab = ref(false);
    var addPopup = ref(false);

    var addText = ref(false);
    var text = ref(null);

    var get_txt = "";

    var read = ref(false);
    return {
      read,

      get_txt,

      addText,
      text,
      f: [],
      selected_file: null,
      check_if_document_upload: false,
      addPopup,
      open,
      files,
      fabPos,
      draggingFab,
      moveFab(ev) {
        draggingFab.value = ev.isFirst !== true && ev.isFinal !== true;
        fabPos.value = [
          fabPos.value[0] - ev.delta.x,
          fabPos.value[1] - ev.delta.y,
        ];
      },
    };
  },
  methods: {
    read_txt(folder, file) {
      // console.log(file);
      var param = {
        folder: Object.keys(folder)[0],
        name: file,
      };
      api.post("/read_txt", param).then((response) => {
        console.log(response.data);
        this.get_txt = response.data;
      });
    },
    uploadText(texts) {
      console.log(texts);
      this.$store.commit("showcase/STATUS_UPLOAD", { status_upload: true });
      api.post("/upload-text", { text: texts }).then((response) => {
        if (response.data.Result) {
          this.$store.commit("showcase/STATUS_UPLOAD", {
            status_upload: false,
          });
          Notify.create({
            type: "positive",
            color: "positive",
            timeout: 1000,
            message: "send file",
          });
          this.$store.dispatch("showcase/get_all_folder");
        }
      });
      this.text = null;
    },

    delete_file(file) {
      console.log("delete: ", Object.keys(file));
      this.$store.dispatch("showcase/delete_folder", Object.keys(file));
      this.$store.dispatch("showcase/folder_size");
      this.$store.dispatch("showcase/get_all_folder");
    },
    file_selected(file) {
      this.f.push(file[0]);
      this.selected_file = file[0];
      this.check_if_document_upload = true;
    },

    uploadFile() {
      console.log(this.f);
      var types = [];
      var name;
      var type;
      if (this.selected_file) {
        this.$store.commit("showcase/STATUS_UPLOAD", { status_upload: true });
        let fd = new FormData();
        for (var i = 0; i < this.f.length; i++) {
          console.log(this.f[i].type);
          name = this.f[i].name;
          type = this.f[i].type;
          types.push({ type: type, name: name });
          fd.append("files", this.f[i]);
        }
        console.log(types);
        api
          .post("/upload-files", fd, {
            headers: { "Content-Type": "multipart/form-data" },
          })
          .then(
            function (response) {
              if (response.data.Result) {
                console.log(response.data);
                Notify.create({
                  type: "positive",
                  color: "positive",
                  timeout: 1000,
                  message: "send file",
                });
                this.$store.dispatch("showcase/folder_size");
                this.$store.dispatch("showcase/get_all_folder");
                this.$store.commit("showcase/STATUS_UPLOAD", {
                  status_upload: false,
                });
              }
            }.bind(this)
          )
          .catch((error) => {
            console.log(error.response);
          });
      } else {
        Notify.create({
          type: "negative",
          color: "negative",
          timeout: 1000,
          message: "selected file!",
        });
      }
      this.f = [];
    },

    download(folder, file) {
      console.log(folder, file);
      var param = {
        folder: folder,
        name: file,
      };
      this.$store.dispatch("showcase/download", param);
    },

    get_format(date) {
      date = moment(date);
      return date.fromNow();
    },

    get_new_file(date) {
      moment.locale("ru");
      var d = moment(date);
      var m_border = "border: 1px solid #ff5722;";
      var s_border = "border: 1px solid #87e887";
      var style = "background: rgb(24, 27, 31);color: white;";
      if (d.fromNow().includes("минут")) style = style + m_border;
      if (d.fromNow().includes("секунд")) style = style + s_border;
      return style;
    },

    get_time(name) {
      name = Object.keys(name);
      name = name[0];
      var date = name.split(/_\s*/);
      date =
        date[0][0] +
        date[0][1] +
        "." +
        date[0][2] +
        date[0][3] +
        "." +
        date[0][4] +
        date[0][5] +
        date[0][6] +
        date[0][7] +
        " " +
        date[1][0] +
        date[1][1] +
        ":" +
        date[1][2] +
        date[1][3] +
        ":" +
        date[1][4] +
        date[1][5];

      return date;
    },
  },

  mounted() {
    this.$store.dispatch("showcase/get_all_folder");
  },
};
</script>
<style lang="sass">
.color_head_upload
  .q-uploader__header
    background-color: #0e0e0e

.q_edit_bg_color
  .q-editor
    background-color: #292828fa
</style>
