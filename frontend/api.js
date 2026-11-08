import {API_URL} from "./config";
import {getToken, deleteToken} from "./auth"
import {router} from "expo-router"

export const apiFetch = async (path, options = {}) => {
    const token = await getToken();
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000)
    let res;
    try {
        res = await fetch(`${API_URL}${path}`, {
        ...options,
        signal: controller.signal,
        headers: {
            ...options.headers,
            Authorization: `Bearer ${token}`,
        },
        });
    } 
    finally {clearTimeout(timeout)}

    if (res.status === 401) {
        await deleteToken();
        router.replace("/login")
    }
    return res;
};