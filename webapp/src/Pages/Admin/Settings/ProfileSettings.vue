<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faCamera, faUser, faEnvelope, faPhone } from '@fortawesome/free-solid-svg-icons';
import FloatLabel from 'primevue/floatlabel';
import { useToast } from 'primevue';
import axios from 'axios';

const props = defineProps<{
    user?: any;
}>();

const toast = useToast();
const saving = ref(false);

const profileForm = ref({
    username: '',
    email: '',
    phone: '',
});

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
    <div class="space-y-6 animate-fade-in h-full">
        <!-- Profile Card -->
        <div
            class="rounded-2xl border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <!-- Cover / Hero -->
            <div class="relative h-32 bg-linear-to-r from-indigo-500 via-purple-500 to-pink-500">
                <div
                    class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PHBhdGggZD0iTTM2IDM0djEyaC0yVjM0SDIydi0yaDE0djJoLTJ6Ii8+PC9nPjwvZz48L3N2Zz4=')] opacity-30">
                </div>
            </div>

            <!-- Avatar + Info -->
            <div class="px-6 pb-6">
                <div class="flex flex-col sm:flex-row items-start sm:items-end gap-4 -mt-12">
                    <!-- Avatar -->
                    <div class="relative group cursor-pointer shrink-0">
                        <div
                            class="w-24 h-24 rounded-2xl overflow-hidden ring-4 ring-white dark:ring-surface-900 shadow-xl">
                            <img :src="avatarUrl" alt="Profile"
                                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                        </div>
                        <div
                            class="absolute inset-0 flex items-center justify-center bg-black/40 rounded-2xl opacity-0 group-hover:opacity-100 transition-all duration-300 backdrop-blur-sm">
                            <font-awesome-icon :icon="faCamera" class="text-white text-lg" />
                        </div>
                        <div
                            class="absolute -bottom-1 -right-1 w-5 h-5 bg-emerald-500 rounded-full border-[3px] border-white dark:border-surface-900">
                        </div>
                    </div>

                    <!-- Name + Role -->
                    <div class="flex-1 sm:pb-1">
                        <h3 class="text-lg font-bold text-surface-900 dark:text-white">
                            {{ profileForm.username || 'Username' }}
                        </h3>
                        <p class="text-sm text-indigo-600 dark:text-indigo-400 font-medium">Administrator</p>
                    </div>

                    <!-- Status Badge -->
                    <span
                        class="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10 px-3 py-1.5 rounded-full border border-emerald-200 dark:border-emerald-500/20 sm:mb-1">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                        Active
                    </span>
                </div>
            </div>
        </div>

        <!-- Personal Information -->
        <div
            class="rounded-2xl lg:h-[calc(100vh-555px)] border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 overflow-hidden">
            <div
                class="px-6 py-4 border-b border-surface-100 dark:border-surface-800 bg-surface-50/50 dark:bg-surface-800/30">
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 rounded-lg bg-linear-to-br from-indigo-500 to-blue-600 flex items-center justify-center text-white">
                        <font-awesome-icon :icon="faUser" class="text-xs" />
                    </div>
                    <div>
                        <h3 class="text-sm font-semibold text-surface-900 dark:text-white">Personal Information</h3>
                        <p class="text-xs text-surface-500 dark:text-surface-400">Update your personal details</p>
                    </div>
                </div>
            </div>
            <div class="p-6">
                <div class="flex flex-col gap-5">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                        <FloatLabel variant="on">
                            <InputText id="profile-username" v-model="profileForm.username" class="w-full" />
                            <label for="profile-username">Username</label>
                        </FloatLabel>
                        <FloatLabel variant="on">
                            <InputText id="profile-email" v-model="profileForm.email" type="email" class="w-full" />
                            <label for="profile-email">Email</label>
                        </FloatLabel>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                        <FloatLabel variant="on">
                            <InputText id="profile-phone" v-model="profileForm.phone" class="w-full" />
                            <label for="profile-phone">Phone</label>
                        </FloatLabel>
                    </div>
                </div>
            </div>
            <!-- Save Button -->
            <div class="flex justify-end px-6 pb-6">
                <button @click="saveProfile" :disabled="saving"
                    class="inline-flex items-center gap-2 text-sm font-semibold bg-linear-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white px-6 py-2.5 rounded-xl shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:shadow-indigo-500/40 hover:-translate-y-0.5 disabled:opacity-50">
                    Save Profile
                </button>
            </div>
        </div>
    </div>
</template>
