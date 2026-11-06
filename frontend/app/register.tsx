import {View, Text, StyleSheet, Pressable, TextInput, ScrollView, Image} from "react-native";
import {useFonts, Montserrat_700Bold, Montserrat_400Regular } from "@expo-google-fonts/montserrat";
import {Inter_700Bold, Inter_400Regular } from "@expo-google-fonts/inter";
import {router} from "expo-router";
import {useState} from "react"
import {API_URL} from "../config";
import {showError} from "../utils";
import {saveToken} from "../auth"

export default function Register() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [fontLoaded] = useFonts({
        Montserrat_700Bold,
        Montserrat_400Regular,
        Inter_700Bold,
        Inter_400Regular,
    });

    const handleRegister = async () => {
        if (email === "" || password === "") {
            showError("Wpisz e-mail i hasło")
            return;
        }

        if (password.length < 8) {
            showError("Hasło musi mieć minimum 8 znaków")
            return;
        }

    const res = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password}),
    })

    if (res.status === 409) {
        showError("Konto z tym adresem e-mail już istnieje");
        return;
    }

    if (!res.ok) {
        showError("Nie udało się utworzyć konta");
        return;
    }

    const res2 = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password}),
    })

    if (!res2.ok) {
        showError("Konto utworzone, zaloguj się")
        router.replace("/login")
        return;
    }

    const data = await res2.json()
    await saveToken(data.access_token)
    router.replace("/")
    };

    if (!fontLoaded) {
        return null;
    }

    return (
        <ScrollView style={styles.container} contentContainerStyle={styles.content}>
            <Image
                source={require("../assets/images/high-resolution-color-logo(1).png")}
                style={styles.logo}
            />
            <Text style={styles.loginText}>Załóż konto</Text>
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
            />
            <Text style={styles.label}>Hasło</Text>
            <TextInput
                style={styles.input}
                placeholder="Minimum 8 znaków"
                value={password}
                onChangeText={setPassword}
                secureTextEntry={true}
                textContentType="password"
            />
            <Pressable style={styles.nextButton} onPress={handleRegister}>
                <Text style={styles.nextButtonText}>Zarejestruj się</Text>
            </Pressable>
            <Pressable onPress={() => router.back()}>
                <Text style={styles.switchText}>
                    Masz już konto? <Text style={styles.switchLink}>Zaloguj się</Text>
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
        width: "100%",
        height: 50,
        resizeMode: "contain",
        marginTop: 15,
        marginBottom: 0,
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