import {ScrollView, Text, View, StyleSheet, Image, Pressable} from "react-native";
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

export default function Index() {

    const [fontLoaded] = useFonts({
        Montserrat_700Bold,
        Montserrat_400Regular,
        Inter_700Bold,
        Inter_400Regular,
    });
    const router = useRouter();

    if (!fontLoaded) {
        return null;
    }

    return (
    <ScrollView style={styles.container}>
        <Image
            source={require("../assets/images/high-resolution-color-logo(1).png")}
            style={styles.logo}
        />
        <View style={styles.topRow}>
            <View style={styles.percentageCircleContainer}>
                <View style={styles.percentageCircle}>
                    <Text style={styles.percentageText}>84%</Text>
                    <Text style={styles.fatigueText}>Obciążenie</Text>
                </View>
            </View>
            <View style={styles.dateBox}>
                <Text style={styles.dateText}>10 sierpnia</Text>
                <View style={{flexDirection: "row", alignItems: "center", gap: 4}}>
                    <Ionicons name="sunny" size={16} color="#1A1A1A" />
                    <Text style={styles.weatherText}>26°C</Text>
                </View>
            </View>
        </View>
        <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Ostatnie treningi</Text>
            <Pressable style={styles.plusButton}>
                <Text style={styles.plusButtonText}>+</Text>
            </Pressable>
        </View>
        <View style={styles.activityCard}>
            {trainings.slice(0, 6).map((training, index) => (
                <View key={index} style={styles.activityRow}>
                     <View style={styles.iconBadge}>
                        <MaterialCommunityIcons name="swim" size={28} color="#FFFFFF"/>
                        <Text style={styles.iconBadgeText}>{training.RPE}</Text>
                    </View>
                    <Text style={styles.activityTitle}>Pływanie</Text>
                    <Text style={styles.activityTime}>{training.time} min</Text>
                </View>
            ))}
        </View>
        <Pressable onPress={() => router.push("/all-trainings")}>
            <Text style={styles.seeAllText}> Zobacz wszystkie →</Text>
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
        width: 672,
        height: 144,
        resizeMode: "contain",
        marginTop: 15,
        marginBottom: -100,
        alignSelf: "center"},
    percentageCircleContainer: {
        width: "50%",
        justifyContent: "center",
        alignItems: "center",
        height: 300},
    percentageCircle: {
        width: 140,
        height: 140,
        borderRadius: 70,
        borderWidth: 8.5,
        borderColor: "#6366F1",
        justifyContent: "center",
        marginTop: 0,
        alignItems: "center"},
    percentageText: {
        color: "#1A1A1A",
        fontSize: 45,
        fontFamily: "Montserrat_700Bold"},
    topRow: {
        flexDirection: "row",
        justifyContent: "flex-start"},
    dateText: {
        color: "#1A1A1A",
        fontSize: 30,
        fontFamily: "Montserrat_700Bold"},
    weatherText: {
        color: "#1A1A1A",
        fontSize: 19,
        fontFamily: "Montserrat_400Regular"},
    fatigueText: {
        color: "#1A1A1A",
        fontSize: 11.5,
        letterSpacing: 1,
        textTransform: "uppercase",
        fontFamily: "Inter_700Bold"},
    sectionHeader: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        marginTop: -50},
    sectionTitle: {
        fontSize: 22,
        color: "#1A1A1A",
        fontFamily: "Montserrat_700Bold"},
    plusButton: {
        width: 44,
        height: 44,
        borderRadius: 22,
        backgroundColor: "#1A1A1A",
        justifyContent: "center",
        alignItems: "center"},
    plusButtonText: {
        color: "#FFFFFF",
        fontSize: 24,
        fontFamily: "Montserrat_700Bold"},
    dateBox: {
        justifyContent: "center",
        alignItems: "center",
        width: 170},
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
    seeAllText: {
        color: "#6366F1",
        fontSize: 14,
        textAlign: "right",
        marginTop: 10,
        fontFamily: "Montserrat_700Bold"},
    activityCard: {
        backgroundColor: "#F5F5F7",
        borderRadius:20,
        padding: 16,
        gap: 8,
        marginTop: 16}
})