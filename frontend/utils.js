import {Alert} from "react-native";

export const parseDecimal = (text) => {
    const changedText = text.replace(",", ".")
    return Number(changedText)
};

export const hasAnyTime = (task) => {
    for (const segment of task.segments) {
        if (segment.target_time !== null) {
            return true;
        }
    }
    return false;
};

export const showError = (message) => {
    Alert.alert("Błąd", message)
};

export const parseTime = (text) => {
    const changedText = text.replace(",",".")

    if (changedText.includes(":")) {
        const changedTextSplit = changedText.split(":")

        if (changedTextSplit.length !== 2 || Number(changedTextSplit[1] >= 60)) {
            return NaN
        }

        const timeInSeconds = Number(changedTextSplit[0]) * 60 + Number(changedTextSplit[1])

        return timeInSeconds;
    }

    return Number(changedText)
};

export const formatTime = (seconds) => {
    if (seconds < 60) {
        return String(seconds)
    }

    const minutes = Math.floor(seconds / 60)

    const rest = seconds - minutes * 60

    const restRound = Math.round(rest * 10) / 10

    if (restRound < 10) {
        const finalTime = `${minutes}:0${restRound}`

        return finalTime
    }

    const finalTime = `${minutes}:${restRound}`

    return finalTime
};