import { setToken, setUser, setUserId } from "../utils/auth";

class AuthService {
    constructor() {
        this.url = import.meta.env.VITE_API_URL;
    }

    async loginUser(username, password) {
        const data = {
            username: username,
            password: password
        };

        // try {
        //     const response = await fetch(`${this.url}/auth/login`, {
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/json'
        //         },
        //         body: JSON.stringify(data)
        //     });
        //     if (response.status !== 200) {
        //         return false
        //     }

        //     const tokenData = await response.json();
        //     setToken(tokenData)
        //     setUser(username)
        //     setUserId(tokenData.user_id)
        //     return true;
        // } catch (error) {
        //     console.error('Error al intentar hacer login:', error);
        //     return false
        // }
        return true
    }
}

const authService = new AuthService();

export { authService };
