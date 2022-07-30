import request from "@/utils/request";

export function login(data) {
  return request({
    url: "/api/user/auth",
    method: "post",
    data,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    transformRequest: [
      (data) => {
        let ret = "";
        for (let it in data) {
          ret +=
            encodeURIComponent(it) + "=" + encodeURIComponent(data[it]) + "&";
        }
        return ret;
      },
    ],
  });
}

export function getInfo() {
  return request({
    url: "/api/user/info",
    method: "get",
  });
}

export function updateInfo(data) {
  return request({
    url: "/api/user/info/update",
    method: "post",
    data,
  });
}

export function logout() {
  return request({
    url: "/api/user/logout",
    method: "post",
  });
}
