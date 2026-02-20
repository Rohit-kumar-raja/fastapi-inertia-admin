<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faShieldAlt, faFingerprint, faMobileAlt,
    faHistory, faSignOutAlt, faExclamationTriangle, faCheck,
    faDesktop, faGlobe
} from '@fortawesome/free-solid-svg-icons';

const twoFactorEnabled = ref(false);

const sessions = ref([
    { device: 'MacBook Pro — Chrome', location: 'San Francisco, US', ip: '192.168.1.1', lastActive: 'Active now', current: true, icon: faDesktop },
    { device: 'iPhone 15 — Safari', location: 'San Francisco, US', ip: '192.168.1.2', lastActive: '2 hours ago', current: false, icon: faMobileAlt },
    { device: 'Windows PC — Firefox', location: 'New York, US', ip: '10.0.0.5', lastActive: '3 days ago', current: false, icon: faGlobe },
]);
</script>

<template>
    <div class="space-y-8 animate-fade-in flex flex-col gap-5">
        <!-- Two-Factor Authentication -->
        <div
            class="relative overflow-hidden rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900">
            <div
                class="absolute top-0 right-0 w-40 h-40 bg-linear-to-bl from-indigo-500/5 to-transparent rounded-bl-full">
            </div>
            <div class="p-6 lg:p-8 relative">
                <div class="flex flex-col sm:flex-row items-start gap-5">
                    <div
                        class="w-14 h-14 rounded-2xl bg-linear-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25 shrink-0">
                        <font-awesome-icon :icon="faShieldAlt" class="text-xl" />
                    </div>
                    <div class="flex-1">
                        <div class="flex items-start justify-between">
                            <div>
                                <h3 class="text-base font-bold text-surface-900 dark:text-white">Two-Factor
                                    Authentication</h3>
                                <p class="text-sm text-surface-500 dark:text-surface-400 mt-1 max-w-md">Add an extra
                                    layer of security. When enabled, you'll need to enter a code from your phone in
                                    addition to your password.</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-3 mt-4">
                            <button v-if="!twoFactorEnabled" @click="twoFactorEnabled = true"
                                class="inline-flex items-center gap-2 text-sm font-semibold bg-linear-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white px-5 py-2.5 rounded-xl shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:shadow-indigo-500/40 hover:-translate-y-0.5">
                                <font-awesome-icon :icon="faFingerprint" class="text-sm" />
                                Enable 2FA
                            </button>
                            <div v-else class="flex items-center gap-3">
                                <span
                                    class="inline-flex items-center gap-2 text-sm font-semibold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10 px-4 py-2 rounded-xl border border-emerald-200 dark:border-emerald-500/20">
                                    <font-awesome-icon :icon="faCheck" class="text-xs" />
                                    2FA Enabled
                                </span>
                                <button @click="twoFactorEnabled = false"
                                    class="text-sm font-medium text-surface-500 hover:text-rose-600 transition-colors">
                                    Disable
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Active Sessions -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div
                            class="w-8 h-8 rounded-lg bg-linear-to-br from-cyan-400 to-blue-500 flex items-center justify-center text-white">
                            <font-awesome-icon :icon="faHistory" class="text-xs" />
                        </div>
                        <div>
                            <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Active Sessions</h3>
                            <p class="text-xs text-surface-500 dark:text-surface-400">Manage your logged-in devices</p>
                        </div>
                    </div>
                    <button
                        class="text-xs font-semibold text-rose-600 dark:text-rose-400 hover:text-rose-700 transition-colors flex items-center gap-1.5">
                        <font-awesome-icon :icon="faSignOutAlt" class="text-[10px]" />
                        Sign out all
                    </button>
                </div>
            </div>
            <div class="divide-y divide-surface-100 dark:divide-surface-800">
                <div v-for="(session, idx) in sessions" :key="idx"
                    class="px-6 py-4 flex items-center justify-between hover:bg-surface-50/50 dark:hover:bg-surface-800/30 transition-colors group">
                    <div class="flex items-center gap-4">
                        <div class="w-10 h-10 rounded-xl flex items-center justify-center" :class="[
                            session.current
                                ? 'bg-indigo-50 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400'
                                : 'bg-surface-100 dark:bg-surface-800 text-surface-500 dark:text-surface-400'
                        ]">
                            <font-awesome-icon :icon="session.icon" />
                        </div>
                        <div>
                            <div class="flex items-center gap-2">
                                <p class="text-sm font-semibold text-surface-900 dark:text-white">{{ session.device }}
                                </p>
                                <span v-if="session.current"
                                    class="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10 px-2 py-0.5 rounded-full uppercase tracking-wider">
                                    This device
                                </span>
                            </div>
                            <p class="text-xs text-surface-500 dark:text-surface-400 mt-0.5">{{ session.location }} · {{
                                session.ip }} · {{ session.lastActive }}</p>
                        </div>
                    </div>
                    <button v-if="!session.current"
                        class="text-xs font-medium text-surface-400 hover:text-rose-600 dark:hover:text-rose-400 opacity-0 group-hover:opacity-100 transition-all">
                        Revoke
                    </button>
                </div>
            </div>
        </div>

     
    </div>
</template>
