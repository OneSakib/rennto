import { useState } from "react";
import { View, Text, TextInput, Pressable, StyleSheet, Alert } from "react-native";
import { router } from "expo-router";
import { useAuth } from "../src/context/AuthContext";

export default function Login() {
  const {login} = useAuth();
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");
  const submit=async()=>{try{await login(email,password);router.replace("/(tabs)");}catch(e:any){Alert.alert("Login failed",e?.response?.data?.detail||"Unable to login");}};
  return <View style={s.container}>
    <Text style={s.logo}>Rennto</Text><Text style={s.subtitle}>Rent management, made simple.</Text>
    <TextInput style={s.input} placeholder="Email" autoCapitalize="none" value={email} onChangeText={setEmail}/>
    <TextInput style={s.input} placeholder="Password" secureTextEntry value={password} onChangeText={setPassword}/>
    <Pressable style={s.button} onPress={submit}><Text style={s.buttonText}>Login</Text></Pressable>
    <Pressable onPress={()=>router.push("/register")}><Text style={s.link}>Create an account</Text></Pressable>
  </View>
}
const s=StyleSheet.create({container:{flex:1,justifyContent:"center",padding:24,backgroundColor:"#F7F9FC"},logo:{fontSize:42,fontWeight:"800",color:"#172033"},subtitle:{fontSize:16,color:"#6B7280",marginBottom:32},input:{backgroundColor:"#fff",borderWidth:1,borderColor:"#E5E7EB",borderRadius:14,padding:15,marginBottom:14,fontSize:16},button:{backgroundColor:"#172033",padding:16,borderRadius:14,alignItems:"center",marginTop:8},buttonText:{color:"#fff",fontWeight:"700",fontSize:16},link:{textAlign:"center",marginTop:20,color:"#2563EB",fontWeight:"600"}});
