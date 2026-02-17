<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { admin } from '@/core';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Tree from 'primevue/tree';
import axios from 'axios';
import { useToast } from 'primevue/usetoast';

const props = defineProps<{
    role?: any;
}>();

const emit = defineEmits(['success', 'cancel']);

const toast = useToast();
const loading = ref(false);
const errors = ref<any>({});
const isEditing = ref(false);
const routes = ref<TreeNode[]>([]);
const selectedRoutes = ref<any>({});

interface RoleForm {
    name: string;
    permission_ids: string[];
}

interface TreeNode {
    key: string;
    label: string;
    icon?: string;
    children?: TreeNode[];
}

const initialForm: RoleForm = {
    name: '',
    permission_ids: []
};

const form = ref<RoleForm>({ ...initialForm });

const loadRoutes = async () => {
    try {
        const response = await axios.get(admin.ROUTES_API);
        // Transform flat routes to tree structure
        routes.value = transformToTreeNodes(response.data.data);
    } catch (error) {
        console.error('Error loading routes:', error);
    }
};

const transformToTreeNodes = (routesList: any[]): TreeNode[] => {
    return routesList
        .filter((route: any) => !route.parent_id)
        .map((route: any) => ({
            key: route.id,
            label: route.name,
            icon: route.icon || 'pi pi-folder',
            children: getChildren(route.id, routesList)
        }));
};

const getChildren = (parentId: string, routesList: any[]): TreeNode[] => {
    return routesList
        .filter((route: any) => route.parent_id === parentId)
        .map((route: any) => ({
            key: route.id,
            label: route.name,
            icon: route.icon || 'pi pi-file',
            children: getChildren(route.id, routesList)
        }));
};

const initForm = () => {
    if (props.role) {
        isEditing.value = true;
        form.value = {
            name: props.role.name,
            permission_ids: []
        };

        // Pre-select routes that are assigned to this role
        if (props.role.routes && props.role.routes.length > 0) {
            const selection: any = {};
            props.role.routes.forEach((route: any) => {
                selection[route.id] = { checked: true, partialChecked: false };
            });
            selectedRoutes.value = selection;
        } else {
            selectedRoutes.value = {};
        }
    } else {
        isEditing.value = false;
        form.value = { ...initialForm };
        selectedRoutes.value = {};
    }
    errors.value = {};
};

watch(() => props.role, () => {
    initForm();
}, { immediate: true });

const submitForm = async () => {
    loading.value = true;
    errors.value = {};

    // Extract selected route IDs from tree selection
    form.value.permission_ids = Object.keys(selectedRoutes.value).filter(
        key => selectedRoutes.value[key].checked || selectedRoutes.value[key].partialChecked
    );

    try {
        if (isEditing.value) {
            await axios.put(`${admin.ROLES_API}/${props.role.id}`, form.value);
            toast.add({ severity: 'success', summary: 'Success', detail: 'Role updated successfully', life: 3000 });
        } else {
            await axios.post(admin.ROLES_API, form.value);
            toast.add({ severity: 'success', summary: 'Success', detail: 'Role created successfully', life: 3000 });
        }

        emit('success');
    } catch (error: any) {
        if (error.response?.data?.message) {
            errors.value.general = error.response.data.message;
        }
        if (error.response?.data?.errors) {
            errors.value = error.response.data.errors;
        }
        console.error('Error saving role:', error);
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    loadRoutes();
});
</script>

<template>
    <form @submit.prevent="submitForm">
        <div v-if="errors.general"
            class="mb-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p class="text-red-600 dark:text-red-400">{{ errors.general }}</p>
        </div>

        <div class="flex flex-col gap-6">
            <!-- Role Name -->
            <div class="flex flex-col gap-2">
                <label for="name" class="font-semibold text-surface-900 dark:text-surface-0">
                    Role Name <span class="text-red-500">*</span>
                </label>
                <InputText id="name" v-model="form.name" placeholder="Enter role name" :invalid="!!errors.name" />
                <small v-if="errors.name" class="text-red-500">{{ errors.name }}</small>
            </div>

            <!-- Permissions Tree -->
            <div class="flex flex-col gap-2">
                <label class="font-semibold text-surface-900 dark:text-surface-0">
                    Permissions
                </label>
                <div class="border border-surface-200 dark:border-surface-800 rounded-lg p-4 max-h-96 overflow-y-auto">
                    <Tree :value="routes" v-model:selectionKeys="selectedRoutes" selectionMode="checkbox"
                        :metaKeySelection="false" />
                </div>
                <small v-if="errors.permission_ids" class="text-red-500">{{ errors.permission_ids }}</small>
                <small class="text-surface-500">Select the routes/permissions this role can access</small>
            </div>
        </div>

        <div class="flex justify-end gap-3 mt-6 pt-6 border-t border-surface-200 dark:border-surface-800">
            <Button label="Cancel" severity="secondary" outlined @click="emit('cancel')" :disabled="loading" />
            <Button :label="isEditing ? 'Update Role' : 'Create Role'" icon="pi pi-check" type="submit"
                :loading="loading" />
        </div>
    </form>
</template>
