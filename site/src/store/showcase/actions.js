import { api } from "boot/axios";

export function get_all_folder({ commit }) {
  api.get("/get_all_folder").then((response) => {
    commit("FOLDER", { folder: response.data });
  });
}

export function get_name_file({ commit }, param) {
  api
    .get("/get_file_names", { params: { name_file: param } })
    .then((response) => {
      commit("NAMES", { name_file: response.data });
    });
}

export function download({}, param) {
  const header = {
    accept: "application/json",
    "Content-Type": "application/json",
  };
  api
    .post(
      "/download-files",
      param,
      { responseType: "arraybuffer" },
      { headers: header }
    )
    .then((response) => {
      var url = window.URL.createObjectURL(
        new Blob([response.data], { type: "application/zip" })
      );
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", param.name);
      document.body.appendChild(link);
      link.click();
    });
}

export function delete_folder({}, param) {
  const params = {
    name_folder: param[0],
  };
  api.get("/delete_file", { params: params }).then((response) => {
    console.log("ok");
  });
}
