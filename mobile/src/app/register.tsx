import { useState } from "react";
import { View, Text, TextInput, Pressable, StyleSheet, Alert } from "react-native";
import { router } from "expo-router";
import { api } from "../services/api";
export default function Register() {
    const [name, setName] = useState(""); const [email, setEmail] = useState(""); const [password, setPassword] = useState("");
    const submit = async () => { try { await api.post("/auth/register", { name, email, password }); Alert.alert("Account created", "Please login."); router.replace("/login"); } catch (e: any) { Alert.alert("Error", e?.response?.data?.detail || "Unable to register"); } };
    return <View style={s.c}><Text style={s.t}>Create Rennto account</Text><TextInput style={s.i} placeholder="Name" value={name} onChangeText={setName} /><TextInput style={s.i} placeholder="Email" autoCapitalize="none" value={email} onChangeText={setEmail} /><TextInput style={s.i} placeholder="Password (6+ chars)" secureTextEntry value={password} onChangeText={setPassword} /><Pressable style={s.b} onPress={submit}><Text style={s.bt}>Create account</Text></Pressable><Pressable onPress={() => router.back()}><Text style={s.l}>Back to login</Text></Pressable></View>
}
const s = StyleSheet.create({ c: { flex: 1, justifyContent: "center", padding: 24, backgroundColor: "#F7F9FC" }, t: { fontSize: 28, fontWeight: "800", marginBottom: 24 }, i: { backgroundColor: "#fff", borderWidth: 1, borderColor: "#E5E7EB", borderRadius: 14, padding: 15, marginBottom: 14 }, b: { backgroundColor: "#172033", padding: 16, borderRadius: 14, alignItems: "center" }, bt: { color: "#fff", fontWeight: "700" }, l: { textAlign: "center", marginTop: 20, color: "#2563EB" } });
