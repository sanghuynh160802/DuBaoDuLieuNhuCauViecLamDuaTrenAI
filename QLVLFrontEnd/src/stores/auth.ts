import { IAuthState } from "@/types/user"
import { defineStore } from "pinia"
import { ref } from "vue"

export const useAuthStore = defineStore("auth", () => {
    const state = ref<IAuthState>({
        user: {
            email: "",
            password: "",
            avatar: ""
        },
        isLoggedIn: false,
        isAdmin: false
    })

    const setAuthStore = (data: IAuthState) => {
        state.value = data
        // Persist to localStorage
        localStorage.setItem('authState', JSON.stringify(data))
    }
    
    // Add method to set user type
    const setUserType = (type: string) => {
        state.value.user.user_type = type
        // Also persist this change
        localStorage.setItem('authState', JSON.stringify(state.value))
    }
    
    // Add method to get user type
    const getUserType = () => {
        return state.value.user.user_type
    }
    
    // Initialize from localStorage
    const initializeFromLocalStorage = () => {
        const savedState = localStorage.getItem('authState')
        if (savedState) {
            state.value = JSON.parse(savedState)
        }
    }
    
    // Call initialization
    initializeFromLocalStorage()
    const getUserID = () => {
        return state.value.user.id
    }    
    const getUserName = () => {
        return state.value.user.name
    }
    const getEmail = () => {
        return state.value.user.email
    }
    const getAvatar = () => { 
        return state.value.user.avatar
    }
    const getAge = () => {
        return state.value.user.age
    }

    const getIsLoggedIn = () => {
        return state.value.isLoggedIn
    }
    const getIsAdmin = () => {
        return state.value.isAdmin
    }
    return {
        state,
        setAuthStore,
        setUserType,
        getUserType,
        getUserName,
        getIsLoggedIn,
        getEmail,
        getAvatar,
        getAge,
        getIsAdmin,
        getUserID
    }
})