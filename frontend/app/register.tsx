import {View, Text, StyleSheet, Pressable, TextInput, ScrollView, Image} from "react-native";
import {useFonts, Montserrat_700Bold, Montserrat_400Regular } from "@expo-google-fonts/montserrat";
import {Inter_700Bold, Inter_400Regular } from "@expo-google-fonts/inter";
import {router} from "expo-router";
import {useState} from "react"
import {API_URL} from "../config";
import {showError} from "../utils";
import {saveToken} from "../auth"
import {MaterialCommunityIcons} from "@expo/vector-icons";
import {fetchWithTimeout} from "@/api";

export default function Register() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const [showPassword, setShowPassword] = useState(false)
    const [fontLoaded] = useFonts({
        Montserrat_700Bold,
        Montserrat_400Regular,
        Inter_700Bold,
        Inter_400Regular,
    });

    const handleRegister = async () => {
        if (loading) {
            return;
        }
        setLoading(true)
        
        try {
            if (email === "" || password === "") {
                showError("Wpisz e-mail i hasło")
                return;
            }

            if (password.length < 8) {
                showError("Hasło musi mieć minimum 8 znaków")
                return;
            }

            const res = await fetchWithTimeout(`${API_URL}/auth/register`, {
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

            const res2 = await fetchWithTimeout(`${API_URL}/auth/login`, {
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
        }
        catch {
            showError("Brak połączenia z serwerem")
            return;
        }
        finally { setLoading(false) }
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
                placeholderTextColor="#9CA3AF"
            />
            <Text style={styles.label}>Hasło</Text>
            <View style={styles.passwordContainer}>
                <TextInput
                    style={[styles.input, {flex: 1}]}
                    placeholder="Minimum 8 znaków"
                    value={password}
                    onChangeText={setPassword}
                    secureTextEntry={!showPassword}
                    textContentType="password"
                    placeholderTextColor="#9CA3AF"
                    autoCapitalize="none"
                    autoCorrect={false}
                />
                <Pressable onPress={() => setShowPassword(!showPassword)}>
                    <MaterialCommunityIcons name={showPassword ? "eye-off" : "eye"} size={22} color="#9CA3AF" />
                </Pressable>
            </View>
            <Pressable style={styles.nextButton} onPress={handleRegister} disabled={loading}>
                <Text style={styles.nextButtonText}>{loading ? "Tworzenie konta..." : "Zarejestruj się"}</Text>
            </Pressable>
            <Pressable onPress={() => router.canGoBack() ? router.back() : router.replace("/login")}>
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
        fontFamily: "Montserrat_700Bold"},
    passwordContainer: {
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: "#F5F5F7",
        borderRadius: 12,
        paddingRight: 14}
})