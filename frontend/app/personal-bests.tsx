import {View, Text, StyleSheet, Pressable, TextInput} from "react-native";
import {useFonts, Montserrat_700Bold, Montserrat_400Regular } from "@expo-google-fonts/montserrat";
import {Inter_700Bold, Inter_400Regular } from "@expo-google-fonts/inter";
import {Ionicons} from "@expo/vector-icons";
import {router} from "expo-router";

export default function PersonalBests() {
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
            <View style={styles.trainingSectionHeader}>
                <Pressable onPress={() => router.back()}>
                    <Ionicons name="chevron-back" size={32} color="#1A1A1A" />
                </Pressable>
            </View>
            <View style={styles.swimmingAndDateSection}>
                <Text style={styles.pageTittle}>Rekordy życiowe</Text>
            </View>
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
    trainingSectionHeader: {
        alignItems: "center",
        flexDirection: "row"},
    swimmingAndDateSection: {
        alignItems: "center",
        flexDirection: "column"}
})