<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar style="background: rgb(24, 27, 31)">
        <q-toolbar-title>
          {{ this.$store.state.showcase.folder_size }}
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  setup() {
    return {};
  },

  mounted() {
    this.$store.dispatch("showcase/folder_size");
  },
});
</script>
