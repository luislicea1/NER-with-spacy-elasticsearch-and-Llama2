
export const setToken = (tokenData) => {
    localStorage.setItem('access_token_ner', tokenData.access_token);
}

export const getToken = () => {
    return localStorage.getItem('access_token_ner')
}

export const setUser = (user) => {
    localStorage.setItem('user_ner', user);
}

export const setUserId = (userId) => {
    localStorage.setItem("user_id_ner", userId)
}

export const getUser = () => {
    const user = localStorage.getItem('user_ner')
    return user ? user : ''
}

export const getUserId = () => {
    const userId = localStorage.getItem('user_id_ner')
    return userId ? userId : 0
}

export const isLoggedIn = () => {
    const token = getToken()
    return Boolean(token)
}

export const setRole = (rol) => {
    localStorage.setItem("rol_ner", rol) 
}


export const getRole = () => {
    return localStorage.getItem("rol_ner") 
    
}
