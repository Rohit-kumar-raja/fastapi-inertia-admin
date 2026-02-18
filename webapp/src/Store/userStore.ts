import { defineStore } from 'pinia';
import { ref } from 'vue';
import { admin, deleteCookie } from '@/core';
import axios from 'axios';
import { router } from '@inertiajs/vue3';

export const useUserStore = defineStore('user', () => {
    const user = ref<any>(null);
    const isAuthenticated = ref(!!localStorage.getItem('access_token'));

    function setUser(userData: any) {
        user.value = userData;
        isAuthenticated.value = true;
    }

    async function login(credentials: any) {
        try {
            const response = await axios.post(admin.LOGIN_API, credentials, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            if (response.data.access_token) {
                const token = response.data.access_token;
                localStorage.setItem('access_token', token);
                axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                isAuthenticated.value = true;

                // Redirect to dashboard
                router.visit('/admin/dashboard');
            }
            return response;
        } catch (error: any) {
            throw error;
        }
    }

    function logout() {
        localStorage.removeItem('access_token');
        delete axios.defaults.headers.common['Authorization'];
        user.value = null;
        isAuthenticated.value = false;
        deleteCookie('access_token');
        // Redirect to login
        router.visit('/admin/login');
    }

    return {
        user,
        isAuthenticated,
        setUser,
        login,
        logout
    };
});