import {API_URL} from "./config";
import {getToken, deleteToken} from "./auth"
import {router} from "expo-router"

export const apiFetch = async (path, options = {}) => {
    const token = await getToken();

    const res = await fetch(`${API_URL}${path}`, {
        ...options, 
        headers: {
            ...options.headers,
            Authorization: `Bearer ${token}`,
        },
    });

    if (res.status === 401) {
        await deleteToken();
        router.replace("/login")
    }
    return res;
};