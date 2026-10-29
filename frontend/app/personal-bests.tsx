import {View, Text, StyleSheet, Pressable, TextInput} from "react-native";
import {useFonts, Montserrat_700Bold, Montserrat_400Regular } from "@expo-google-fonts/montserrat";
import {Inter_700Bold, Inter_400Regular } from "@expo-google-fonts/inter";
import {Ionicons} from "@expo/vector-icons";
import {router} from "expo-router";
import {useState, useEffect} from "react"
import {API_URL} from "../config";
import {parseTime, formatTime, showError} from "../utils";

export default function PersonalBests() {
    const [times, setTimes] = useState({50: "", 100: "", 200: "", 400: ""});
    const [fontLoaded] = useFonts({
        Montserrat_700Bold,
        Montserrat_400Regular,
        Inter_700Bold,
        Inter_400Regular,
    });

    const handleSave = async () => {
        for (const distance of [50, 100, 200, 400]) {
            if (times[distance] === "") continue;

            const time = parseTime(times[distance])
            if (!(time > 0)) {
                showError(`Niepoprawny czas na ${distance} m`);
                return;
            }

            const res = await fetch(`${API_URL}/personal-bests`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({distance: distance, time: time}),
            });
            if (!res.ok) {
                showError("Nie udało się zapisać rekordu")
                return;
            }
        }
        goBack()
    };

    const goBack = () => {
        if (router.canGoBack()) {
            router.back()
        }
        else {
            router.replace("/")
        }
    }
    
    useEffect(() => {
        fetch(`${API_URL}/personal-bests`)
            .then(response => response.json())
            .then(data => {
            setTimes({
                50: data[50] ? formatTime(data[50]) : "",
                100: data[100] ? formatTime(data[100]) : "",
                200: data[200] ? formatTime(data[200]) : "",
                400: data[400] ? formatTime(data[400]) : "",
            });
        });
    }, []);

    if (!fontLoaded) {
        return null;
    }

    return (
        <View style={styles.container}>
            <View style={styles.trainingSectionHeader}>
                <Pressable onPress={() => router.back()}>
                    <Ionicons name="chevron-back" size={32} color="#1A1A1A" />
                </Pressable>
                <Text style={styles.pageTittle}>Rekordy życiowe</Text>
            </View>
            <Text style={styles.label}>Czas na 50m stylem dowolnym</Text>
            <TextInput
                style={styles.input}
                placeholder="np. 26,1"
                value={times[50]}
                onChangeText={(text) => setTimes({...times, 50: text})}
                keyboardType="numbers-and-punctuation"
            />
            <Text style={styles.label}>Czas na 100m stylem dowolnym</Text>
            <TextInput
                style={styles.input}
                placeholder="np. 1:01,05"
                value={times[100]}
                onChangeText={(text) => setTimes({...times, 100: text})}
                keyboardType="numbers-and-punctuation"
            />
            <Text style={styles.label}>Czas na 200m stylem dowolnym</Text>
            <TextInput
                style={styles.input}
                placeholder="np. 2:08"
                value={times[200]}
                onChangeText={(text) => setTimes({...times, 200: text})}
                keyboardType="numbers-and-punctuation"
            />
            <Text style={styles.label}>Czas na 400m stylem dowolnym</Text>
            <TextInput
                style={styles.input}
                placeholder="np. 4:40"
                value={times[400]}
                onChangeText={(text) => setTimes({...times, 400: text})}
                keyboardType="numbers-and-punctuation"
            />
            <Pressable style={[styles.nextButton, {marginTop: 12}]} onPress={handleSave}>
                <Text style={styles.nextButtonText}>Zatwierdź</Text>
            </Pressable>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingHorizontal: 20,
        paddingTop: 70,
        backgroundColor: "#FFFFFF"},
    pageTittle: {
        flex: 1,
        marginRight: 8,
        color: "#1A1A1A",
        fontSize: 16,
        letterSpacing: 1,
        textTransform: "uppercase",
        fontFamily: "Inter_700Bold",
        marginLeft: 12},
    label: {
        color: "#1A1A1A",
        fontSize: 18,
        fontFamily: "Montserrat_700Bold",
        marginTop: 20,
        marginBottom: 8},
    input: {
        backgroundColor: "#F5F5F7",
        borderRadius: 12,
        paddingVertical: 12,
        paddingHorizontal: 14,
        fontSize: 16,
        fontFamily: "Montserrat_400Regular",
        color: "#1A1A1A"},
    trainingSectionHeader: {
        alignItems: "center",
        flexDirection: "row"},
    nextButton: {
        backgroundColor: "#6366F1",
        borderRadius: 16,
        paddingVertical: 14,
        alignItems: "center",
        marginTop: 40},
    nextButtonText: {
        color: "#FFFFFF",
        fontSize: 18,
        fontFamily: "Montserrat_700Bold"}
})