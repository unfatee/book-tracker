import axiosClient from "./axiosClient";

export const booksApi = {
  getBooks: async (params = {}) => {
    const response = await axiosClient.get("/books", { params });
    return response.data;
  },
  getBook: async (id) => {
    const response = await axiosClient.get(`/books/${id}`);
    return response.data;
  },
  createBook: async (payload) => {
    const response = await axiosClient.post("/books", payload);
    return response.data;
  },
  updateBook: async (id, payload) => {
    const response = await axiosClient.put(`/books/${id}`, payload);
    return response.data;
  },
  deleteBook: async (id) => axiosClient.delete(`/books/${id}`),
  updateProgress: async (id, currentPage) => {
    const response = await axiosClient.patch(`/books/${id}/progress`, { current_page: currentPage });
    return response.data;
  },
  toggleFavorite: async (id) => {
    const response = await axiosClient.patch(`/books/${id}/favorite`);
    return response.data;
  },
  updateStatus: async (id, status) => {
    const response = await axiosClient.patch(`/books/${id}/status`, { status });
    return response.data;
  },
  createDemoData: async () => {
    const response = await axiosClient.post("/books/demo-data");
    return response.data;
  },
};
