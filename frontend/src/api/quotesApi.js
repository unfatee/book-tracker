import axiosClient from "./axiosClient";

export const quotesApi = {
  getBookQuotes: async (bookId) => {
    const response = await axiosClient.get(`/books/${bookId}/quotes`);
    return response.data;
  },
  createQuote: async (bookId, payload) => {
    const response = await axiosClient.post(`/books/${bookId}/quotes`, payload);
    return response.data;
  },
  updateQuote: async (bookId, quoteId, payload) => {
    const response = await axiosClient.put(`/books/${bookId}/quotes/${quoteId}`, payload);
    return response.data;
  },
  deleteQuote: async (bookId, quoteId) => axiosClient.delete(`/books/${bookId}/quotes/${quoteId}`),
  getQuotes: async (params = {}) => {
    const response = await axiosClient.get("/quotes", { params });
    return response.data;
  },
};
