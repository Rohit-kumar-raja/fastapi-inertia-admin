<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { router } from '@inertiajs/vue3';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Tree from 'primevue/tree';
import axios from 'axios';

const props = defineProps<{
    roleId: string
}>();

interface RoleForm {
    name: string;
    permission_ids: string[];
}

const form = ref<RoleForm>({
    name: '',
    permission_ids: []
});

interface TreeNode {
    key: string;
    label: string;
    icon?: string;
    children?: TreeNode[];
}

const routes = ref<TreeNode[]>([]);
const selectedRoutes = ref<any>({});
const loading = ref(false);
const errors = ref<any>({});

const loadRole = async () => {
    try {
        const response = await axios.get(`${admin.ROLES_API}/${props.roleId}`);
        const role = response.data.data;
        form.value.name = role.name;

        // Pre-select routes that are assigned to this role
        if (role.routes && role.routes.length > 0) {
            const selection: any = {};
            role.routes.forEach((route: any) => {
                selection[route.id] = { checked: true, partialChecked: false };
            });
            selectedRoutes.value = selection;
        }
    } catch (error) {
        console.error('Error loading role:', error);
    }
};

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

const submitForm = async () => {
    loading.value = true;
    errors.value = {};

    // Extract selected route IDs from tree selection
    form.value.permission_ids = Object.keys(selectedRoutes.value).filter(
        key => selectedRoutes.value[key].checked || selectedRoutes.value[key].partialChecked
    );

    try {
        await axios.put(`/api/v1/roles/${props.roleId}`, form.value);
        router.visit('/admin/roles');
    } catch (error: any) {
        if (error.response?.data?.message) {
            errors.value.general = error.response.data.message;
        }
        if (error.response?.data?.errors) {
            errors.value = error.response.data.errors;
        }
        console.error('Error updating role:', error);
    } finally {
        loading.value = false;
    }
};

const cancel = () => {
    router.visit('/administration/roles');
};

onMounted(async () => {
    await loadRoutes();
    await loadRole();
});
</script>

<template>
    <div class="p-6">
        <div class="mb-6">
            <div class="flex items-center gap-2 mb-2">
                <Button icon="pi pi-arrow-left" text rounded @click="cancel" v-tooltip.top="'Back to Roles'" />
                <h1 class="text-3xl font-bold text-surface-900 dark:text-surface-0">Edit Role</h1>
            </div>
            <p class="text-surface-600 dark:text-surface-400">Update role information and permissions</p>
        </div>

        <div
            class="bg-white dark:bg-surface-900 rounded-xl shadow-sm border border-surface-200 dark:border-surface-800 p-6 max-w-3xl">
            <form @submit.prevent="submitForm">
                <div v-if="errors.general"
                    class="mb-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                    <p class="text-red-600 dark:text-red-400">{{ errors.general }}</p>
                </div>

                <!-- Role Name -->
                <div class="flex flex-col gap-2 mb-6">
                    <label for="name" class="font-semibold text-surface-900 dark:text-surface-0">
                        Role Name <span class="text-red-500">*</span>
                    </label>
                    <InputText id="name" v-model="form.name" placeholder="Enter role name" :invalid="!!errors.name" />
                    <small v-if="errors.name" class="text-red-500">{{ errors.name }}</small>
                </div>

                <!-- Permissions Tree -->
                <div class="flex flex-col gap-2 mb-6">
                    <label class="font-semibold text-surface-900 dark:text-surface-0">
                        Permissions
                    </label>
                    <div
                        class="border border-surface-200 dark:border-surface-800 rounded-lg p-4 max-h-96 overflow-y-auto">
                        <Tree :value="routes" v-model:selectionKeys="selectedRoutes" selectionMode="checkbox"
                            :metaKeySelection="false" />
                    </div>
                    <small v-if="errors.permission_ids" class="text-red-500">{{ errors.permission_ids }}</small>
                    <small class="text-surface-500">Select the routes/permissions this role can access</small>
                </div>

                <!-- Actions -->
                <div class="flex justify-end gap-3 pt-6 border-t border-surface-200 dark:border-surface-800">
                    <Button label="Cancel" severity="secondary" outlined @click="cancel" :disabled="loading" />
                    <Button label="Update Role" icon="pi pi-check" type="submit" :loading="loading" />
                </div>
            </form>
        </div>
    </div>
</template>
