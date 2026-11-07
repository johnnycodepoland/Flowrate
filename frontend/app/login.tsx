import {View, Text, StyleSheet, Pressable, TextInput, ScrollView, Image} from "react-native";
import {useFonts, Montserrat_700Bold, Montserrat_400Regular } from "@expo-google-fonts/montserrat";
import {Inter_700Bold, Inter_400Regular } from "@expo-google-fonts/inter";
import {router} from "expo-router";
import {useState} from "react"
import {API_URL} from "../config";
import {showError} from "../utils";
import {saveToken} from "../auth"

export default function Login() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const [fontLoaded] = useFonts({
        Montserrat_700Bold,
        Montserrat_400Regular,
        Inter_700Bold,
        Inter_400Regular,
    });

    const handleLogin = async () => {
        if (loading) {
            return;
        }
        setLoading(true)

        try {
            if (email === "" || password === "") {
                showError("Wpisz e-mail i hasło")
                return;
            }

            const res = await fetch(`${API_URL}/auth/login`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({email, password}),
            })

            if (!res.ok) {
                showError("Nieprawidłowy e-mail lub hasło")
                return;
            }

            const data = await res.json()
            await saveToken(data.access_token)
            router.replace("/")
        }
        finally {setLoading(false)}
    };

    if (!fontLoaded) {
        return null;
    }

    return (
        <ScrollView style={styles.container} contentContainerStyle={styles.content}>
            <Image
                source={require("../assets/images/logo.png")}
                style={styles.logo}
                resizeMode="contain"
            />  
            <Text style={styles.loginText}>Zaloguj się</Text>
            <Text style={styles.label}>E-mail</Text>
            <TextInput
                style={styles.input}
                placeholder="np. jankowalski@gmail.com"
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
                autoCorrect={false}
                textContentType="emailAddress"
                placeholderTextColor="#9CA3AF"
            />
            <Text style={styles.label}>Hasło</Text>
            <TextInput
                style={styles.input}
                placeholder="Minimum 8 znaków"
                value={password}
                onChangeText={setPassword}
                secureTextEntry={true}
                textContentType="password"
                placeholderTextColor="#9CA3AF"
            />
            <Pressable style={styles.nextButton} onPress={handleLogin} disabled={loading}>
                <Text style={styles.nextButtonText}>{loading ? "Logowanie..." : "Zaloguj się"}</Text>
            </Pressable>
            <Pressable onPress={() => router.push("/register")}>
                <Text style={styles.switchText}>
                    Nie masz konta? <Text style={styles.switchLink}>Zarejestruj się</Text>
                </Text>
            </Pressable>
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingHorizontal: 20,
        backgroundColor: "#FFFFFF"},
    logo: {
        width: 200,
        height: 38,
        marginBottom: 24,
        alignSelf: "center"},
    content: {
        flexGrow: 1,
        justifyContent: "center",
        gap: 12},
    loginText: {
        fontFamily: "Montserrat_700Bold",
        fontSize: 28,
        color: "#1A1A1A"},
    input: {
        backgroundColor: "#F5F5F7",
        borderRadius: 12,
        paddingVertical: 12,
        paddingHorizontal: 14,
        fontSize: 16,
        fontFamily: "Montserrat_400Regular",
        color: "#1A1A1A"},
    label: {
        color: "#1A1A1A",
        fontSize: 18,
        fontFamily: "Montserrat_700Bold"},
    nextButton: {
        backgroundColor: "#6366F1",
        borderRadius: 16,
        paddingVertical: 14,
        alignItems: "center"},
    nextButtonText: {
        color: "#FFFFFF",
        fontSize: 18,
        fontFamily: "Montserrat_700Bold"},
    switchText: {
        textAlign: "center",
        color: "#6B7280",
        fontSize: 14,
        fontFamily: "Montserrat_400Regular"},
    switchLink: {
        color: "#6366F1",
        fontFamily: "Montserrat_700Bold"}
})