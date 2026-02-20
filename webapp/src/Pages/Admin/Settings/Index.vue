<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faUser, faShieldAlt, faPalette, faBell, faGlobe, faCog,
    faBuilding, faSliders, faDesktop, faRocket
} from '@fortawesome/free-solid-svg-icons';
import ProfileSettings from './ProfileSettings.vue';
import AccountSettings from './AccountSettings.vue';
import AppearanceSettings from './AppearanceSettings.vue';
import NotificationSettings from './NotificationSettings.vue';
import LanguageSettings from './LanguageSettings.vue';
import CompanySettings from './CompanySettings.vue';
import AppSettings from './AppSettings.vue';
import { usePage } from '@inertiajs/vue3';

const page = usePage();
const user = computed(() => (page.props as any).user || null);
const company = computed(() => (page.props as any).company || null);
const appSettings = computed(() => (page.props as any).app_settings || []);

// Top-level tabs
const topTab = ref<'system' | 'app'>('system');

// Sub-tabs per top-level
const systemTab = ref('profile');
const appTab = ref('appsettings');

const systemTabs = [
    { id: 'profile', label: 'Profile', icon: faUser },
    { id: 'company', label: 'Company', icon: faBuilding },
    { id: 'account', label: 'Security', icon: faShieldAlt },
    { id: 'appearance', label: 'Appearance', icon: faPalette },
    { id: 'notifications', label: 'Notifications', icon: faBell },
    { id: 'language', label: 'Language', icon: faGlobe },
];

const topTabs = [
    { id: 'system', label: 'System', icon: faDesktop },
    { id: 'app', label: 'Application', icon: faRocket },
];
</script>

<template>
    <div class="flex flex-col gap-5 bg-white dark:bg-surface-900 h-full">
        <!-- ═══════════ Page Header ═══════════ -->
        <div class="flex items-center justify-between px-5 py-2">
            <div class="flex items-center gap-3">
                <div
                    class="w-10 h-10 rounded-xl bg-linear-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25">
                    <font-awesome-icon :icon="faCog" class="text-base" />
                </div>
                <div>
                    <h1 class="text-xl font-bold text-surface-900 dark:text-white">Settings</h1>
                    <p class="text-xs text-surface-500 dark:text-surface-400">Manage your account and preferences</p>
                </div>
            </div>

            <!-- Top-Level Tabs (System / App) -->
            <div class="flex items-center gap-1 bg-surface-100 dark:bg-surface-800 rounded-xl p-1">
                <button v-for="t in topTabs" :key="t.id" @click="topTab = t.id as 'system' | 'app'"
                    class="flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg transition-all duration-200"
                    :class="[
                        topTab === t.id
                            ? 'bg-white dark:bg-surface-700 text-indigo-600 dark:text-indigo-400 shadow-sm'
                            : 'text-surface-500 dark:text-surface-400 hover:text-surface-700 dark:hover:text-surface-300'
                    ]">
                    <font-awesome-icon :icon="t.icon" class="text-[10px]" />
                    {{ t.label }}
                </button>
            </div>
        </div>

        <!-- ═══════════ Sub Tabs ═══════════ -->
        <Transition name="settings-fade" mode="out-in">
            <!-- SYSTEM MODE -->
            <div v-if="topTab === 'system'" key="system" class="flex flex-col gap-5">
                <div
                    class="sticky top-0 z-20 rounded-2xl border border-surface-200 dark:border-surface-700 bg-white/95 dark:bg-surface-900/95 backdrop-blur-md shadow-sm overflow-hidden">
                    <nav class="flex overflow-x-auto scrollbar-none">
                        <button v-for="ntab in systemTabs" :key="ntab.id" @click="systemTab = ntab.id"
                            class="relative flex items-center gap-2 px-5 py-3.5 text-sm font-medium whitespace-nowrap transition-all duration-200 border-b-2"
                            :class="[
                                systemTab === ntab.id
                                    ? 'text-indigo-600 dark:text-indigo-400 border-indigo-600 dark:border-indigo-400 bg-indigo-50/50 dark:bg-indigo-500/5'
                                    : 'text-surface-500 dark:text-surface-400 border-transparent hover:text-surface-700 dark:hover:text-surface-300 hover:bg-surface-50 dark:hover:bg-surface-800/50'
                            ]">
                            <font-awesome-icon :icon="ntab.icon" class="text-xs" />
                            {{ ntab.label }}
                        </button>
                    </nav>
                </div>

                <Transition name="settings-fade" mode="out-in">
                    <ProfileSettings v-if="systemTab === 'profile'" key="profile" :user="user" />
                    <CompanySettings v-else-if="systemTab === 'company'" key="company" :company="company" />
                    <AccountSettings v-else-if="systemTab === 'account'" key="account" />
                    <AppearanceSettings v-else-if="systemTab === 'appearance'" key="appearance"
                        :app-settings="appSettings" />
                    <NotificationSettings v-else-if="systemTab === 'notifications'" key="notifications"
                        :app-settings="appSettings" />
                    <LanguageSettings v-else-if="systemTab === 'language'" key="language" :company="company" />
                </Transition>
            </div>

            <!-- APP MODE -->
            <div v-else key="app" class="flex flex-col gap-5">
                <AppSettings :app-settings="appSettings" />
            </div>
        </Transition>
    </div>
</template>

<style scoped>
.scrollbar-none::-webkit-scrollbar {
    display: none;
}

.scrollbar-none {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.settings-fade-enter-active {
    animation: settingsFadeIn 0.3s ease-out;
}

.settings-fade-leave-active {
    animation: settingsFadeOut 0.15s ease-in;
}

@keyframes settingsFadeIn {
    from {
        opacity: 0;
        transform: translateY(6px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes settingsFadeOut {
    from {
        opacity: 1;
    }

    to {
        opacity: 0;
    }
}
</style>
