import {Pressable, StyleSheet, ScrollView, Text, View} from "react-native";
import {useState, useEffect} from "react"
import {useLocalSearchParams} from "expo-router";
import {Ionicons, MaterialCommunityIcons} from "@expo/vector-icons";
import {useFonts, Montserrat_700Bold, Montserrat_400Regular } from "@expo-google-fonts/montserrat";
import {Inter_700Bold, Inter_400Regular } from "@expo-google-fonts/inter";
import {useRouter} from "expo-router";

export default function TrainingDetails() {
    const {id} = useLocalSearchParams();
    const router = useRouter();
    const [training, setTraining] = useState(null);

    useEffect (() => {
        fetch(`http://192.168.68.64:8000/trainings/${id}`)
            .then(response => response.json())
            .then(data => setTraining(data));
    }, []);

    const [fontLoaded] = useFonts({
        Montserrat_700Bold,
        Montserrat_400Regular,
        Inter_700Bold,
        Inter_400Regular,
    });

    if (!fontLoaded) {
        return null;
    }

    if (!training) {
        return null;
    }

    const formattedDate = new Date(training.date).toLocaleDateString("pl-PL", {day: "numeric", month: "long"});

    const handleDelete = () => {
        fetch(`http://192.168.68.64:8000/trainings/${id}`, {
            method: "DELETE"
        })
            .then(() => router.back());
    };

    return (
        <ScrollView style={styles.container}>
             <View style={styles.trainingSectionHeader}>
             <Pressable onPress={() => router.back()}>
                <Ionicons name="chevron-back" size={32} color="#1A1A1A" />
             </Pressable>
             <View style={styles.swimmingAndDateSection}>
                <Text style={styles.pageTittle}>Pływanie</Text>
                <Text style={styles.pageSubtitle}>{formattedDate}</Text>
             </View>
             <Pressable style={styles.menuButton} onPress={handleDelete}>
                <Ionicons name="ellipsis-horizontal" size={24} color="#1A1A1A" />
             </Pressable>
             </View>
             <View style={styles.heroStat}>
                <Text style={styles.heroNumber}>{training.RPE}</Text>
                <Text style={styles.heroLabel}>RPE sesji</Text>
             </View>
             <View style={styles.statsRow}>
                <View style={styles.statBox}>
                    <View style={styles.statHeader}>
                        <MaterialCommunityIcons name="clock-outline" size={18} color="#1A1A1A" />
                        <Text style={styles.statLabel}>Czas</Text>
                    </View>
                    <Text style={styles.statNumber}>{training.time} min</Text>
                </View>
                <View style={styles.statBox}>
                    <View style={styles.statHeader}>
                        <MaterialCommunityIcons name="map-marker-distance" size={18} color="#1A1A1A" />
                        <Text style={styles.statLabel}>Dystans</Text>
                    </View>
                    <Text style={styles.statNumber}>{training.distance} m</Text>
                </View>
             </View>
             <Text style={styles.sectionTitle}>Zadania</Text>
             <View style={styles.tasksList}>
                {training.tasks.map((task, index) => (
                    <View key={index} style={styles.taskCard}>
                        <Text style={styles.taskTitle}>{task.description}</Text>
                        <View style={styles.taskDetailsRow}>
                            <View style={styles.taskDetailItem}>
                                <MaterialCommunityIcons name="map-marker-distance" size={18} color="#1A1A1A" />
                                <Text style={styles.taskDetailText}>{task.task_distance} m</Text>
                            </View>
                            <View style={styles.taskDetailItem}>
                                <MaterialCommunityIcons name="speedometer" size={18} color="#1A1A1A" />
                                <Text style={styles.taskDetailText}>{task.task_target_time}s → {task.average_segment_time}s</Text>
                            </View>
                            <View style={styles.taskDetailItem}>
                                <MaterialCommunityIcons name="pause-circle-outline" size={18} color="#1A1A1A" />
                                <Text style={styles.taskDetailText}>{task.task_break}s</Text>
                            </View>
                        </View>
                    </View>
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
    heroStat: {
        marginTop: 15,
        flexDirection: "column"},
    heroNumber: {
        color: "#6366F1",
        fontSize: 40,
        fontFamily: "Montserrat_700Bold"},
    heroLabel: {
        color: "#1A1A1A",
        fontSize: 14,
        letterSpacing: 1,
        textTransform: "uppercase",
        fontFamily: "Inter_700Bold"},
    pageSubtitle: {
        color: "#1A1A1A",
        fontSize: 16,
        fontFamily: "Montserrat_400Regular"},
    statsRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        marginTop: 30,
        gap: 12},
    statBox: {
        height: 125,
        borderRadius: 20,
        flex: 1,
        backgroundColor: "#F5F5F7",
        padding: 16,
        alignItems: "flex-start"},
    statLabel: {
        color: "#1A1A1A",
        fontSize: 12,
        letterSpacing: 1,
        textTransform: "uppercase",
        fontFamily: "Inter_700Bold"},
    statHeader: {
        flexDirection: "row",
        alignItems: "center",
        gap: 6,
        marginBottom: 8},
    statNumber: {
        fontFamily: "Montserrat_700Bold",
        color: "#1A1A1A",
        fontSize: 30,
        marginTop: 4},
    sectionTitle: {
        marginTop: 30,
        fontSize: 30,
        color: "#1A1A1A",
        fontFamily: "Montserrat_700Bold"},
    tasksList: {
        marginTop: 20,
        gap: 8},
    taskCard: {
        height: 100,
        backgroundColor: "#F5F5F7",
        borderRadius: 20,
        padding: 16},
    taskTitle: {
        color: "#1A1A1A",
        fontSize: 22,
        fontFamily: "Montserrat_700Bold"},
    taskDetailsRow: {
        flexDirection: "row",
        gap: 16,
        marginTop: 8},
    taskDetailItem: {
        flexDirection: "row",
        alignItems: "center",
        gap: 4},
    taskDetailText: {
        color: "#1A1A1A",
        fontSize: 18,
        fontFamily: "Inter_400Regular"},
    menuButton: {
        marginLeft: "auto"}
})