import {Stack} from "expo-router";
import {GestureHandlerRootView} from "react-native-gesture-handler";

export default function RootLayout() {
    return (
        <GestureHandlerRootView style={{flex: 1}}>
            <Stack screenOptions={{headerShown: false}} >
                <Stack.Screen
                    name="add-training" 
                    options={ { gestureEnabled: false }}
                />
                <Stack.Screen
                    name="edit-training/[id]" 
                    options={{ gestureEnabled: false }}
                />
            </Stack>
        </GestureHandlerRootView>
    );
}