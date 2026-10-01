import axios from "axios";
import * as SecureStore from "expo-secure-store";
console.log(
  "API URL",
  process.env.EXPO_PUBLIC_API_URL || "http://localhost:8000/api/v1",
);
export const api = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL || "http://localhost:8000/api/v1",
  // timeout: 15000,
});

api.interceptors.request.use(async config => {
  const token = await SecureStore.getItemAsync("rennto_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
