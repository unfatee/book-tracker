import axios from "axios";

const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
});

axiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("book_tracker_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("book_tracker_token");
      window.dispatchEvent(new Event("book-tracker:logout"));
    }
    return Promise.reject(error);
  }
);

export function getApiError(error, fallback = "Something went wrong") {
  return error.response?.data?.detail || error.message || fallback;
}

export default axiosClient;
