import {useState} from "react";
import {View, Text, StyleSheet, Pressable} from "react-native";
import {useRouter} from "expo-router";
import {Ionicons} from "@expo/vector-icons";
import Slider from "@react-native-community/slider";
import {useFonts, Montserrat_700Bold, Montserrat_400Regular } from "@expo-google-fonts/montserrat";
import {Inter_700Bold, Inter_400Regular } from "@expo-google-fonts/inter";
import DateTimePicker from "@react-native-community/datetimepicker";

export default function AddTraining() {
    const router = useRouter();
    const [step, setStep] = useState(1);
    const [rpe, setRpe] = useState(5);
    const [date, setDate] = useState(new Date());
    const formattedDate = date.toLocaleDateString("pl-PL", {day: "numeric", month: "long", year: "numeric"});
    const [showDatePicker, setShowDatePicker] = useState(false);
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
        <View style={styles.container}>
            <View style={styles.addTrainingSectionHeader}>
                <Pressable onPress={() => router.back()}>
                    <Ionicons name="chevron-back" size={32} color="#1A1A1A" />
                </Pressable>
                <Text style={styles.pageTitle}>Dodaj trening</Text>
            </View>
            <Text style={styles.label}>RPE sesji: {rpe}</Text>
            <Slider
                style={{width: "100%", height: 40}}
                minimumValue={1}
                maximumValue={10}
                step={1}
                value={rpe}
                onValueChange={setRpe}
                minimumTrackTintColor="#6366F1"
            />
            <Text style={styles.label}>Data treningu</Text>
            <Pressable style={styles.dateBox} onPress={() => setShowDatePicker(true)}>
                <Text style={styles.dateText}>{formattedDate}</Text>
            </Pressable>
            {showDatePicker && (
                <DateTimePicker
                    value={date}
                    mode="date"
                    display="default"
                    onValueChange={(event, selectedDate) => {
                        setShowDatePicker(false);
                        if (selectedDate) {
                            setDate(selectedDate);
                        }
                    }}
                />
            )}
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingHorizontal: 20,
        paddingTop: 70,
        backgroundColor: "#FFFFFF"},
    addTrainingSectionHeader: {
        flexDirection: "row"},
    pageTitle: {
        fontSize: 32,
        color: "#1A1A1A",
        fontFamily: "Montserrat_700Bold",
        marginBottom: 20},
    label: {
        color: "#1A1A1A",
        fontSize: 18,
        fontFamily: "Montserrat_700Bold",
        marginTop: 20,
        marginBottom: 8},
    dateText: {
        color: "#1A1A1A",
        fontSize: 18,
        fontFamily: "Montserrat_400Regular"},
    dateBox: {
        backgroundColor: "#F5F5F7",
        borderRadius: 12,
        paddingVertical: 10,
        paddingHorizontal: 14,
        alignSelf: "flex-start"}
})