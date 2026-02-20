<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faBell, faEnvelope, faMobileAlt, faShoppingCart,
    faUserPlus, faExclamationCircle, faBullhorn, faChartLine
} from '@fortawesome/free-solid-svg-icons';
import FloatLabel from 'primevue/floatlabel';

defineProps<{
    appSettings?: any[];
}>();

interface NotificationChannel {
    id: string;
    label: string;
    description: string;
    icon: any;
    color: string;
    email: boolean;
    push: boolean;
    sms: boolean;
}

const channels = ref<NotificationChannel[]>([
    { id: 'orders', label: 'Orders', description: 'New orders, cancellations, and refunds', icon: faShoppingCart, color: 'from-indigo-500 to-indigo-600', email: true, push: true, sms: false },
    { id: 'users', label: 'New Users', description: 'Account registrations and verifications', icon: faUserPlus, color: 'from-emerald-500 to-emerald-600', email: true, push: false, sms: false },
    { id: 'alerts', label: 'System Alerts', description: 'Downtime, errors, and security alerts', icon: faExclamationCircle, color: 'from-rose-500 to-red-600', email: true, push: true, sms: true },
    { id: 'marketing', label: 'Marketing', description: 'Campaign updates and analytics reports', icon: faBullhorn, color: 'from-amber-500 to-orange-500', email: true, push: false, sms: false },
    { id: 'reports', label: 'Reports', description: 'Weekly and monthly summary reports', icon: faChartLine, color: 'from-cyan-500 to-blue-500', email: true, push: false, sms: false },
]);

const quietHoursEnabled = ref(false);
const quietHoursStart = ref('22:00');
const quietHoursEnd = ref('07:00');
const soundEnabled = ref(true);
const badgeEnabled = ref(true);
</script>

<template>
    <div class="space-y-8 animate-fade-in">
        <!-- Notification Channels -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center justify-between">
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Notification Channels</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400 mt-0.5">Choose how you want to be
                            notified for each type</p>
                    </div>
                    <div
                        class="hidden sm:flex items-center gap-6 text-[10px] font-bold text-surface-500 dark:text-surface-400 uppercase tracking-widest">
                        <span class="w-14 text-center flex items-center gap-1 justify-center">
                            <font-awesome-icon :icon="faEnvelope" class="text-surface-400" />
                            Email
                        </span>
                        <span class="w-14 text-center flex items-center gap-1 justify-center">
                            <font-awesome-icon :icon="faBell" class="text-surface-400" />
                            Push
                        </span>
                        <span class="w-14 text-center flex items-center gap-1 justify-center">
                            <font-awesome-icon :icon="faMobileAlt" class="text-surface-400" />
                            SMS
                        </span>
                    </div>
                </div>
            </div>
            <div class="divide-y divide-surface-100 dark:divide-surface-800">
                <div v-for="channel in channels" :key="channel.id"
                    class="px-6 py-4 flex items-center justify-between hover:bg-surface-50/50 dark:hover:bg-surface-800/30 transition-colors">
                    <div class="flex items-center gap-4">
                        <div class="w-10 h-10 rounded-xl bg-gradient-to-br flex items-center justify-center text-white shadow-md"
                            :class="channel.color">
                            <font-awesome-icon :icon="channel.icon" class="text-sm" />
                        </div>
                        <div>
                            <p class="text-sm font-semibold text-surface-900 dark:text-white">{{ channel.label }}</p>
                            <p class="text-xs text-surface-500 dark:text-surface-400 mt-0.5 hidden sm:block">{{
                                channel.description }}</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-6">
                        <!-- Email Toggle -->
                        <label class="relative inline-flex items-center cursor-pointer w-14 justify-center">
                            <input type="checkbox" v-model="channel.email" class="sr-only peer" />
                            <div
                                class="w-9 h-5 bg-surface-200 dark:bg-surface-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[calc(50%-18px+2px)] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-indigo-600 after:shadow-sm">
                            </div>
                        </label>
                        <!-- Push Toggle -->
                        <label class="relative inline-flex items-center cursor-pointer w-14 justify-center">
                            <input type="checkbox" v-model="channel.push" class="sr-only peer" />
                            <div
                                class="w-9 h-5 bg-surface-200 dark:bg-surface-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[calc(50%-18px+2px)] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-indigo-600 after:shadow-sm">
                            </div>
                        </label>
                        <!-- SMS Toggle -->
                        <label class="relative inline-flex items-center cursor-pointer w-14 justify-center">
                            <input type="checkbox" v-model="channel.sms" class="sr-only peer" />
                            <div
                                class="w-9 h-5 bg-surface-200 dark:bg-surface-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[calc(50%-18px+2px)] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-indigo-600 after:shadow-sm">
                            </div>
                        </label>
                    </div>
                </div>
            </div>
        </div>

        <!-- Quick Preferences -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Sound -->
            <div
                class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-5 flex items-center justify-between hover:shadow-md transition-shadow">
                <div class="flex items-center gap-3">
                    <div
                        class="w-10 h-10 rounded-xl bg-violet-50 dark:bg-violet-500/10 flex items-center justify-center text-violet-600 dark:text-violet-400">
                        🔔
                    </div>
                    <div>
                        <p class="text-sm font-semibold text-surface-900 dark:text-white">Sound</p>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Play sound for notifications</p>
                    </div>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="soundEnabled" class="sr-only peer" />
                    <div
                        class="w-11 h-6 bg-surface-200 dark:bg-surface-700 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600 after:shadow-sm">
                    </div>
                </label>
            </div>

            <!-- Badge Count -->
            <div
                class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 p-5 flex items-center justify-between hover:shadow-md transition-shadow">
                <div class="flex items-center gap-3">
                    <div
                        class="w-10 h-10 rounded-xl bg-rose-50 dark:bg-rose-500/10 flex items-center justify-center text-rose-600 dark:text-rose-400">
                        🔴
                    </div>
                    <div>
                        <p class="text-sm font-semibold text-surface-900 dark:text-white">Badge Count</p>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Show unread count badges</p>
                    </div>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="badgeEnabled" class="sr-only peer" />
                    <div
                        class="w-11 h-6 bg-surface-200 dark:bg-surface-700 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600 after:shadow-sm">
                    </div>
                </label>
            </div>
        </div>

        <!-- Quiet Hours -->
        <div
            class="h-full rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center justify-between">
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">🌙 Quiet Hours</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400 mt-0.5">Pause notifications during
                            specific hours</p>
                    </div>
                    <label class="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" v-model="quietHoursEnabled" class="sr-only peer" />
                        <div
                            class="w-11 h-6 bg-surface-200 dark:bg-surface-700 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600 after:shadow-sm">
                        </div>
                    </label>
                </div>
            </div>
            <div v-if="quietHoursEnabled" class="p-6">
                <div class="flex items-end gap-4 max-w-sm">
                    <div class="flex-1">
                        <FloatLabel variant="on">
                            <InputText id="quiet-start" v-model="quietHoursStart" type="time" class="w-full" />
                            <label for="quiet-start">From</label>
                        </FloatLabel>
                    </div>
                    <span class="text-surface-400 font-medium pb-2">to</span>
                    <div class="flex-1">
                        <FloatLabel variant="on">
                            <InputText id="quiet-end" v-model="quietHoursEnd" type="time" class="w-full" />
                            <label for="quiet-end">Until</label>
                        </FloatLabel>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
