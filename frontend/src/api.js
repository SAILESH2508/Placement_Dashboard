import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/api/",
});

// ✅ Add token to requests
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ✅ Auto token refresh
API.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;

      const refresh = localStorage.getItem("refresh_token");
      if (!refresh) {
        window.location.href = "/login";
        return;
      }

      try {
        const res = await axios.post("http://127.0.0.1:8000/api/auth/refresh/", {
          refresh,
        });

        localStorage.setItem("access_token", res.data.access);

        original.headers.Authorization = `Bearer ${res.data.access}`;
        return API(original);
      } catch (err) {
        localStorage.clear();
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default API;
