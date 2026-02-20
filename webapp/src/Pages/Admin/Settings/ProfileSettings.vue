<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faCamera, faMapMarkerAlt, faBriefcase, faLink } from '@fortawesome/free-solid-svg-icons';
import { faGithub, faTwitter, faLinkedin } from '@fortawesome/free-brands-svg-icons';
import FloatLabel from 'primevue/floatlabel';
import Textarea from 'primevue/textarea';
import { useToast } from 'primevue';
import axios from 'axios';

const props = defineProps<{
    user?: any;
}>();

const emit = defineEmits(['save']);
const toast = useToast();
const saving = ref(false);

const profileForm = ref({
    username: '',
    email: '',
    phone: '',
});

// Initialize form from user prop
watchEffect(() => {
    if (props.user) {
        profileForm.value.username = props.user.username || '';
        profileForm.value.email = props.user.email || '';
        profileForm.value.phone = props.user.phone || '';
    }
});

const avatarUrl = ref('https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png');

const saveProfile = async () => {
    saving.value = true;
    try {
        const { data } = await axios.put('/admin/settings/profile', profileForm.value);
        if (data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Profile updated successfully', life: 3000 });
        }
    } catch (error: any) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.response?.data?.message || 'Failed to update profile',
            life: 3000,
        });
    } finally {
        saving.value = false;
    }
};

defineExpose({ saveProfile });
</script>

<template>
    <div class="space-y-8 animate-fade-in">
        <!-- Profile Header Card -->
        <div
            class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-[1px]">
            <div class="rounded-2xl bg-white dark:bg-surface-900 p-6 lg:p-8">
                <div class="flex flex-col sm:flex-row items-start gap-6">
                    <!-- Avatar with upload -->
                    <div class="relative group cursor-pointer shrink-0">
                        <div
                            class="w-28 h-28 rounded-2xl overflow-hidden ring-4 ring-white dark:ring-surface-800 shadow-xl shadow-indigo-500/10">
                            <img :src="avatarUrl" alt="Profile"
                                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                        </div>
                        <div
                            class="absolute inset-0 flex items-center justify-center bg-black/40 rounded-2xl opacity-0 group-hover:opacity-100 transition-all duration-300 backdrop-blur-sm">
                            <div class="flex flex-col items-center gap-1">
                                <font-awesome-icon :icon="faCamera" class="text-white text-lg" />
                                <span class="text-white text-[10px] font-medium tracking-wide uppercase">Change</span>
                            </div>
                        </div>
                        <!-- Online indicator -->
                        <div
                            class="absolute -bottom-1 -right-1 w-5 h-5 bg-emerald-500 rounded-full border-[3px] border-white dark:border-surface-900">
                        </div>
                    </div>

                    <!-- Profile Summary -->
                    <div class="flex-1">
                        <div class="flex items-start justify-between">
                            <div>
                                <h3 class="text-xl font-bold text-surface-900 dark:text-white">{{ profileForm.username
                                }}</h3>
                                <p class="text-sm text-indigo-600 dark:text-indigo-400 font-medium mt-0.5">
                                    Administrator</p>
                            </div>
                            <span
                                class="hidden sm:inline-flex items-center gap-1.5 text-xs font-medium text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10 px-3 py-1.5 rounded-full border border-emerald-200 dark:border-emerald-500/20">
                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                                Active
                            </span>
                        </div>
                        <div
                            class="flex flex-wrap items-center gap-4 mt-3 text-sm text-surface-500 dark:text-surface-400">
                            <span class="flex items-center gap-1.5">
                                <font-awesome-icon :icon="faMapMarkerAlt" class="text-xs text-surface-400" />
                                {{ profileForm.email }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Personal Information -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Personal Information</h3>
                <p class="text-xs text-surface-500 dark:text-surface-400 mt-0.5">Update your personal details here</p>
            </div>
            <div class="p-6">
                <div class="flex flex-col gap-6">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-5 gap-y-6">
                        <FloatLabel variant="on">
                            <InputText id="profile-username" v-model="profileForm.username" class="w-full" />
                            <label for="profile-username">Username</label>
                        </FloatLabel>
                        <FloatLabel variant="on">
                            <InputText id="profile-email" v-model="profileForm.email" type="email" class="w-full" />
                            <label for="profile-email">Email</label>
                        </FloatLabel>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-5 gap-y-6">
                        <FloatLabel variant="on">
                            <InputText id="profile-phone" v-model="profileForm.phone" class="w-full" />
                            <label for="profile-phone">Phone</label>
                        </FloatLabel>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
