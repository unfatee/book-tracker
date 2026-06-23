import axiosClient from "./axiosClient";

export const authApi = {
  register: async (payload) => {
    const response = await axiosClient.post("/auth/register", payload);
    return response.data;
  },
  login: async (payload) => {
    const response = await axiosClient.post("/auth/login", payload);
    return response.data;
  },
  me: async () => {
    const response = await axiosClient.get("/auth/me");
    return response.data;
  },
};
