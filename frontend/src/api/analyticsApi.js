import axiosClient from "./axiosClient";

export const analyticsApi = {
  summary: async () => {
    const response = await axiosClient.get("/analytics/summary");
    return response.data;
  },
  byGenre: async () => {
    const response = await axiosClient.get("/analytics/by-genre");
    return response.data;
  },
  monthlyReading: async (year) => {
    const response = await axiosClient.get("/analytics/monthly-reading", { params: { year } });
    return response.data;
  },
  topAuthors: async () => {
    const response = await axiosClient.get("/analytics/top-authors");
    return response.data;
  },
  recentActivity: async () => {
    const response = await axiosClient.get("/analytics/recent-activity");
    return response.data;
  },
};
