import { useAuthStore } from "./auth"
import { getInfo } from "@/services/user.service"
import { jwtDecode } from 'jwt-decode';

export const initAuthStore = async () => {
    const authStore = useAuthStore()
    const accessToken = localStorage.getItem("access_token");
    if (accessToken) {
        const decodedToken = jwtDecode(accessToken) as { role: string };
        const roles = decodedToken.role;
        
        // Normalize the role by removing spaces and converting to lowercase
        const normalizedRole = roles.replace(/\s+/g, '').toLowerCase();
        
        // Check if the normalized role contains 'admin'
        const isAdmin = normalizedRole.includes('admin');
        
        const { data } = await getInfo()
        authStore.setAuthStore({
            user: data,
            isLoggedIn: true,
            isAdmin: isAdmin
        })
        
        console.log("initAuthStore", authStore.getIsLoggedIn(), authStore.getIsAdmin())
    }
}