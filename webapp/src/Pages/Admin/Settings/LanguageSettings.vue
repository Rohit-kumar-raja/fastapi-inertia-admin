<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faCheck, faGlobe, faClock, faCalendarAlt, faMoneyBillWave } from '@fortawesome/free-solid-svg-icons';
import FloatLabel from 'primevue/floatlabel';
import Select from 'primevue/select';
import { useToast } from 'primevue';
import axios from 'axios';

const props = defineProps<{
    company?: any;
}>();

const toast = useToast();
const saving = ref(false);

const selectedLanguage = ref('en');
const selectedTimezone = ref('Asia/Kolkata');
const selectedDateFormat = ref('DD/MM/YYYY');
const selectedCurrency = ref('INR');

// Sync from company data 
watchEffect(() => {
    if (props.company) {
        selectedLanguage.value = props.company.language || 'en';
        selectedTimezone.value = props.company.timezone || 'Asia/Kolkata';
        selectedDateFormat.value = props.company.date_format || 'DD/MM/YYYY';
        selectedCurrency.value = props.company.currency || 'INR';
    }
});

const languages = [
    { code: 'en', name: 'English', native: 'English', flag: '🇺🇸' },
    { code: 'es', name: 'Spanish', native: 'Español', flag: '🇪🇸' },
    { code: 'fr', name: 'French', native: 'Français', flag: '🇫🇷' },
    { code: 'de', name: 'German', native: 'Deutsch', flag: '🇩🇪' },
    { code: 'ja', name: 'Japanese', native: '日本語', flag: '🇯🇵' },
    { code: 'zh', name: 'Chinese', native: '中文', flag: '🇨🇳' },
    { code: 'hi', name: 'Hindi', native: 'हिन्दी', flag: '🇮🇳' },
    { code: 'ar', name: 'Arabic', native: 'العربية', flag: '🇸🇦' },
];

const timezones = [
    { value: 'America/New_York', label: 'Eastern Time (ET) — UTC-5' },
    { value: 'America/Chicago', label: 'Central Time (CT) — UTC-6' },
    { value: 'America/Denver', label: 'Mountain Time (MT) — UTC-7' },
    { value: 'America/Los_Angeles', label: 'Pacific Time (PT) — UTC-8' },
    { value: 'Europe/London', label: 'Greenwich Mean Time (GMT) — UTC+0' },
    { value: 'Europe/Paris', label: 'Central European Time (CET) — UTC+1' },
    { value: 'Asia/Kolkata', label: 'India Standard Time (IST) — UTC+5:30' },
    { value: 'Asia/Tokyo', label: 'Japan Standard Time (JST) — UTC+9' },
];

const dateFormats = ['MM/DD/YYYY', 'DD/MM/YYYY', 'YYYY-MM-DD', 'DD.MM.YYYY'];
const currencies = [
    { code: 'USD', symbol: '$', name: 'US Dollar' },
    { code: 'EUR', symbol: '€', name: 'Euro' },
    { code: 'GBP', symbol: '£', name: 'British Pound' },
    { code: 'INR', symbol: '₹', name: 'Indian Rupee' },
    { code: 'JPY', symbol: '¥', name: 'Japanese Yen' },
];

const saveLanguage = async () => {
    saving.value = true;
    try {
        const { data } = await axios.put('/admin/settings/company', {
            language: selectedLanguage.value,
            timezone: selectedTimezone.value,
            date_format: selectedDateFormat.value,
            currency: selectedCurrency.value,
        });
        if (data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Language settings saved', life: 3000 });
        }
    } catch (error: any) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.message || 'Failed to save',
            life: 3000,
        });
    } finally {
        saving.value = false;
    }
};

defineExpose({ saveLanguage });
</script>

<template>
    <div class="space-y-6 animate-fade-in flex flex-col gap-5">
        <!-- Language Selection -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-linear-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white">
                        <font-awesome-icon :icon="faGlobe" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Language</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Choose your preferred language</p>
                    </div>
                </div>
            </div>
            <div class="p-6 pb-8">
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <button v-for="lang in languages" :key="lang.code" @click="selectedLanguage = lang.code"
                        class="relative group flex items-center gap-3 px-4 py-3 rounded-xl border-2 transition-all duration-300 text-left"
                        :class="[
                            selectedLanguage === lang.code
                                ? 'border-indigo-500 bg-indigo-50/50 dark:bg-indigo-500/5 shadow-md shadow-indigo-500/10'
                                : 'border-surface-200 dark:border-surface-700 hover:border-surface-300 dark:hover:border-surface-600 hover:shadow-sm'
                        ]">
                        <span class="text-2xl">{{ lang.flag }}</span>
                        <div class="min-w-0">
                            <p class="text-sm font-semibold text-surface-900 dark:text-white truncate">{{ lang.name }}
                            </p>
                            <p class="text-[11px] text-surface-500 dark:text-surface-400 truncate">{{ lang.native }}</p>
                        </div>
                        <div v-if="selectedLanguage === lang.code"
                            class="absolute top-2 right-2 w-4 h-4 rounded-full bg-indigo-600 flex items-center justify-center">
                            <font-awesome-icon :icon="faCheck" class="text-white text-[8px]" />
                        </div>
                    </button>
                </div>
            </div>
        </div>

        <!-- Timezone -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-linear-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white">
                        <font-awesome-icon :icon="faClock" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Timezone</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Set your local timezone for accurate
                            scheduling</p>
                    </div>
                </div>
            </div>
            <div class="p-6 pb-8">
                <FloatLabel variant="on" class="w-full max-w-lg">
                    <Select id="tz-select" v-model="selectedTimezone" :options="timezones" optionLabel="label"
                        optionValue="value" class="w-full" />
                    <label for="tz-select">Timezone</label>
                </FloatLabel>
            </div>
        </div>
        <div class="flex justify-end px-6 mt-9 pb-6">
            <button @click="saveLanguage" :disabled="saving"
                class="inline-flex items-center gap-2 text-sm font-semibold bg-linear-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white px-6 py-2.5 rounded-xl shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:shadow-indigo-500/40 hover:-translate-y-0.5 disabled:opacity-50">
                Save Language Settings
            </button>
        </div>
        <!-- Date & Number Format -->

    </div>
</template>
