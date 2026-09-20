import {useState, useEffect} from "react";
import {View, Text, StyleSheet, Pressable, TextInput, Keyboard, TouchableWithoutFeedback, Modal} from "react-native";
import {useRouter, useLocalSearchParams} from "expo-router";
import {Ionicons, MaterialCommunityIcons} from "@expo/vector-icons";
import Slider from "@react-native-community/slider";
import {useFonts, Montserrat_700Bold, Montserrat_400Regular } from "@expo-google-fonts/montserrat";
import {Inter_700Bold, Inter_400Regular } from "@expo-google-fonts/inter";
import {Swipeable} from "react-native-gesture-handler";
import DateTimePicker from "@react-native-community/datetimepicker";

export default function AddTraining() {
    const router = useRouter();
    const {id} = useLocalSearchParams();
    const [step, setStep] = useState(1);
    const [rpe, setRpe] = useState(5);
    const [date, setDate] = useState(new Date());
    const formattedDate = date.toLocaleDateString("pl-PL", {day: "numeric", month: "long", year: "numeric"});
    const [showDatePicker, setShowDatePicker] = useState(false);
    const [taskDescription, setTaskDescription] = useState("");
    const [taskDistance, setTaskDistance] = useState("");
    const [taskReps, setTaskReps] = useState("");
    const [taskTargetTime, setTaskTargetTime] = useState("");
    const [taskBreak, setTaskBreak] = useState("");
    const [averageSegmentTime, setAverageSegmentTime] = useState("");
    const [tasks, setTasks] = useState([]);
    const [modalVisible, setModalVisible] = useState(false);
    const [fontLoaded] = useFonts({
        Montserrat_700Bold,
        Montserrat_400Regular,
        Inter_700Bold,
        Inter_400Regular,
    });
    const handleBack = () => {
        if (step ===1) {
            router.back();
         } else {
             setStep(step - 1);
         }
    };

    const handleAddTask = () => {
        const newTask = {
            description: taskDescription,
            task_distance: Number(taskDistance),
            task_reps: Number(taskReps),
            task_target_time: Number(taskTargetTime),
            task_break: Number(taskBreak),
            average_segment_time: Number(averageSegmentTime),
        };
        const updatedTasks = [...tasks, newTask];
        setTasks(updatedTasks);
        setTaskDescription("");
        setTaskDistance("");
        setTaskReps("");
        setTaskTargetTime("");
        setTaskBreak("");
        setAverageSegmentTime("");
        setModalVisible(false);
    };

    const handleSave = () => {
        let allTasks = tasks;

        if (taskDescription.trim() !== "") {
            const lastTask = {
                description: taskDescription,
                task_distance: Number(taskDistance),
                task_reps: Number(taskReps),
                task_target_time: Number(taskTargetTime),
                task_break: Number(taskBreak),
                average_segment_time: Number(averageSegmentTime),
            };
            allTasks = [...tasks, lastTask]
        }

        const totalDistance = allTasks.reduce((sum, task) => sum + task.task_distance * task.task_reps, 0);
        const totalTime = allTasks.reduce((sum, task) => sum + (task.task_target_time + task.task_break) * task.task_reps, 0);

        const newTraining = {
            date: date.toISOString().split("T")[0],
            time: Math.round(totalTime / 60),
            distance: totalDistance,
            RPE: rpe,
            tasks: allTasks,
        };

        fetch(`http://192.168.68.59:8000/trainings/${id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({...newTraining, id: Number(id)}),
        })
            .then(() => router.push("/"));
    };

    const handleRemoveTask = (indexToRemove) => {
        setTasks(tasks.filter((_, index) => index !== indexToRemove));
    };

    useEffect(() => {
        fetch(`http://192.168.68.59:8000/trainings/${id}`)
            .then(response => response.json())
            .then(data => {
                setRpe(data.RPE);;
                setDate(new Date(data.date));
                setTasks(data.tasks);
            });
    }, []);

    if (!fontLoaded) {
        return null;
    }

    return (
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
            <View style={styles.container}>
                <View style={styles.addTrainingSectionHeader}>
                    <Pressable onPress={handleBack}>
                        <Ionicons name="chevron-back" size={32} color="#1A1A1A" />
                    </Pressable>
                    <Text style={styles.pageTitle}>Edytuj trening</Text>
                </View>

                {step === 1 && (
                    <>
                        <Text style={styles.label}>RPE sesji: {rpe}</Text>
                        <Slider
                            style={{width: "100%", height: 40}}
                            minimumValue={1}
                            maximumValue={10}
                            step={1}
                            value={rpe}
                            onValueChange={setRpe}
                            minimumTrackTintColor="#6366F1"
                            maximumTrackTintColor="#F5F5F7"
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
                        <Pressable style={styles.nextButton} onPress={() => setStep(2)}>
                            <Text style={styles.nextButtonText}>Dalej</Text>
                        </Pressable>
                    </>
                )}

                {step === 2 && (
                    <>
                        <View style={styles.tasksList}>
                            {tasks.map((task, index) => (
                                <Swipeable
                                    key={index}
                                    renderRightActions={() => (
                                        <Pressable style={styles.deleteAction} onPress={() => handleRemoveTask(index)}>
                                            <Text style={styles.deleteActionText}>Usuń</Text>
                                       </Pressable>
                                    )}
                                >
                                    <View style={styles.taskCard}>
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
                                </Swipeable>
                            ))}
                        </View>
                        <Pressable style={styles.nextButton} onPress={() => setModalVisible(true)}>
                            <Text style={styles.nextButtonText}>Dodaj nowe zadanie</Text>
                        </Pressable>
                        <Pressable style={[styles.nextButton, {marginTop: 12}]} onPress={handleSave}>
                            <Text style={styles.nextButtonText}>Zakończ i zapisz trening</Text>
                        </Pressable>
                        <Modal
                            visible={modalVisible}
                            animationType="slide"
                            presentationStyle="pageSheet"
                        >
                            <View style={styles.modalContent}>
                                <Pressable onPress={() => setModalVisible(false)} style={{padding: 20, alignSelf: "flex-end"}}>
                                    <Ionicons name="close" size={28} color="#1A1A1A" />
                                </Pressable>
                                <Text style={styles.label}>Opis zadania</Text>
                                <TextInput
                                    style={styles.input}
                                    placeholder="np. 8x50m"
                                    value={taskDescription}
                                    onChangeText={setTaskDescription}
                                />

                                <Text style={styles.label}>Dystans odcinka (m)</Text>
                                <TextInput
                                    style={styles.input}
                                    placeholder="np. 1000"
                                    value={taskDistance}
                                    onChangeText={setTaskDistance}
                                    keyboardType="numeric"
                                />

                                <Text style={styles.label}>Liczba powtórzeń</Text>
                                <TextInput
                                    style={styles.input}
                                    placeholder="np. 8"
                                    value={taskReps}
                                    onChangeText={setTaskReps}
                                    keyboardType="numeric"
                                />

                                <Text style={styles.label}>Docelowy czas powórzenia (s)</Text>
                                <TextInput
                                    style={styles.input}
                                    placeholder="np. 30"
                                    value={taskTargetTime}
                                    onChangeText={setTaskTargetTime}
                                    keyboardType="numeric"
                                />

                                <Text style={styles.label}>Przerwa (s)</Text>
                                <TextInput
                                    style={styles.input}
                                    placeholder="np. 20"
                                    value={taskBreak}
                                    onChangeText={setTaskBreak}
                                    keyboardType="numeric"
                                />

                                <Text style={styles.label}>Średni czas powórzenia (s)</Text>
                                <TextInput
                                    style={styles.input}
                                    placeholder="np. 31"
                                    value={averageSegmentTime}
                                    onChangeText={setAverageSegmentTime}
                                    keyboardType="numeric"
                                />

                                <Pressable style={styles.nextButton} onPress={handleAddTask}>
                                    <Text style={styles.nextButtonText}>Zatwierdź</Text>
                                </Pressable>
                            </View>
                        </Modal>
                    </>
                )}
            </View>
        </TouchableWithoutFeedback>
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
        alignSelf: "flex-start"},
    nextButton: {
        backgroundColor: "#6366F1",
        borderRadius: 16,
        paddingVertical: 14,
        alignItems: "center",
        marginTop: 40},
    nextButtonText: {
        color: "#FFFFFF",
        fontSize: 18,
        fontFamily: "Montserrat_700Bold"},
    input: {
        backgroundColor: "#F5F5F7",
        borderRadius: 12,
        paddingVertical: 12,
        paddingHorizontal: 14,
        fontSize: 16,
        fontFamily: "Montserrat_400Regular",
        color: "#1A1A1A"},
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
    deleteAction: {
        backgroundColor: "#FF3B30",
        justifyContent: "center",
        alignItems: "center",
        width: 80,
        borderRadius: 20},
    deleteActionText: {
        color: "#FFFFFF",
        fontFamily: "Montserrat_700Bold"},
    modalContent: {
        flex: 1,
        paddingHorizontal: 20,
        backgroundColor: "#FFFFFF"}
})