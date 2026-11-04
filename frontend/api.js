import {API_URL} from "./config";
import {getToken, deleteToken} from "./auth"

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
    }
    return res;
};