<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUser, faShieldAlt, faPalette, faBell, faGlobe, faCog, faBuilding } from '@fortawesome/free-solid-svg-icons';
import ProfileSettings from './ProfileSettings.vue';
import AccountSettings from './AccountSettings.vue';
import AppearanceSettings from './AppearanceSettings.vue';
import NotificationSettings from './NotificationSettings.vue';
import LanguageSettings from './LanguageSettings.vue';
import CompanySettings from './CompanySettings.vue';
import { usePage } from '@inertiajs/vue3';

const page = usePage();
const user = computed(() => (page.props as any).user || null);
const company = computed(() => (page.props as any).company || null);
const appSettings = computed(() => (page.props as any).app_settings || []);

const activeTab = ref('profile');
const profileRef = ref<InstanceType<typeof ProfileSettings> | null>(null);
const accountRef = ref<InstanceType<typeof AccountSettings> | null>(null);
const companyRef = ref<InstanceType<typeof CompanySettings> | null>(null);
const languageRef = ref<InstanceType<typeof LanguageSettings> | null>(null);

const newTabs = [
    { id: 'profile', label: 'Profile', icon: faUser },
    { id: 'company', label: 'Company', icon: faBuilding },
    { id: 'account', label: 'Security', icon: faShieldAlt },
    { id: 'appearance', label: 'Appearance', icon: faPalette },
    { id: 'notifications', label: 'Notifications', icon: faBell },
    { id: 'language', label: 'Language', icon: faGlobe },
];

const savableTabs = ['profile', 'account', 'company', 'language'];

const handleSave = () => {
    if (activeTab.value === 'profile' && profileRef.value) {
        profileRef.value.saveProfile();
    } else if (activeTab.value === 'account' && accountRef.value) {
        accountRef.value.saveProfile();
    } else if (activeTab.value === 'company' && companyRef.value) {
        companyRef.value.saveCompany();
    } else if (activeTab.value === 'language' && languageRef.value) {
        languageRef.value.saveLanguage();
    }
};
</script>

<template>
    <div class="flex flex-col gap-6 bg-white dark:bg-surface-900">
        <!-- ═══════════ Page Header ═══════════ -->
        <div class="flex items-center justify-between">
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
            <button v-if="savableTabs.includes(activeTab)" @click="handleSave"
                class="inline-flex items-center gap-2 text-sm font-semibold bg-linear-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white px-5 py-2.5 rounded-xl shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:shadow-indigo-500/40 hover:-translate-y-0.5">
                Save Changes
            </button>
        </div>

        <!-- ═══════════ Horizontal Tabs ═══════════ -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 shadow-sm overflow-hidden">
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
            <ProfileSettings v-if="activeTab === 'profile'" key="profile" ref="profileRef" :user="user" />
            <CompanySettings v-else-if="activeTab === 'company'" key="company" ref="companyRef" :company="company" />
            <AccountSettings v-else-if="activeTab === 'account'" key="account" ref="accountRef" />
            <AppearanceSettings v-else-if="activeTab === 'appearance'" key="appearance" :app-settings="appSettings" />
            <NotificationSettings v-else-if="activeTab === 'notifications'" key="notifications"
                :app-settings="appSettings" />
            <LanguageSettings v-else-if="activeTab === 'language'" key="language" ref="languageRef"
                :company="company" />
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
