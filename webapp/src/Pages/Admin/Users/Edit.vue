<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { router } from '@inertiajs/vue3';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import MultiSelect from 'primevue/multiselect';
import Checkbox from 'primevue/checkbox';
import axios from 'axios';

const props = defineProps<{
    userId: string
}>();

const form = ref({
    username: '',
    email: '',
    phone: '',
    role_ids: [],
    is_active: true,
    is_superuser: false
});

const roles = ref([]);
const loading = ref(false);
const errors = ref<any>({});

const loadUser = async () => {
    try {
        const response = await axios.get(`/api/v1/users/${props.userId}`);
        const user = response.data.data;
        form.value = {
            username: user.username,
            email: user.email,
            phone: user.phone || '',
            role_ids: user.roles?.map((r: any) => r.id) || [],
            is_active: user.is_active,
            is_superuser: user.is_superuser
        };
    } catch (error) {
        console.error('Error loading user:', error);
    }
};

const loadRoles = async () => {
    try {
        const response = await axios.get('/api/v1/roles');
        roles.value = response.data.data;
    } catch (error) {
        console.error('Error loading roles:', error);
    }
};

const submitForm = async () => {
    loading.value = true;
    errors.value = {};

    try {
        await axios.put(`/api/v1/users/${props.userId}`, form.value);
        router.visit('/admin/users');
    } catch (error: any) {
        if (error.response?.data?.message) {
            errors.value.general = error.response.data.message;
        }
        if (error.response?.data?.errors) {
            errors.value = error.response.data.errors;
        }
        console.error('Error updating user:', error);
    } finally {
        loading.value = false;
    }
};

const cancel = () => {
    router.visit('/admin/users');
};

onMounted(() => {
    loadRoles();
    loadUser();
});
</script>

<template>
    <div class="p-6">
        <div class="mb-6">
            <div class="flex items-center gap-2 mb-2">
                <Button icon="pi pi-arrow-left" text rounded @click="cancel" v-tooltip.top="'Back to Users'" />
                <h1 class="text-3xl font-bold text-surface-900 dark:text-surface-0">Edit User</h1>
            </div>
            <p class="text-surface-600 dark:text-surface-400">Update user information</p>
        </div>

        <div
            class="bg-white dark:bg-surface-900 rounded-xl shadow-sm border border-surface-200 dark:border-surface-800 p-6 max-w-3xl">
            <form @submit.prevent="submitForm">
                <div v-if="errors.general"
                    class="mb-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                    <p class="text-red-600 dark:text-red-400">{{ errors.general }}</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Username -->
                    <div class="flex flex-col gap-2">
                        <label for="username" class="font-semibold text-surface-900 dark:text-surface-0">
                            Username <span class="text-red-500">*</span>
                        </label>
                        <InputText id="username" v-model="form.username" placeholder="Enter username"
                            :invalid="!!errors.username" />
                        <small v-if="errors.username" class="text-red-500">{{ errors.username }}</small>
                    </div>

                    <!-- Email -->
                    <div class="flex flex-col gap-2">
                        <label for="email" class="font-semibold text-surface-900 dark:text-surface-0">
                            Email <span class="text-red-500">*</span>
                        </label>
                        <InputText id="email" v-model="form.email" type="email" placeholder="Enter email address"
                            :invalid="!!errors.email" />
                        <small v-if="errors.email" class="text-red-500">{{ errors.email }}</small>
                    </div>

                    <!-- Phone -->
                    <div class="flex flex-col gap-2">
                        <label for="phone" class="font-semibold text-surface-900 dark:text-surface-0">
                            Phone
                        </label>
                        <InputText id="phone" v-model="form.phone" placeholder="Enter phone number"
                            :invalid="!!errors.phone" />
                        <small v-if="errors.phone" class="text-red-500">{{ errors.phone }}</small>
                    </div>

                    <!-- Roles -->
                    <div class="flex flex-col gap-2">
                        <label for="roles" class="font-semibold text-surface-900 dark:text-surface-0">
                            Roles
                        </label>
                        <MultiSelect id="roles" v-model="form.role_ids" :options="roles" optionLabel="name"
                            optionValue="id" placeholder="Select roles" :invalid="!!errors.role_ids" class="w-full" />
                        <small v-if="errors.role_ids" class="text-red-500">{{ errors.role_ids }}</small>
                    </div>

                    <!-- Is Active -->
                    <div class="flex items-center gap-2">
                        <Checkbox id="is_active" v-model="form.is_active" :binary="true" />
                        <label for="is_active"
                            class="font-semibold text-surface-900 dark:text-surface-0 cursor-pointer">
                            Active User
                        </label>
                    </div>

                    <!-- Is Superuser -->
                    <div class="flex items-center gap-2">
                        <Checkbox id="is_superuser" v-model="form.is_superuser" :binary="true" />
                        <label for="is_superuser"
                            class="font-semibold text-surface-900 dark:text-surface-0 cursor-pointer">
                            Superuser
                        </label>
                    </div>
                </div>

                <!-- Actions -->
                <div class="flex justify-end gap-3 mt-6 pt-6 border-t border-surface-200 dark:border-surface-800">
                    <Button label="Cancel" severity="secondary" outlined @click="cancel" :disabled="loading" />
                    <Button label="Update User" icon="pi pi-check" type="submit" :loading="loading" />
                </div>
            </form>
        </div>
    </div>
</template>
