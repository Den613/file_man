import { boot } from "quasar/wrappers";
import axios from "axios";

const hostname = document.location.hostname;
console.log("hostname: ", hostname);

let baseURL;
if (process.env.DEV) {
  baseURL = "http://" + hostname + ":8001";
} else {
  baseURL = document.location.origin + "/api";
}

const api = axios.create({ baseURL });

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios;
  app.config.globalProperties.$api = api;
});

export { api };
