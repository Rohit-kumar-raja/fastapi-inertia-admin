<script setup lang="ts">
import { ref } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUser, faShieldAlt, faPalette, faBell, faGlobe } from '@fortawesome/free-solid-svg-icons';


const activeTab = ref('profile');

const tabs = [
    { id: 'profile', label: 'Profile', icon: faUser },
    { id: 'account', label: 'Account', icon: faShieldAlt },
    { id: 'appearance', label: 'Appearance', icon: faPalette },
    { id: 'notifications', label: 'Notifications', icon: faBell },
    { id: 'language', label: 'Language & Region', icon: faGlobe },
];

const profileForm = ref({
    fullName: 'Amy Elsner',
    email: 'amy@example.com',
    bio: 'Product Designer based in San Francisco.',
    role: 'Administrator'
});

const themeSettings = ref({
    mode: 'system'
});
</script>

<template>
    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-2xl font-bold text-slate-800 dark:text-white mb-2">Settings</h1>
        <p class="text-slate-500 dark:text-slate-400 mb-8">Manage your account settings and preferences.</p>

        <div class="flex flex-col lg:flex-row gap-8">
            <!-- Sidebar Navigation -->
            <aside class="w-full lg:w-64 shrink-0">
                <nav class="space-y-1">
                    <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
                        class="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200"
                        :class="[
                            activeTab === tab.id
                                ? 'bg-indigo-50 dark:bg-indigo-500/10 text-indigo-700 dark:text-indigo-400 shadow-sm'
                                : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-white/5 hover:text-slate-900 dark:hover:text-slate-200'
                        ]">
                        <font-awesome-icon :icon="tab.icon" class="text-base" :class="[
                            activeTab === tab.id ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-400'
                        ]" />
                        {{ tab.label }}
                    </button>
                </nav>
            </aside>

            <!-- Content Area -->
            <div class="flex-1 min-w-0">
                <div
                    class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">

                    <!-- Profile Section -->
                    <div v-if="activeTab === 'profile'" class="p-6 lg:p-8 space-y-8 animate-fade-in">
                        <div>
                            <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Public Profile</h2>
                            <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">This information will be
                                displayed publicly.</p>
                        </div>

                        <div
                            class="flex flex-col sm:flex-row items-start gap-6 pt-6 border-t border-slate-100 dark:border-slate-800">
                            <!-- Avatar -->
                            <div class="relative group cursor-pointer">
                                <img src="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" alt="Profile"
                                    class="w-24 h-24 rounded-2xl object-cover ring-4 ring-white dark:ring-slate-800 shadow-lg group-hover:opacity-90 transition-opacity" />
                                <div
                                    class="absolute inset-0 flex items-center justify-center bg-black/40 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity">
                                    <span class="text-white text-xs font-medium">Change</span>
                                </div>
                            </div>

                            <!-- Fields -->
                            <div class="flex-1 space-y-5 w-full max-w-xl">
                                <div>
                                    <label
                                        class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Full
                                        Name</label>
                                    <input type="text" v-model="profileForm.fullName"
                                        class="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all" />
                                </div>

                                <div>
                                    <label
                                        class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Bio</label>
                                    <textarea v-model="profileForm.bio" rows="3"
                                        class="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all resize-none"></textarea>
                                    <p class="mt-1.5 text-xs text-slate-400">Brief description for your profile. URLs
                                        are hyperlinked.</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Account Section -->
                    <div v-else-if="activeTab === 'account'" class="p-6 lg:p-8 space-y-8 animate-fade-in">
                        <div>
                            <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Account Security</h2>
                            <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Manage your password and
                                authentication methods.</p>
                        </div>

                        <div
                            class="bg-indigo-50 dark:bg-indigo-500/10 rounded-xl p-4 border border-indigo-100 dark:border-indigo-500/20 flex gap-4">
                            <div
                                class="p-2 bg-indigo-100 dark:bg-indigo-500/20 rounded-lg text-indigo-600 dark:text-indigo-400 shrink-0 h-fit">
                                <font-awesome-icon :icon="faShieldAlt" />
                            </div>
                            <div>
                                <h3 class="text-sm font-semibold text-indigo-900 dark:text-indigo-200">Two-Factor
                                    Authentication</h3>
                                <p class="text-xs text-indigo-700 dark:text-indigo-300/70 mt-1 mb-3">Add an extra layer
                                    of security to your account.</p>
                                <button
                                    class="text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-1.5 rounded-lg transition-colors">
                                    Enable 2FA
                                </button>
                            </div>
                        </div>

                        <div class="pt-6 border-t border-slate-100 dark:border-slate-800">
                            <h3 class="text-sm font-medium text-slate-900 dark:text-white mb-4">Change Password</h3>
                            <div class="grid gap-4 max-w-sm">
                                <input type="password" placeholder="Current Password"
                                    class="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 focus:border-indigo-500 outline-none" />
                                <input type="password" placeholder="New Password"
                                    class="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 focus:border-indigo-500 outline-none" />
                            </div>
                        </div>
                    </div>

                    <!-- Appearance Section -->
                    <div v-else-if="activeTab === 'appearance'" class="p-6 lg:p-8 space-y-8 animate-fade-in">
                        <div>
                            <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Appearance</h2>
                            <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Customize the interface look and
                                feel.</p>
                        </div>

                        <div class="grid grid-cols-3 gap-4">
                            <button @click="themeSettings.mode = 'light'"
                                class="border-2 rounded-xl p-2 hover:border-indigo-500 transition-all text-left group"
                                :class="themeSettings.mode === 'light' ? 'border-indigo-500 ring-2 ring-indigo-500/20 bg-indigo-50/50' : 'border-slate-200 dark:border-slate-700'">
                                <div
                                    class="h-24 bg-slate-100 rounded-lg mb-3 border border-slate-200 relative overflow-hidden">
                                    <div class="absolute inset-y-0 left-0 w-1/4 bg-white border-r border-slate-200">
                                    </div>
                                </div>
                                <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Light</span>
                            </button>
                            <button @click="themeSettings.mode = 'dark'"
                                class="border-2 rounded-xl p-2 hover:border-indigo-500 transition-all text-left group"
                                :class="themeSettings.mode === 'dark' ? 'border-indigo-500 ring-2 ring-indigo-500/20 bg-indigo-50/50' : 'border-slate-200 dark:border-slate-700'">
                                <div
                                    class="h-24 bg-slate-900 rounded-lg mb-3 border border-slate-700 relative overflow-hidden">
                                    <div class="absolute inset-y-0 left-0 w-1/4 bg-slate-800 border-r border-slate-700">
                                    </div>
                                </div>
                                <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Dark</span>
                            </button>
                        </div>
                    </div>

                    <!-- Footer Actions -->
                    <div
                        class="bg-slate-50 dark:bg-slate-800/50 px-6 py-4 border-t border-slate-200 dark:border-slate-800 flex justify-end gap-3">
                        <button
                            class="px-4 py-2 text-sm font-medium text-slate-600 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-700 rounded-lg border border-transparent hover:border-slate-200 dark:hover:border-slate-600 transition-all">Cancel</button>
                        <button
                            class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg shadow-sm shadow-indigo-500/20 transition-all">Save
                            Changes</button>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(4px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
