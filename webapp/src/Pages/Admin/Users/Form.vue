<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { admin } from '@/core';
import axios from 'axios';
import { useToast } from 'primevue/usetoast';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import MultiSelect from 'primevue/multiselect';
import Checkbox from 'primevue/checkbox';

const props = defineProps<{
    user?: any;
}>();

const emit = defineEmits(['success', 'cancel']);

const toast = useToast();
const loading = ref(false);
const roles = ref([]);
const errors = ref<any>({});
const isEditing = ref(false);

const initialForm = {
    username: '',
    email: '',
    phone: '',
    password: '',
    role_ids: [],
    is_active: true,
    is_superuser: false
}

const form = ref(initialForm);

const loadRoles = async () => {
    try {
        const response = await axios.get(admin.ROLES_LIST_API);
        roles.value = response.data.data;
    } catch (error) {
        console.error('Error loading roles:', error);
    }
};

const initForm = () => {
    if (props.user) {
        isEditing.value = true;
        form.value = {
            username: props.user.username,
            email: props.user.email,
            phone: props.user.phone || '',
            password: '',
            role_ids: props.user.roles.map((r: any) => r.id),
            is_active: props.user.is_active,
            is_superuser: props.user.is_superuser
        };
    } else {
        isEditing.value = false;
        form.value = initialForm;
    }
    errors.value = {};
};

watch(() => props.user, () => {
    initForm();
}, { immediate: true });

const submitForm = async () => {
    loading.value = true;
    errors.value = {};

    try {
        if (isEditing.value) {
            const data: any = { ...form.value };
            if (!data.password) delete data.password;

            await axios.put(`${admin.USERS_API}/${props.user.id}`, data);
            toast.add({ severity: 'success', summary: 'Success', detail: 'User updated successfully', life: 3000 });
        } else {
            await axios.post(admin.USERS_API, form.value);
            toast.add({ severity: 'success', summary: 'Success', detail: 'User created successfully', life: 3000 });
        }

        emit('success');
    } catch (error: any) {
        if (error.response?.data?.message) {
            errors.value.general = error.response.data.message;
        }
        if (error.response?.data?.errors) {
            errors.value = error.response.data.errors;
        }
        console.error('Error saving user:', error);
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    loadRoles();
});
</script>

<template>
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
                <InputText id="phone" v-model="form.phone" placeholder="Enter phone number" :invalid="!!errors.phone" />
                <small v-if="errors.phone" class="text-red-500">{{ errors.phone }}</small>
            </div>

            <!-- Password -->
            <div class="flex flex-col gap-2">
                <label for="password" class="font-semibold text-surface-900 dark:text-surface-0">
                    Password <span v-if="!isEditing" class="text-red-500">*</span>
                </label>
                <Password id="password" v-model="form.password" placeholder="Enter password" :feedback="true" toggleMask
                    :invalid="!!errors.password" inputClass="w-full" class="w-full" />
                <small v-if="errors.password" class="text-red-500">{{ errors.password }}</small>
                <small class="text-surface-500" v-if="isEditing">Leave blank to keep current password</small>
                <small class="text-surface-500" v-else>Minimum 8 characters</small>
            </div>

            <!-- Roles -->
            <div class="flex flex-col gap-2 md:col-span-2">
                <label for="roles" class="font-semibold text-surface-900 dark:text-surface-0">
                    Roles
                </label>
                <MultiSelect id="roles" v-model="form.role_ids" :options="roles" optionLabel="name" optionValue="id"
                    placeholder="Select roles" :invalid="!!errors.role_ids" class="w-full" />
                <small v-if="errors.role_ids" class="text-red-500">{{ errors.role_ids }}</small>
            </div>

            <!-- Is Active -->
            <div class="flex items-center gap-2">
                <Checkbox id="is_active" v-model="form.is_active" :binary="true" />
                <label for="is_active" class="font-semibold text-surface-900 dark:text-surface-0 cursor-pointer">
                    Active User
                </label>
            </div>

            <!-- Is Superuser -->
            <div class="flex items-center gap-2">
                <Checkbox id="is_superuser" v-model="form.is_superuser" :binary="true" />
                <label for="is_superuser" class="font-semibold text-surface-900 dark:text-surface-0 cursor-pointer">
                    Superuser
                </label>
            </div>
        </div>

        <div class="flex justify-end gap-3 mt-6 pt-6 border-t border-surface-200 dark:border-surface-800">
            <Button label="Cancel" severity="secondary" outlined @click="emit('cancel')" :disabled="loading" />
            <Button :label="isEditing ? 'Update User' : 'Create User'" icon="pi pi-check" type="submit"
                :loading="loading" />
        </div>
    </form>
</template>
