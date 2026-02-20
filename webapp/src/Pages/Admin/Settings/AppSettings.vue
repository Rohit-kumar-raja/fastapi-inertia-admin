<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faRocket, faShieldAlt, faEnvelope, faBell,
    faHdd, faBriefcase, faDatabase, faClipboardList, faWrench
} from '@fortawesome/free-solid-svg-icons';
import SettingsSection from './AppSettings/SettingsSection.vue';
import type { SettingsConfig } from './AppSettings/SettingsSection.vue';
import CustomSettings from './AppSettings/CustomSettings.vue';
import { useToast } from 'primevue';
import axios from 'axios';

const props = defineProps<{
    appSettings?: any[];
}>();

const toast = useToast();
const saving = ref(false);
const activeCategory = ref('core');

// ─── Category tabs ───
const categories = [
    { id: 'core', label: 'Core', icon: faRocket, color: 'from-indigo-500 to-blue-600' },
    { id: 'auth', label: 'Auth & Security', icon: faShieldAlt, color: 'from-red-500 to-rose-600' },
    { id: 'email', label: 'Email', icon: faEnvelope, color: 'from-emerald-500 to-teal-600' },
    { id: 'notification', label: 'Notifications', icon: faBell, color: 'from-yellow-500 to-amber-600' },
    { id: 'storage', label: 'Storage', icon: faHdd, color: 'from-cyan-500 to-blue-600' },
    { id: 'business', label: 'Business Rules', icon: faBriefcase, color: 'from-lime-500 to-green-600' },
    { id: 'backup', label: 'Backup', icon: faDatabase, color: 'from-teal-500 to-emerald-600' },
    { id: 'audit', label: 'Audit', icon: faClipboardList, color: 'from-orange-500 to-red-600' },
    { id: 'custom', label: 'Custom', icon: faWrench, color: 'from-gray-500 to-slate-600' },
];

// ─── Category configs ───
const configs: Record<string, SettingsConfig> = {
    core: {
        title: 'Core Application Settings',
        description: 'Basic application identity and defaults',
        icon: faRocket,
        color: 'from-indigo-500 to-blue-600',
        sections: [
            {
                title: 'Application Identity', fields: [
                    { key: 'app_name', label: 'Application Name', type: 'text', placeholder: 'My App' },
                    { key: 'app_short_name', label: 'Short Name', type: 'text', placeholder: 'App' },
                    { key: 'app_logo_light', label: 'Logo (Light)', type: 'text', placeholder: 'https://...' },
                    { key: 'app_logo_dark', label: 'Logo (Dark)', type: 'text', placeholder: 'https://...' },
                    { key: 'app_favicon', label: 'Favicon URL', type: 'text', placeholder: 'https://...' },
                ]
            },
            {
                title: 'Locale & Formatting', fields: [
                    { key: 'default_language', label: 'Default Language', type: 'select', options: [{ label: 'English', value: 'en' }, { label: 'Hindi', value: 'hi' }, { label: 'Spanish', value: 'es' }, { label: 'French', value: 'fr' }] },
                    { key: 'supported_languages', label: 'Supported Languages', type: 'text', placeholder: 'en,hi,es,fr' },
                    { key: 'default_timezone', label: 'Default Timezone', type: 'select', options: [{ label: 'Asia/Kolkata (IST)', value: 'Asia/Kolkata' }, { label: 'America/New_York (ET)', value: 'America/New_York' }, { label: 'Europe/London (GMT)', value: 'Europe/London' }, { label: 'Asia/Tokyo (JST)', value: 'Asia/Tokyo' }] },
                    { key: 'date_time_format', label: 'Date/Time Format', type: 'select', options: [{ label: 'DD/MM/YYYY', value: 'DD/MM/YYYY' }, { label: 'MM/DD/YYYY', value: 'MM/DD/YYYY' }, { label: 'YYYY-MM-DD', value: 'YYYY-MM-DD' }] },
                    { key: 'currency_format', label: 'Currency', type: 'select', options: [{ label: '₹ INR', value: 'INR' }, { label: '$ USD', value: 'USD' }, { label: '€ EUR', value: 'EUR' }, { label: '£ GBP', value: 'GBP' }] },
                    { key: 'number_format', label: 'Number Format', type: 'select', options: [{ label: '1,00,000.00 (Indian)', value: 'indian' }, { label: '1,000,000.00 (International)', value: 'international' }] },
                ]
            }
        ]
    },
    auth: {
        title: 'Authentication & Security',
        description: 'Login, passwords, sessions, and tokens',
        icon: faShieldAlt,
        color: 'from-red-500 to-rose-600',
        sections: [{
            title: 'Authentication & Security', fields: [
                { key: 'enable_registration', label: 'Enable Registration', type: 'toggle' },
                { key: 'login_method', label: 'Login Method', type: 'select', options: [{ label: 'Email', value: 'email' }, { label: 'Username', value: 'username' }, { label: 'Mobile', value: 'mobile' }, { label: 'OAuth', value: 'oauth' }] },
                { key: 'password_min_length', label: 'Password Min Length', type: 'number', placeholder: '8' },
                { key: 'session_timeout', label: 'Session Timeout (minutes)', type: 'number', placeholder: '30' },
                { key: 'enable_totp', label: 'Enable 2FA (TOTP)', type: 'toggle' },
                { key: 'access_token_expiry', label: 'Access Token Expiry (minutes)', type: 'number', placeholder: '15' },
                { key: 'refresh_token_expiry', label: 'Refresh Token Expiry (days)', type: 'number', placeholder: '7' },
                { key: 'enable_csrf', label: 'CSRF Protection', type: 'toggle' },
            ]
        }]
    },
    email: {
        title: 'Email Configuration',
        description: 'Outgoing mail server and sender settings',
        icon: faEnvelope,
        color: 'from-emerald-500 to-teal-600',
        sections: [{
            title: 'Mail Server', fields: [
                { key: 'mail_driver', label: 'Mail Driver', type: 'select', options: [{ label: 'SMTP', value: 'smtp' }, { label: 'Amazon SES', value: 'ses' }, { label: 'Mailgun', value: 'mailgun' }, { label: 'SendGrid', value: 'sendgrid' }] },
                { key: 'smtp_host', label: 'SMTP Host', type: 'text', placeholder: 'smtp.gmail.com' },
                { key: 'smtp_port', label: 'SMTP Port', type: 'number', placeholder: '587' },
                { key: 'smtp_encryption', label: 'Encryption', type: 'select', options: [{ label: 'TLS', value: 'tls' }, { label: 'SSL', value: 'ssl' }, { label: 'None', value: 'none' }] },
                { key: 'smtp_username', label: 'SMTP Username', type: 'text' },
                { key: 'smtp_password', label: 'SMTP Password', type: 'password' },
                { key: 'mail_sender_name', label: 'Sender Name', type: 'text', placeholder: 'My App' },
                { key: 'mail_sender_email', label: 'Sender Email', type: 'text', placeholder: 'noreply@myapp.com' },
            ]
        }]
    },
    notification: {
        title: 'Notification Settings',
        description: 'Configure notification channels and behavior',
        icon: faBell,
        color: 'from-yellow-500 to-amber-600',
        sections: [{
            title: 'Notification Channels', fields: [
                { key: 'enable_email_notifications', label: 'Email Notifications', type: 'toggle' },
                { key: 'sms_provider', label: 'SMS Provider', type: 'select', options: [{ label: 'None', value: 'none' }, { label: 'Twilio', value: 'twilio' }, { label: 'MSG91', value: 'msg91' }] },
                { key: 'push_notification_provider', label: 'Push Provider', type: 'select', options: [{ label: 'None', value: 'none' }, { label: 'Firebase', value: 'firebase' }, { label: 'OneSignal', value: 'onesignal' }] },
                { key: 'enable_websocket', label: 'WebSocket Real-time', type: 'toggle' },
                { key: 'notification_retention_days', label: 'Retention Period (days)', type: 'number', placeholder: '30' },
            ]
        }]
    },
    storage: {
        title: 'Storage & File Management',
        description: 'File upload and storage configuration',
        icon: faHdd,
        color: 'from-cyan-500 to-blue-600',
        sections: [{
            title: 'Storage Configuration', fields: [
                { key: 'storage_driver', label: 'Storage Driver', type: 'select', options: [{ label: 'Local', value: 'local' }, { label: 'Amazon S3', value: 's3' }, { label: 'MinIO', value: 'minio' }, { label: 'Google Cloud', value: 'gcs' }] },
                { key: 'max_upload_size', label: 'Max Upload Size (MB)', type: 'number', placeholder: '10' },
                { key: 'allowed_file_types', label: 'Allowed File Types', type: 'text', placeholder: 'jpg,png,pdf,docx' },
                { key: 'public_storage', label: 'Public Storage', type: 'toggle' },
                { key: 'cdn_base_url', label: 'CDN Base URL', type: 'text', placeholder: 'https://cdn.myapp.com' },
            ]
        }]
    },
    business: {
        title: 'Business Rules',
        description: 'Tax, invoicing, and operational settings',
        icon: faBriefcase,
        color: 'from-lime-500 to-green-600',
        sections: [{
            title: 'Business Configuration', fields: [
                { key: 'tax_percentage', label: 'Tax Percentage (%)', type: 'number', placeholder: '18' },
                { key: 'discount_rules', label: 'Discount Rules (JSON)', type: 'textarea', placeholder: '{"bulk_10": 5, "bulk_50": 10}' },
                { key: 'invoice_format', label: 'Invoice Number Format', type: 'text', placeholder: 'INV-{YEAR}-{SEQ}' },
                { key: 'order_auto_expiry', label: 'Order Auto-Expiry (hours)', type: 'number', placeholder: '48' },
                { key: 'sla_timing', label: 'SLA Timing (hours)', type: 'number', placeholder: '24' },
            ]
        }]
    },
    backup: {
        title: 'Backup & Maintenance',
        description: 'Automated backup and maintenance mode',
        icon: faDatabase,
        color: 'from-teal-500 to-emerald-600',
        sections: [{
            title: 'Backup Configuration', fields: [
                { key: 'enable_auto_backup', label: 'Auto Backup', type: 'toggle' },
                { key: 'backup_frequency', label: 'Backup Frequency', type: 'select', options: [{ label: 'Hourly', value: 'hourly' }, { label: 'Daily', value: 'daily' }, { label: 'Weekly', value: 'weekly' }, { label: 'Monthly', value: 'monthly' }] },
                { key: 'backup_retention_days', label: 'Backup Retention (days)', type: 'number', placeholder: '30' },
                { key: 'maintenance_mode', label: 'Maintenance Mode', type: 'toggle' },
                { key: 'maintenance_message', label: 'Maintenance Message', type: 'textarea', placeholder: 'We are currently under maintenance...' },
            ]
        }]
    },
    audit: {
        title: 'Audit & Compliance',
        description: 'Activity logging, data retention, and GDPR',
        icon: faClipboardList,
        color: 'from-orange-500 to-red-600',
        sections: [{
            title: 'Audit Configuration', fields: [
                { key: 'enable_activity_logs', label: 'Activity Logs', type: 'toggle' },
                { key: 'data_retention_days', label: 'Data Retention (days)', type: 'number', placeholder: '365' },
                { key: 'gdpr_deletion_window', label: 'GDPR Deletion Window (days)', type: 'number', placeholder: '30' },
                { key: 'enable_data_export', label: 'User Data Export', type: 'toggle' },
            ]
        }]
    },
};

// ─── Settings state ───
const settingsMap = ref<Record<string, string>>({});

watchEffect(() => {
    if (props.appSettings) {
        const map: Record<string, string> = {};
        for (const s of props.appSettings) {
            map[s.key] = s.value;
        }
        settingsMap.value = { ...settingsMap.value, ...map };
    }
});

const handleValueUpdate = (key: string, value: string) => {
    settingsMap.value[key] = value;
};

const saveCategory = async () => {
    const config = configs[activeCategory.value];
    if (!config) return;

    saving.value = true;
    const settings: { key: string; value: string; group: string }[] = [];
    for (const section of config.sections) {
        for (const field of section.fields) {
            const val = settingsMap.value[field.key];
            if (val !== undefined && val !== '') {
                settings.push({ key: field.key, value: val, group: activeCategory.value });
            }
        }
    }

    try {
        await axios.put('/admin/settings/app/bulk', { settings });
        toast.add({ severity: 'success', summary: 'Saved', detail: `${config.title} settings saved`, life: 3000 });
    } catch (error: any) {
        toast.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.message || 'Failed to save', life: 3000 });
    } finally {
        saving.value = false;
    }
};

const currentConfig = computed(() => configs[activeCategory.value]);
</script>

<template>
    <div class="space-y-5 animate-fade-in">
        <!-- Category Tabs -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white/95 dark:bg-surface-900/95 backdrop-blur-md shadow-sm overflow-hidden">
            <nav class="flex overflow-x-auto scrollbar-none">
                <button v-for="cat in categories" :key="cat.id" @click="activeCategory = cat.id"
                    class="relative flex items-center gap-1.5 px-3.5 py-3 text-xs font-medium whitespace-nowrap transition-all duration-200 border-b-2"
                    :class="[
                        activeCategory === cat.id
                            ? 'text-indigo-600 dark:text-indigo-400 border-indigo-600 dark:border-indigo-400 bg-indigo-50/50 dark:bg-indigo-500/5'
                            : 'text-surface-500 dark:text-surface-400 border-transparent hover:text-surface-700 dark:hover:text-surface-300 hover:bg-surface-50 dark:hover:bg-surface-800/50'
                    ]">
                    <font-awesome-icon :icon="cat.icon" class="text-[10px]" />
                    {{ cat.label }}
                </button>
            </nav>
        </div>

        <!-- Content -->
        <Transition name="settings-fade" mode="out-in">
            <CustomSettings v-if="activeCategory === 'custom'" key="custom" />
            <SettingsSection v-else-if="currentConfig" :key="activeCategory" :config="currentConfig"
                :settings-map="settingsMap" :saving="saving" @update:value="handleValueUpdate" @save="saveCategory" />
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
    animation: settingsFadeIn 0.25s ease-out;
}

.settings-fade-leave-active {
    animation: settingsFadeOut 0.12s ease-in;
}

@keyframes settingsFadeIn {
    from {
        opacity: 0;
        transform: translateY(4px);
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
