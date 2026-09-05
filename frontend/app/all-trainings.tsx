import {ScrollView, StyleSheet, Text, View, Pressable} from "react-native";
import {useFonts, Montserrat_700Bold, Montserrat_400Regular } from "@expo-google-fonts/montserrat";
import {Inter_700Bold, Inter_400Regular } from "@expo-google-fonts/inter";
import {Ionicons, MaterialCommunityIcons} from "@expo/vector-icons";
import {useRouter} from "expo-router";

const trainings = [
    {date: "10 sierpnia", distance: 2800, time: 90, RPE: 4.5},
    {date: "9 sierpnia", distance: 4200, time: 90, RPE: 9.3},
    {date: "11 sierpnia", distance: 2200, time: 90, RPE: 5.2},
    {date: "12 sierpnia", distance: 1850, time: 90, RPE: 9.8},
    {date: "15 sierpnia", distance: 1150, time: 90, RPE: 1.8},
    {date: "20 sierpnia", distance: 3500, time: 60, RPE: 6.8},
    {date: "1 września", distance: 2500, time: 90, RPE: 3.8},
    ];
    const router = useRouter();

export default function AllTrainings() {
    return (
        <ScrollView style={styles.container}>
            <Text style={styles.pageTitle}>Wszystkie treningi</Text>
            <View style={styles.activityCard}>
                {trainings.map((training, index) => (
                    <Pressable key={index} style={styles.activityRow} onPress={() => router.push(`/training/${index}`)}>
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
        marginTop: 16}
})