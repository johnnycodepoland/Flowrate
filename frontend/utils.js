export const parseDecimal = (text) => {
    const changedText = text.replace(",", ".")
    return Number(changedText)
};