import { defineStore } from 'pinia';
import { ref } from 'vue';
import { admin, deleteCookie } from '@/core';
import axios from 'axios';
import { router } from '@inertiajs/vue3';
import { usePermission } from '@/Composables/usePermission';

export const useUserStore = defineStore('user', () => {
    // Try to load initial user from localStorage if present
    const storedUser = localStorage.getItem('user_data');
    const user = ref<any>(storedUser ? JSON.parse(storedUser) : null);

    // Authenticated if we have stored user data, or will be set true on successful login/fetch
    const isAuthenticated = ref(!!storedUser);
    const { loadPermissions, clearPermissions, initPermissions } = usePermission();

    // Initialize permissions from localStorage on store creation
    initPermissions();

    function setUser(userData: any) {
        user.value = userData;
        localStorage.setItem('user_data', JSON.stringify(userData));
        isAuthenticated.value = true;
    }

    async function fetchUser() {
        try {
            const response = await axios.get(admin.SETTINGS_PROFILE_API);
            if (response.data.data) {
                user.value = response.data.data;
                localStorage.setItem('user_data', JSON.stringify(response.data.data));
                isAuthenticated.value = true;
            }
        } catch (error) {
            console.error('Failed to fetch user profile:', error);
            isAuthenticated.value = false;
            user.value = null;
            localStorage.removeItem('user_data');
        }
    }
    onMounted(setUser)

    async function login(credentials: any) {
        const response = await axios.post(admin.LOGIN_API, credentials, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });

        // The backend sets the HTTP-Only cookie automatically.
        if (response.data.access_token) {
            isAuthenticated.value = true;

            // Save user data to state and localStorage if it's sent back during login
            if (response.data.user || response.data.data?.user) {
                const userData = response.data.user || response.data.data.user;
                user.value = userData;
                localStorage.setItem('user_data', JSON.stringify(userData));
            }

            // Load permissions from login response
            const permissions = response.data.data?.permissions || response.data.permissions || [];
            loadPermissions(permissions);

            // Redirect to dashboard
            router.visit('/admin/dashboard');
        }
        return response;
    }

    function logout() {
        user.value = null;
        isAuthenticated.value = false;
        localStorage.removeItem('user_data');
        clearPermissions();
        deleteCookie('access_token');
        // Redirect to login
        router.visit('/admin/login');
    }

    return {
        user,
        isAuthenticated,
        setUser,
        fetchUser,
        login,
        logout
    };
});