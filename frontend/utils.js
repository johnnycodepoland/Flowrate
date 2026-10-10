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