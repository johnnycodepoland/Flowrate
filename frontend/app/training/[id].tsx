import {Pressable, StyleSheet, ScrollView, Text, View} from "react-native";
import {useLocalSearchParams} from "expo-router";
import {Ionicons, MaterialCommunityIcons} from "@expo/vector-icons";
import {useFonts, Montserrat_700Bold, Montserrat_400Regular } from "@expo-google-fonts/montserrat";
import {Inter_700Bold, Inter_400Regular } from "@expo-google-fonts/inter";
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

export default function TrainingDetails() {
    const {id} = useLocalSearchParams();
    const router = useRouter();
    const training = trainings[Number(id)];
    const [fontLoaded] = useFonts({
        Montserrat_700Bold,
        Montserrat_400Regular,
        Inter_700Bold,
        Inter_400Regular,
    });

    if (!fontLoaded) {
        return null;
    }

    return (
        <ScrollView style={styles.container}>
             <View style={styles.trainingSectionHeader}>
             <Pressable onPress={() => router.back()}>
                <Ionicons name="chevron-back" size={32} color="#1A1A1A" />
             </Pressable>
             <View style={styles.swimmingAndDateSection}>
                <Text style={styles.pageTittle}>Pływanie</Text>
                <Text style={styles.pageSubtitle}>{training.date}</Text>
             </View>
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
    pageTittle: {
        flex: 1,
        marginRight: 8,
        color: "#1A1A1A",
        fontSize: 16,
        letterSpacing: 1,
        textTransform: "uppercase",
        fontFamily: "Inter_700Bold",
        marginLeft: 12},
    trainingSectionHeader: {
        alignItems: "center",
        flexDirection: "row"},
    swimmingAndDateSection: {
        alignItems: "center",
        flexDirection: "column"},
    pageSubtitle: {
        color: "#1A1A1A",
        fontSize: 14,
        fontFamily: "Montserrat_400Regular"}
})