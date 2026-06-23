import axiosClient from "./axiosClient";

export const exportApi = {
  booksCsv: async () => {
    const response = await axiosClient.get("/books/export/csv", { responseType: "blob" });
    return response.data;
  },
};
