<script setup lang="ts">
import { useForm } from '@inertiajs/vue3';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useToast } from 'primevue';
import { faBolt, faLock, faArrowRight, faArrowLeft } from '@fortawesome/free-solid-svg-icons';
import { Link } from '@inertiajs/vue3';
import { ref } from 'vue';

defineOptions({
    layout: null
});

const props = defineProps<{
    token: string;
    email: string;
}>();

const form = useForm({
    token: props.token,
    email: props.email,
    password: '',
    password_confirmation: '',
});

const toast = useToast();
const loading = ref(false);

const handleResetPassword = () => {
    loading.value = true;
    form.post('/login/reset-password', {
        onSuccess: (page) => {
            toast.add({ severity: 'success', summary: 'Success', detail: page.props.message || 'Password reset successfully. You can now login.', life: 5000 });
            // Optionally redirect to login, but inertia might handle it or user can click link
        },
        onError: (errors) => {
            const errorMessage = Object.values(errors)[0] || 'An error occurred. Please try again.';
            toast.add({
                severity: 'error',
                summary: 'Reset Failed',
                detail: errorMessage as string,
                life: 5000
            });
        },
        onFinish: () => {
            loading.value = false;
        }
    });
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
                    Set a New Password
                </h1>

                <p class="text-lg text-surface-200 font-light leading-relaxed mb-8">
                    Choose a strong password to secure your Conquer account. Make sure you don't use it anywhere else!
                </p>
            </div>

            <!-- Decorative Overlay Pattern -->
            <div
                class="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay pointer-events-none">
            </div>
        </div>

        <!-- Right Side: Reset Form -->
        <div class="w-full lg:w-1/2 flex items-center justify-center p-6 lg:p-12 relative">
            <div
                class="relative w-full max-w-md bg-white dark:bg-surface-900 p-8 md:p-10 rounded-3xl shadow-xl border border-surface-100 dark:border-surface-800 animate-fade-in-up">

                <div class="mb-4">
                    <Link href="/login"
                        class="inline-flex items-center gap-2 text-sm font-medium text-surface-500 hover:text-primary-600 transition-colors mb-6">
                        <font-awesome-icon :icon="faArrowLeft" />
                        Back to Login
                    </Link>
                </div>

                <div class="mb-8 text-center">
                    <div
                        class="inline-flex lg:hidden mb-4 items-center justify-center w-14 h-14 rounded-xl bg-primary-600 text-white shadow-lg">
                        <font-awesome-icon :icon="faBolt" class="text-2xl" />
                    </div>
                    <h2 class="text-3xl font-bold text-surface-900 dark:text-surface-0 mb-2 tracking-tight">Create New
                        Password</h2>
                    <p class="text-surface-500 dark:text-surface-400">Please enter your new password below for {{
                        form.email }}.</p>
                </div>

                <form @submit.prevent="handleResetPassword" class="flex flex-col gap-5">

                    <!-- Password Input -->
                    <div class="flex flex-col gap-2 group">
                        <label for="password"
                            class="font-medium text-surface-700 dark:text-surface-200 group-focus-within:text-primary-600 transition-colors">New
                            Password</label>
                        <div class="w-full">
                            <IconField>
                                <InputIcon class="z-10">
                                    <font-awesome-icon :icon="faLock"
                                        class="text-surface-400 dark:text-surface-500 group-focus-within:text-primary-500 transition-colors" />
                                </InputIcon>
                                <Password id="password" v-model="form.password" :feedback="true" toggleMask
                                    :invalid="!!form.errors.password" placeholder="••••••••" required
                                    inputClass="w-full pl-10 py-3 rounded-xl! border-surface-300! dark:border-surface-700! focus:border-primary-500! focus:ring-4! focus:ring-primary-100! dark:focus:ring-primary-900/30! transition-all duration-300"
                                    class="w-full [&>input]:w-full" />
                            </IconField>
                        </div>
                        <small v-if="form.errors.password" class="text-red-500 text-xs mt-1 animate-shake">{{
                            form.errors.password }}</small>
                    </div>

                    <!-- Confirm Password Input -->
                    <div class="flex flex-col gap-2 group">
                        <label for="password_confirmation"
                            class="font-medium text-surface-700 dark:text-surface-200 group-focus-within:text-primary-600 transition-colors">Confirm
                            Password</label>
                        <div class="w-full">
                            <IconField>
                                <InputIcon class="z-10">
                                    <font-awesome-icon :icon="faLock"
                                        class="text-surface-400 dark:text-surface-500 group-focus-within:text-primary-500 transition-colors" />
                                </InputIcon>
                                <Password id="password_confirmation" v-model="form.password_confirmation"
                                    :feedback="false" toggleMask :invalid="!!form.errors.password_confirmation"
                                    placeholder="••••••••" required
                                    inputClass="w-full pl-10 py-3 rounded-xl! border-surface-300! dark:border-surface-700! focus:border-primary-500! focus:ring-4! focus:ring-primary-100! dark:focus:ring-primary-900/30! transition-all duration-300"
                                    class="w-full [&>input]:w-full" />
                            </IconField>
                        </div>
                        <small v-if="form.errors.password_confirmation"
                            class="text-red-500 text-xs mt-1 animate-shake">{{
                                form.errors.password_confirmation }}</small>
                    </div>

                    <!-- Submit Button -->
                    <Button type="submit"
                        class="w-full py-3.5 mt-4 rounded-xl text-lg font-bold shadow-lg shadow-primary-500/20 hover:shadow-primary-500/40 hover:-translate-y-0.5 active:translate-y-0 active:shadow-md transition-all duration-300 flex justify-center gap-2 bg-linear-to-r from-primary-600 to-primary-500 border-none"
                        :loading="loading" label="Reset Password" iconPos="right">
                        <template #icon>
                            <font-awesome-icon :icon="faArrowRight" class="animate-pulse-slow" />
                        </template>
                    </Button>
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
