/**
 * Axios instance — JWT refresh interceptor.
 * Vite proxy se `/api` backend par jata hai.
 */
import axios from "axios";
import { useAuthStore } from "../store/authStore";

const apiBase = import.meta.env.VITE_API_BASE_URL || "/api/v1";

const api = axios.create({
  baseURL: apiBase,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().access;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

let refreshing = null;

api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = useAuthStore.getState().refresh;
      if (!refresh) throw error;
      try {
        if (!refreshing) {
          const refreshUrl =
            (import.meta.env.VITE_API_BASE_URL || "/api/v1").replace(/\/api\/v1\/?$/, "") +
            "/api/v1/auth/token/refresh/";
          refreshing = axios
            .post(refreshUrl, { refresh }, { withCredentials: true })
            .then((res) => {
              useAuthStore.getState().setTokens(res.data.access, refresh);
              refreshing = null;
              return res.data.access;
            })
            .catch((e) => {
              refreshing = null;
              useAuthStore.getState().logout();
              throw e;
            });
        }
        const newAccess = await refreshing;
        original.headers.Authorization = `Bearer ${newAccess}`;
        return api(original);
      } catch {
        /* logged out */
      }
    }
    throw error;
  },
);

export default api;
