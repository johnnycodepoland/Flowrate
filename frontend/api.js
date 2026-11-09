import {API_URL} from "./config";
import {getToken, deleteToken} from "./auth"
import {router} from "expo-router"

export const apiFetch = async (path, options = {}) => {
    const token = await getToken();
    const res = await fetchWithTimeout(`${API_URL}${path}`, {
        ...options,
        headers: {
            ...options.headers,
            Authorization:`Bearer ${token}`, 
        },
    });

    if (res.status === 401) {
        await deleteToken();
        router.replace("/login")
    }
    return res;
};

export const fetchWithTimeout = async (url, options = {}) => {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000)
    let res;
    try {
        res = await fetch(url, {
        ...options,
        signal: controller.signal,
        });
    } 
    finally {clearTimeout(timeout)}
    return res;
};