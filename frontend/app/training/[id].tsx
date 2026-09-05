import {Text, View} from "react-native";
import {useLocalSearchParams} from "expo-router";

export default function TrainingDetails() {
    const {id} = useLocalSearchParams();

    return (
        <View>
            <Text>Szczegóły treningu {id}</Text>
        </View>
    )
}