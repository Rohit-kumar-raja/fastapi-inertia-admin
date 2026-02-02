<script setup lang="ts">
import { ref } from 'vue';
import { useForm } from '@inertiajs/vue3';
import axios from 'axios';

// PrimeVue Components
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Checkbox from 'primevue/checkbox';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import { useToast } from 'primevue/usetoast';

// FontAwesome Setup
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faBolt, faUser, faLock, faArrowRight } from '@fortawesome/free-solid-svg-icons';

// Add icons to the library for this component
library.add(faBolt, faUser, faLock, faArrowRight);

defineOptions({
    layout: null
});

const form = useForm({
    username: '',
    password: '',
    remember: false
});

const toast = useToast();
const loading = ref(false);

const handleLogin = async () => {
    loading.value = true;
    try {
        const response = await axios.post('/api/v1/login', {
            username: form.username,
            password: form.password
        }, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });

        if (response.data.access_token) {
            localStorage.setItem('access_token', response.data.access_token);
            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
            
            toast.add({ severity: 'success', summary: 'Success', detail: 'Welcome back!', life: 1000 });
            
            setTimeout(() => {
                window.location.href = '/';
            }, 500);
        }
    } catch (error: any) {
        toast.add({
            severity: 'error',
            summary: 'Login Failed',
            detail: error.response?.data?.detail || 'Invalid credentials',
            life: 3000
        });
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div class="flex min-h-screen bg-surface-0 dark:bg-surface-950 overflow-hidden">
        
        <!-- Left Side: Branding -->
        <div class="hidden lg:flex w-1/2 bg-primary-600 relative overflow-hidden items-center justify-center p-12">
            <div class="absolute top-0 left-0 w-full h-full opacity-20 pointer-events-none">
                <div class="absolute top-[-10%] left-[-10%] w-96 h-96 bg-white rounded-full blur-3xl"></div>
                <div class="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-surface-900 rounded-full blur-3xl"></div>
            </div>

            <div class="relative z-10 text-white max-w-lg text-center lg:text-left">
                <div class="mb-8 inline-flex items-center justify-center w-16 h-16 rounded-xl bg-white/20 backdrop-blur-sm shadow-lg">
                    <!-- FontAwesome Icon: Logo -->
                    <font-awesome-icon :icon="['fas', 'bolt']" class="text-4xl text-white" />
                </div>
                <h1 class="text-5xl font-bold mb-6 leading-tight">Welcome to <br/> Conquer</h1>
                <p class="text-xl text-primary-100 font-light leading-relaxed">
                    Streamline your workflow, track your progress, and achieve your goals with our powerful platform.
                </p>
            </div>
        </div>

        <!-- Right Side: Login Form -->
        <div class="w-full lg:w-1/2 flex items-center justify-center p-6 lg:p-12">
            <div class="w-full max-w-md">
                
                <div class="mb-10 text-center lg:text-left">
                    <h2 class="text-3xl font-bold text-surface-900 dark:text-surface-0 mb-2">Sign In</h2>
                    <p class="text-surface-500 dark:text-surface-400">Enter your details to access your account</p>
                </div>

                <form @submit.prevent="handleLogin" class="flex flex-col gap-6">
                    
                    <!-- Username Input -->
                    <div class="flex flex-col gap-2">
                        <label for="username" class="font-medium text-surface-900 dark:text-surface-0">Username</label>
                        <IconField>
                            <InputIcon>
                                <!-- FontAwesome Icon: User -->
                                <font-awesome-icon :icon="['fas', 'user']" class="text-surface-400 dark:text-surface-500" />
                            </InputIcon>
                            <InputText 
                                id="username" 
                                v-model="form.username" 
                                class="w-full pl-10" 
                                :class="{'p-invalid': form.errors.username}"
                                placeholder="name@company.com" 
                                size="large"
                            />
                        </IconField>
                        <small v-if="form.errors.username" class="text-red-500 animate-fade-in">{{ form.errors.username }}</small>
                    </div>

                    <!-- Password Input -->
                    <div class="flex flex-col gap-2">
                        <div class="flex justify-between items-center">
                            <label for="password" class="font-medium text-surface-900 dark:text-surface-0">Password</label>
                            <a href="#" class="text-sm font-medium text-primary-600 hover:text-primary-500 transition-colors">Forgot password?</a>
                        </div>
                        <div class="w-full">
                            <IconField>
                                <InputIcon>
                                    <!-- FontAwesome Icon: Lock -->
                                    <font-awesome-icon :icon="['fas', 'lock']" class="text-surface-400 dark:text-surface-500" />
                                </InputIcon>
                            <Password 
                                id="password" 
                                v-model="form.password" 
                                :feedback="false" 
                                toggleMask 
                                :invalid="!!form.errors.password" 
                                placeholder="••••••••"
                                inputClass="w-full pl-10 py-3"
                                class="w-full [&>input]:w-full"
                            >
                                <!-- Custom Header Slot to inject Icon -->
                                <template #header>
                                    <!-- FontAwesome Icon: Lock -->
                                    <font-awesome-icon :icon="['fas', 'lock']" class="absolute left-3 top-1/2 -translate-y-1/2 text-surface-400 z-10 pointer-events-none" />
                                </template>
                            </Password>
                            </IconField>
                        </div>
                        <small v-if="form.errors.password" class="text-red-500 animate-fade-in">{{ form.errors.password }}</small>
                    </div>

                    <!-- Remember Me -->
                    <div class="flex items-center gap-2">
                        <Checkbox v-model="form.remember" inputId="remember" binary />
                        <label for="remember" class="text-surface-600 dark:text-surface-300 cursor-pointer select-none">Remember me for 30 days</label>
                    </div>

                    <!-- Submit Button -->
                    <Button 
                        type="submit" 
                        class="w-full py-3 text-lg font-semibold shadow-md hover:shadow-lg transition-all duration-300 flex justify-center gap-2" 
                        :loading="loading" 
                    >
                        <span>Sign In</span>
                        <!-- FontAwesome Icon: Arrow Right (Using span/slot instead of icon prop) -->
                        <font-awesome-icon :icon="['fas', 'arrow-right']" v-if="!loading" />
                    </Button>

                    <div class="text-center mt-6 text-surface-500 dark:text-surface-400">
                        Don't have an account? 
                        <a href="#" class="font-bold text-primary-600 hover:text-primary-500 hover:underline transition-all">Create account</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-5px); }
    to { opacity: 1; transform: translateY(0); }
}

:deep(.p-password) {
    position: relative;
    width: 100%;
}
:deep(.p-password-input) {
    padding-left: 2.5rem !important;
}
</style>