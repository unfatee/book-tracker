import axiosClient from "./axiosClient";

export const goalsApi = {
  getGoals: async () => {
    const response = await axiosClient.get("/goals");
    return response.data;
  },
  getGoal: async (year) => {
    const response = await axiosClient.get(`/goals/${year}`);
    return response.data;
  },
  createOrUpdate: async (payload) => {
    const response = await axiosClient.post("/goals", payload);
    return response.data;
  },
  update: async (year, payload) => {
    const response = await axiosClient.put(`/goals/${year}`, payload);
    return response.data;
  },
  delete: async (year) => axiosClient.delete(`/goals/${year}`),
  progress: async (year) => {
    const response = await axiosClient.get(`/goals/${year}/progress`);
    return response.data;
  },
};
