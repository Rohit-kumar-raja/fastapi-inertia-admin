<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUser, faShieldAlt, faPalette, faBell, faGlobe, faCog, faBuilding, faSliders } from '@fortawesome/free-solid-svg-icons';
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

const activeTab = ref('profile');

const newTabs = [
    { id: 'profile', label: 'Profile', icon: faUser },
    { id: 'company', label: 'Company', icon: faBuilding },
    { id: 'account', label: 'Security', icon: faShieldAlt },
    { id: 'appearance', label: 'Appearance', icon: faPalette },
    { id: 'notifications', label: 'Notifications', icon: faBell },
    { id: 'language', label: 'Language', icon: faGlobe },
    { id: 'appsettings', label: 'App Settings', icon: faSliders },
];
</script>

<template>
    <div class="flex flex-col gap-6 bg-white dark:bg-surface-900 ">
        <!-- ═══════════ Page Header ═══════════ -->
        <div class="flex items-center gap-3 px-5 py-2">
            <div
                class="w-10 h-10 rounded-xl bg-linear-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25">
                <font-awesome-icon :icon="faCog" class="text-base" />
            </div>
            <div>
                <h1 class="text-xl font-bold text-surface-900 dark:text-white">Settings</h1>
                <p class="text-xs text-surface-500 dark:text-surface-400">Manage your account and preferences</p>
            </div>
        </div>

        <!-- ═══════════ Horizontal Tabs ═══════════ -->
        <div
            class="sticky top-0 z-20 rounded-2xl border border-surface-200 dark:border-surface-700 bg-white/95 dark:bg-surface-900/95 backdrop-blur-md shadow-sm overflow-hidden">
            <nav class="flex overflow-x-auto scrollbar-none">
                <button v-for="ntab in newTabs" :key="ntab.id" @click="activeTab = ntab.id"
                    class="relative flex items-center gap-2 px-5 py-3.5 text-sm font-medium whitespace-nowrap transition-all duration-200 border-b-2"
                    :class="[
                        activeTab === ntab.id
                            ? 'text-indigo-600 dark:text-indigo-400 border-indigo-600 dark:border-indigo-400 bg-indigo-50/50 dark:bg-indigo-500/5'
                            : 'text-surface-500 dark:text-surface-400 border-transparent hover:text-surface-700 dark:hover:text-surface-300 hover:bg-surface-50 dark:hover:bg-surface-800/50'
                    ]">
                    <font-awesome-icon :icon="ntab.icon" class="text-xs" />
                    {{ ntab.label }}
                </button>
            </nav>
        </div>

        <!-- ═══════════ Content Area ═══════════ -->
        <Transition name="settings-fade" mode="out-in">
            <ProfileSettings v-if="activeTab === 'profile'" key="profile" :user="user" />
            <CompanySettings v-else-if="activeTab === 'company'" key="company" :company="company" />
            <AccountSettings v-else-if="activeTab === 'account'" key="account" />
            <AppearanceSettings v-else-if="activeTab === 'appearance'" key="appearance" :app-settings="appSettings" />
            <NotificationSettings v-else-if="activeTab === 'notifications'" key="notifications"
                :app-settings="appSettings" />
            <LanguageSettings v-else-if="activeTab === 'language'" key="language" :company="company" />
            <AppSettings v-else-if="activeTab === 'appsettings'" key="appsettings" :app-settings="appSettings" />
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
