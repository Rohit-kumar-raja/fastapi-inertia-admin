<script setup lang="ts">
import { useForm } from '@inertiajs/vue3';
import { useUserStore } from '@/Store/userStore';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useToast } from 'primevue';
import { faBolt, faUser, faLock, faArrowRight } from '@fortawesome/free-solid-svg-icons';
import { Link } from '@inertiajs/vue3';

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
const userStore = useUserStore();

const handleLogin = async () => {
    loading.value = true;
    try {
        await userStore.login({
            username: form.username,
            password: form.password
        });

        toast.add({ severity: 'success', summary: 'Success', detail: 'Welcome back!', life: 1000 });

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
    <div class="flex min-h-screen overflow-hidden bg-surface-50 dark:bg-surface-950">

        <!-- Left Side: Branding & Visuals (Hidden on mobile) -->
        <div class="hidden lg:flex w-1/2 relative bg-surface-900 overflow-hidden items-center justify-center p-12">
            <!-- Animated Background Mesh -->
            <div class="absolute inset-0 w-full h-full bg-linear-to-br from-primary-900 via-surface-900 to-black z-0">
            </div>

            <div class="absolute top-0 left-0 w-full h-full overflow-hidden opacity-30 pointer-events-none z-0">
                <div
                    class="absolute top-[-20%] left-[-10%] w-160 h-160 bg-primary-500 rounded-full blur-[120px] animate-blob">
                </div>
                <div
                    class="absolute bottom-[-20%] right-[-10%] w-140 h-140 bg-purple-500 rounded-full blur-[100px] animate-blob animation-delay-2000">
                </div>
                <div
                    class="absolute top-[40%] left-[30%] w-120 h-120 bg-blue-400 rounded-full blur-[90px] animate-blob animation-delay-4000">
                </div>
            </div>

            <!-- Glassmorphism Content Card -->
            <div
                class="relative z-10 p-10 bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl max-w-lg w-full text-center lg:text-left transform hover:scale-[1.01] transition-transform duration-500">
                <div
                    class="mb-8 inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-linear-to-tr from-primary-500 to-purple-600 shadow-lg shadow-primary-500/30">
                    <font-awesome-icon :icon="faBolt" class="text-4xl text-white" />
                </div>

                <h1 class="text-5xl font-extrabold mb-6 leading-tight text-white tracking-tight">
                    Welcome to <span
                        class="text-transparent bg-clip-text bg-linear-to-r from-primary-300 to-purple-300">Conquer</span>
                </h1>

                <p class="text-lg text-surface-200 font-light leading-relaxed mb-8">
                    Elevate your productivity with our next-generation platform. Streamline workflows, track progress,
                    and achieve your goals faster than ever.
                </p>

                <div class="flex gap-4 justify-center lg:justify-start">
                    <div class="flex -space-x-3">
                        <img class="w-10 h-10 rounded-full border-2 border-surface-900"
                            src="https://i.pravatar.cc/100?img=1" alt="User" />
                        <img class="w-10 h-10 rounded-full border-2 border-surface-900"
                            src="https://i.pravatar.cc/100?img=2" alt="User" />
                        <img class="w-10 h-10 rounded-full border-2 border-surface-900"
                            src="https://i.pravatar.cc/100?img=3" alt="User" />
                        <div
                            class="w-10 h-10 rounded-full border-2 border-surface-900 bg-surface-700 flex items-center justify-center text-xs text-white font-medium">
                            +2k</div>
                    </div>
                    <div class="flex flex-col text-left">
                        <span class="text-white font-bold text-sm">Trusted by</span>
                        <span class="text-surface-400 text-xs">2,000+ Teams Worldwide</span>
                    </div>
                </div>
            </div>

            <!-- Decorative Overlay Pattern -->
            <div
                class="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay pointer-events-none">
            </div>
        </div>

        <!-- Right Side: Login Form -->
        <div class="w-full lg:w-1/2 flex items-center justify-center p-6 lg:p-12 relative">
            <div
                class="relative w-full max-w-md bg-white dark:bg-surface-900 p-8 md:p-10 rounded-3xl shadow-xl border border-surface-100 dark:border-surface-800 animate-fade-in-up">

                <div class="mb-8 text-center">
                    <div
                        class="inline-flex lg:hidden mb-4 items-center justify-center w-14 h-14 rounded-xl bg-primary-600 text-white shadow-lg">
                        <font-awesome-icon :icon="faBolt" class="text-2xl" />
                    </div>
                    <h2 class="text-3xl font-bold text-surface-900 dark:text-surface-0 mb-2 tracking-tight">Sign In</h2>
                    <p class="text-surface-500 dark:text-surface-400">Welcome back! Please enter your details.</p>
                </div>

                <form @submit.prevent="handleLogin" class="flex flex-col gap-5">

                    <!-- Username Input -->
                    <div class="flex flex-col gap-2 group">
                        <label for="username"
                            class="font-medium text-surface-700 dark:text-surface-200 group-focus-within:text-primary-600 transition-colors">Username
                            or Email</label>
                        <IconField>
                            <InputIcon>
                                <font-awesome-icon :icon="faUser"
                                    class="text-surface-400 dark:text-surface-500 group-focus-within:text-primary-500 transition-colors" />
                            </InputIcon>
                            <InputText id="username" v-model="form.username"
                                class="w-full pl-10 rounded-xl! border-surface-300! dark:border-surface-700! focus:border-primary-500! focus:ring-4! focus:ring-primary-100! dark:focus:ring-primary-900/30! transition-all duration-300"
                                :class="{ 'border-red-500! focus:ring-red-100!': form.errors.username }"
                                placeholder="name@company.com" size="large" />
                        </IconField>
                        <small v-if="form.errors.username" class="text-red-500 text-xs mt-1 animate-shake">{{
                            form.errors.username }}</small>
                    </div>

                    <!-- Password Input -->
                    <div class="flex flex-col gap-2 group">
                        <div class="flex justify-between items-center">
                            <label for="password"
                                class="font-medium text-surface-700 dark:text-surface-200 group-focus-within:text-primary-600 transition-colors">Password</label>
                            <Link href="/login/admin/forgot-password"
                                class="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 transition-colors hover:underline">
                                Forgot
                                password?</Link>
                        </div>
                        <div class="w-full">
                            <IconField>
                                <InputIcon class="z-10">
                                    <font-awesome-icon :icon="faLock"
                                        class="text-surface-400 dark:text-surface-500 group-focus-within:text-primary-500 transition-colors" />
                                </InputIcon>
                                <Password id="password" v-model="form.password" :feedback="false" toggleMask
                                    :invalid="!!form.errors.password" placeholder="••••••••"
                                    inputClass="w-full pl-10 py-3 rounded-xl! border-surface-300! dark:border-surface-700! focus:border-primary-500! focus:ring-4! focus:ring-primary-100! dark:focus:ring-primary-900/30! transition-all duration-300"
                                    class="w-full [&>input]:w-full" />
                            </IconField>
                        </div>
                        <small v-if="form.errors.password" class="text-red-500 text-xs mt-1 animate-shake">{{
                            form.errors.password }}</small>
                    </div>

                    <!-- Remember Me -->
                    <div class="flex items-center gap-2 mt-1">
                        <Checkbox v-model="form.remember" inputId="remember" binary class="peer" />
                        <label for="remember"
                            class="text-sm text-surface-600 dark:text-surface-300 cursor-pointer select-none peer-focus:text-primary-600 transition-colors">Remember
                            me for 30 days</label>
                    </div>

                    <!-- Submit Button -->
                    <Button type="submit"
                        class="w-full py-3.5 mt-2 rounded-xl text-lg font-bold shadow-lg shadow-primary-500/20 hover:shadow-primary-500/40 hover:-translate-y-0.5 active:translate-y-0 active:shadow-md transition-all duration-300 flex justify-center gap-2 bg-linear-to-r from-primary-600 to-primary-500 border-none"
                        :loading="loading" label="Sign In" iconPos="right">
                        <template #icon>
                            <font-awesome-icon :icon="faArrowRight" class="animate-pulse-slow" />
                        </template>
                    </Button>

                    <!-- Divider -->
                    <div class="relative flex py-4 items-center">
                        <div class="grow border-t border-surface-200 dark:border-surface-700"></div>
                        <span class="shrink mx-4 text-surface-400 text-sm">Or continue with</span>
                        <div class="grow border-t border-surface-200 dark:border-surface-700"></div>
                    </div>

                    <!-- Social Login (Mock) -->
                    <div class="grid grid-cols-2 gap-3">
                        <button type="button"
                            class="flex items-center justify-center gap-2 px-4 py-2.5 border border-surface-200 dark:border-surface-700 rounded-xl hover:bg-surface-50 dark:hover:bg-surface-800 transition-colors text-surface-700 dark:text-white font-medium text-sm">
                            <!-- Google SVG Icon -->
                            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path
                                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                                    fill="#4285F4" />
                                <path
                                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                                    fill="#34A853" />
                                <path
                                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                                    fill="#FBBC05" />
                                <path
                                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                                    fill="#EA4335" />
                            </svg>
                            Google
                        </button>
                        <button type="button"
                            class="flex items-center justify-center gap-2 px-4 py-2.5 border border-surface-200 dark:border-surface-700 rounded-xl hover:bg-surface-50 dark:hover:bg-surface-800 transition-colors text-surface-700 dark:text-white font-medium text-sm">
                            <!-- GitHub SVG Icon -->
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                <path fill-rule="evenodd"
                                    d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                                    clip-rule="evenodd" />
                            </svg>
                            GitHub
                        </button>
                    </div>

                    <div class="text-center mt-6 text-surface-500 dark:text-surface-400 text-sm">
                        Don't have an account?
                        <a href="#"
                            class="font-bold text-primary-600 hover:text-primary-500 hover:underline transition-all">Create
                            account</a>
                    </div>
                </form>
            </div>

            <!-- Mobile Footer / Copyright -->
            <div class="absolute bottom-4 text-center w-full text-xs text-surface-400 lg:hidden">
                &copy; {{ new Date().getFullYear() }} Conquer. All rights reserved.
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Keyframes for animations */
@keyframes blob {
    0% {
        transform: translate(0px, 0px) scale(1);
    }

    33% {
        transform: translate(30px, -50px) scale(1.1);
    }

    66% {
        transform: translate(-20px, 20px) scale(0.9);
    }

    100% {
        transform: translate(0px, 0px) scale(1);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes shake {

    0%,
    100% {
        transform: translateX(0);
    }

    10%,
    30%,
    50%,
    70%,
    90% {
        transform: translateX(-4px);
    }

    20%,
    40%,
    60%,
    80% {
        transform: translateX(4px);
    }
}

.animate-blob {
    animation: blob 7s infinite;
}

.animation-delay-2000 {
    animation-delay: 2s;
}

.animation-delay-4000 {
    animation-delay: 4s;
}

.animate-fade-in-up {
    animation: fadeInUp 0.6s ease-out forwards;
}

.animate-shake {
    animation: shake 0.4s cubic-bezier(.36, .07, .19, .97) both;
}

.animate-pulse-slow {
    animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: .7;
    }
}

/* Custom shadow utility not in tailwind config yet */
.shadow-primary-500\/30 {
    box-shadow: 0 10px 40px -10px rgba(59, 130, 246, 0.3);
}

.shadow-primary-500\/20 {
    box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2), 0 2px 4px -1px rgba(59, 130, 246, 0.1);
}

.shadow-primary-500\/40 {
    box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4), 0 4px 6px -2px rgba(59, 130, 246, 0.2);
}
</style>