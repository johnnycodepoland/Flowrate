import {ScrollView, StyleSheet, Text, View, Pressable} from "react-native";
import {useState, useEffect, useCallback} from "react";
import {useFonts, Montserrat_700Bold, Montserrat_400Regular } from "@expo-google-fonts/montserrat";
import {Inter_700Bold, Inter_400Regular } from "@expo-google-fonts/inter";
import {Ionicons, MaterialCommunityIcons} from "@expo/vector-icons";
import {useRouter, useFocusEffect} from "expo-router";

export default function AllTrainings() {
    const [fontLoaded] = useFonts({
        Montserrat_700Bold,
        Montserrat_400Regular,
        Inter_700Bold,
        Inter_400Regular,
    });
    const router = useRouter();
    const [trainings, setTrainings] = useState([]);

    useFocusEffect(
        useCallback(() => {
            fetch("http://192.168.68.65:8000/trainings")
                .then(response => response.json())
                .then(data => setTrainings(data));
        }, [])
    );

    if (!fontLoaded) {
        return null;
    }

    return (
        <ScrollView style={styles.container}>
            <View style={styles.allTrainingsSectionHeader}>
                <Pressable onPress={() => router.back()}>
                    <Ionicons name="chevron-back" size={32} color="#1A1A1A" />
                </Pressable>
                <Text style={styles.pageTitle}>Wszystkie treningi</Text>
            </View>
            <View style={styles.activityCard}>
                {trainings.map((training, index) => (
                    <Pressable key={index} style={styles.activityRow} onPress={() => router.push(`/training/${training.id}`)}>
                        <View style={styles.iconBadge}>
                            <MaterialCommunityIcons name="swim" size={28} color="#FFFFFF"/>
                            <Text style={styles.iconBadgeText}>{training.RPE}</Text>
                        </View>
                        <Text style={styles.activityTitle}>Pływanie</Text>
                        <Text style={styles.activityTime}>{training.time} min</Text>
                    </Pressable>
                ))}
            </View>
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingHorizontal: 20,
        paddingTop: 70,
        backgroundColor: "#FFFFFF"},
    pageTitle: {
        fontSize: 32,
        color: "#1A1A1A",
        fontFamily: "Montserrat_700Bold",
        marginBottom: 20},
    activityRow: {
        flexDirection: "row",
        paddingVertical: 8,
        paddingHorizontal: 10,
        borderWidth: 1,
        borderColor: "#1A1A1A",
        borderRadius: 14,
        alignItems: "center"},
    activityTitle: {
        flex: 1,
        marginRight: 8,
        color: "#1A1A1A",
        fontSize: 13,
        letterSpacing: 1,
        textTransform: "uppercase",
        fontFamily: "Inter_700Bold",
        marginLeft: 12},
    iconBadge: {
        width: 88,
        height: 44,
        borderRadius: 12,
        backgroundColor: "#6366F1",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "row",
        gap: 6},
    iconBadgeText: {
        color: "#FFFFFF",
        fontSize: 16,
        fontFamily: "Montserrat_700Bold"},
    activityTime: {
        color: "#1A1A1A",
        fontSize: 13,
        letterSpacing: 1,
        textTransform: "uppercase",
        fontFamily: "Inter_700Bold"},
    activityCard: {
        backgroundColor: "#F5F5F7",
        borderRadius:20,
        padding: 16,
        gap: 8,
        marginTop: 16},
    allTrainingsSectionHeader: {
        flexDirection: "row"}
})