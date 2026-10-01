import { createContext, useContext, useEffect, useState } from "react";
import * as SecureStore from "expo-secure-store";
import { api } from "../services/api";
import axios from "axios";

type User = { id: number; name: string; email: string };
type Ctx = { user: User | null; loading: boolean; login: (email: string, password: string) => Promise<void>; logout: () => Promise<void> };
const AuthContext = createContext<Ctx>({ user: null, loading: true, login: async () => { }, logout: async () => { } });
export function AuthProvider({ children }: { children: any }) {
    const [user, setUser] = useState<User | null>(null); const [loading, setLoading] = useState(true);
    useEffect(() => { (async () => { try { const t = await SecureStore.getItemAsync("rennto_token"); if (t) { const r = await api.get("/auth/me"); setUser(r.data) } } catch { } finally { setLoading(false) } })() }, []);
    const login = async (email: string, password: string) => {
        const body = new URLSearchParams({ username: email, password });
        console.log("Logging in with", body.toString())
        console.log("Logging in with health check 2", await axios.get("http://localhost:8000/health"))
        const r = await api.post("/auth/login", body.toString(),
            {
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            }
        );
        console.log("Login response", r.data)
        await SecureStore.setItemAsync("rennto_token", r.data.access_token);
        setUser(r.data.user)
    };
    const logout = async () => { await SecureStore.deleteItemAsync("rennto_token"); setUser(null) };
    return <AuthContext.Provider value={{ user, loading, login, logout }}>{children}</AuthContext.Provider>
}
export const useAuth = () => useContext(AuthContext);
