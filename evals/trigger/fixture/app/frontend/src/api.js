import axios from "axios";
export const api = axios.create({ baseURL: "/api" });
api.interceptors.request.use((c) => { c.headers.Authorization = `Bearer ${localStorage.token}`; return c; });
