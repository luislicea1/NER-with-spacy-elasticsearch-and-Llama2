
export const setToken = (tokenData) => {
    localStorage.setItem('access_token', tokenData.access_token);
}

export const getToken = () => {
    return localStorage.getItem('access_token')
}

export const setUser = (user) => {
    localStorage.setItem('user', user);
}

export const setUserId = (userId) => {
    localStorage.setItem("user_id", userId)
}

export const getUser = () => {
    const user = localStorage.getItem('user')
    return user ? user : ''
}

export const getUserId = () => {
    const userId = localStorage.getItem('user_id')
    return userId ? userId : 0
}

export const isLoggedIn = () => {
    const token = getToken()
    return Boolean(token)
}

export function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
}