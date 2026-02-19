<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { admin } from '@/core';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Checkbox from 'primevue/checkbox';
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
const searchQuery = ref('');

interface PermissionItem {
    id: string;
    name: string;
    module: string;
    description: string;
}

interface PermissionGroup {
    module: string;
    permissions: PermissionItem[];
}

interface RoleForm {
    name: string;
    permission_ids: string[];
}

const permissionGroups = ref<PermissionGroup[]>([]);
const selectedPermissions = ref<string[]>([]);
const expandedModules = ref<Set<string>>(new Set());

const initialForm: RoleForm = {
    name: '',
    permission_ids: []
};

const form = ref<RoleForm>({ ...initialForm });

// Module icons mapping
const moduleIcons: Record<string, string> = {
    user: 'pi pi-users',
    role: 'pi pi-shield',
    permission: 'pi pi-lock',
    dashboard: 'pi pi-th-large',
    setting: 'pi pi-cog',
    order: 'pi pi-shopping-cart',
    product: 'pi pi-box',
    notification: 'pi pi-bell',
    report: 'pi pi-chart-bar',
};

// Module colors mapping
const moduleColors: Record<string, { bg: string; text: string; border: string; badge: string }> = {
    user: { bg: 'bg-blue-50 dark:bg-blue-950/30', text: 'text-blue-700 dark:text-blue-300', border: 'border-blue-200 dark:border-blue-800', badge: 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300' },
    role: { bg: 'bg-purple-50 dark:bg-purple-950/30', text: 'text-purple-700 dark:text-purple-300', border: 'border-purple-200 dark:border-purple-800', badge: 'bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300' },
    permission: { bg: 'bg-amber-50 dark:bg-amber-950/30', text: 'text-amber-700 dark:text-amber-300', border: 'border-amber-200 dark:border-amber-800', badge: 'bg-amber-100 dark:bg-amber-900/50 text-amber-700 dark:text-amber-300' },
    dashboard: { bg: 'bg-emerald-50 dark:bg-emerald-950/30', text: 'text-emerald-700 dark:text-emerald-300', border: 'border-emerald-200 dark:border-emerald-800', badge: 'bg-emerald-100 dark:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300' },
    setting: { bg: 'bg-slate-50 dark:bg-slate-950/30', text: 'text-slate-700 dark:text-slate-300', border: 'border-slate-200 dark:border-slate-800', badge: 'bg-slate-100 dark:bg-slate-900/50 text-slate-700 dark:text-slate-300' },
    default: { bg: 'bg-indigo-50 dark:bg-indigo-950/30', text: 'text-indigo-700 dark:text-indigo-300', border: 'border-indigo-200 dark:border-indigo-800', badge: 'bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300' },
};

const getModuleIcon = (module: string) => moduleIcons[module] || 'pi pi-folder';
const getModuleColor = (module: string) => moduleColors[module] || moduleColors.default;

const filteredGroups = computed(() => {
    if (!searchQuery.value.trim()) return permissionGroups.value;
    const q = searchQuery.value.toLowerCase();
    return permissionGroups.value
        .map(group => ({
            ...group,
            permissions: group.permissions.filter(
                p => p.name.toLowerCase().includes(q) || p.description?.toLowerCase().includes(q) || p.module.toLowerCase().includes(q)
            )
        }))
        .filter(group => group.permissions.length > 0);
});

const totalPermissions = computed(() =>
    permissionGroups.value.reduce((sum, g) => sum + g.permissions.length, 0)
);

const loadPermissions = async () => {
    try {
        const response = await axios.get(admin.PERMISSIONS_API);
        permissionGroups.value = response.data.data;
        // Expand all modules by default
        permissionGroups.value.forEach(g => expandedModules.value.add(g.module));
    } catch (error) {
        console.error('Error loading permissions:', error);
    }
};

const isModuleFullySelected = (group: PermissionGroup): boolean => {
    return group.permissions.length > 0 && group.permissions.every(p => selectedPermissions.value.includes(p.id));
};

const isModulePartiallySelected = (group: PermissionGroup): boolean => {
    const count = group.permissions.filter(p => selectedPermissions.value.includes(p.id)).length;
    return count > 0 && count < group.permissions.length;
};

const getModuleSelectedCount = (group: PermissionGroup): number => {
    return group.permissions.filter(p => selectedPermissions.value.includes(p.id)).length;
};

const toggleModule = (group: PermissionGroup) => {
    if (isModuleFullySelected(group)) {
        selectedPermissions.value = selectedPermissions.value.filter(
            id => !group.permissions.some(p => p.id === id)
        );
    } else {
        const newIds = group.permissions.map(p => p.id);
        const existing = selectedPermissions.value.filter(
            id => !group.permissions.some(p => p.id === id)
        );
        selectedPermissions.value = [...existing, ...newIds];
    }
};

const toggleModuleExpand = (module: string) => {
    if (expandedModules.value.has(module)) {
        expandedModules.value.delete(module);
    } else {
        expandedModules.value.add(module);
    }
};

const selectAll = () => {
    selectedPermissions.value = permissionGroups.value.flatMap(g => g.permissions.map(p => p.id));
};

const deselectAll = () => {
    selectedPermissions.value = [];
};

const getActionLabel = (permName: string): string => {
    const parts = permName.split('.');
    const action = parts[parts.length - 1];
    return action.charAt(0).toUpperCase() + action.slice(1).replace(/-/g, ' ');
};

const getActionIcon = (permName: string): string => {
    const parts = permName.split('.');
    const action = parts[parts.length - 1];
    const icons: Record<string, string> = {
        read: 'pi pi-eye',
        write: 'pi pi-plus',
        edit: 'pi pi-pencil',
        delete: 'pi pi-trash',
        list: 'pi pi-list',
        detail: 'pi pi-info-circle',
        sync: 'pi pi-sync',
        datatables: 'pi pi-table',
    };
    return icons[action] || 'pi pi-circle';
};

const getActionColor = (permName: string): string => {
    const parts = permName.split('.');
    const action = parts[parts.length - 1];
    const colors: Record<string, string> = {
        read: 'text-blue-500',
        write: 'text-green-500',
        edit: 'text-amber-500',
        delete: 'text-red-500',
        list: 'text-cyan-500',
        detail: 'text-indigo-500',
        sync: 'text-purple-500',
        datatables: 'text-teal-500',
    };
    return colors[action] || 'text-surface-400';
};

const initForm = () => {
    if (props.role) {
        isEditing.value = true;
        form.value = {
            name: props.role.name,
            permission_ids: []
        };
        if (props.role.permissions && props.role.permissions.length > 0) {
            selectedPermissions.value = props.role.permissions.map((p: any) => p.id);
        } else {
            selectedPermissions.value = [];
        }
    } else {
        isEditing.value = false;
        form.value = { ...initialForm };
        selectedPermissions.value = [];
    }
    errors.value = {};
};

watch(() => props.role, () => {
    initForm();
}, { immediate: true });

const submitForm = async () => {
    loading.value = true;
    errors.value = {};
    form.value.permission_ids = [...selectedPermissions.value];

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
    loadPermissions();
});
</script>

<template>
    <form @submit.prevent="submitForm">
        <div v-if="errors.general"
            class="mb-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl">
            <p class="text-red-600 dark:text-red-400 flex items-center gap-2">
                <i class="pi pi-exclamation-triangle"></i>
                {{ errors.general }}
            </p>
        </div>

        <div class="flex flex-col gap-6">
            <!-- Role Name -->
            <div class="flex flex-col gap-2">
                <label for="name" class="font-semibold text-surface-900 dark:text-surface-0">
                    Role Name <span class="text-red-500">*</span>
                </label>
                <InputText id="name" v-model="form.name" placeholder="Enter role name" :invalid="!!errors.name"
                    class="w-full" />
                <small v-if="errors.name" class="text-red-500">{{ errors.name }}</small>
            </div>

            <!-- Permissions Section -->
            <div class="flex flex-col gap-3">
                <!-- Header -->
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <label class="font-semibold text-surface-900 dark:text-surface-0">
                            Permissions
                        </label>
                        <span
                            class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300">
                            <i class="pi pi-check-circle text-[10px]"></i>
                            {{ selectedPermissions.length }} / {{ totalPermissions }}
                        </span>
                    </div>
                    <div class="flex items-center gap-1">
                        <Button label="All" size="small" text severity="info" @click="selectAll"
                            icon="pi pi-check-square" class="!text-xs" />
                        <Button label="None" size="small" text severity="secondary" @click="deselectAll"
                            icon="pi pi-stop" class="!text-xs" />
                    </div>
                </div>

                <!-- Search -->
                <div class="relative">
                    <i
                        class="pi pi-search absolute left-3 top-1/2 -translate-y-1/2 text-surface-400 text-sm pointer-events-none"></i>
                    <InputText v-model="searchQuery" placeholder="Search permissions..."
                        class="w-full !pl-9 !text-sm" />
                </div>

                <!-- Permission Groups -->
                <div
                    class="border border-surface-200 dark:border-surface-700 rounded-xl overflow-hidden bg-surface-0 dark:bg-surface-900">
                    <div v-if="filteredGroups.length === 0"
                        class="text-surface-400 text-center py-12 flex flex-col items-center gap-3">
                        <i class="pi pi-lock text-3xl opacity-40"></i>
                        <span class="text-sm">No permissions available</span>
                    </div>

                    <div v-for="(group, idx) in filteredGroups" :key="group.module"
                        :class="[idx > 0 ? 'border-t border-surface-100 dark:border-surface-800' : '']">

                        <!-- Module Header -->
                        <div class="flex items-center gap-3 px-4 py-3 cursor-pointer select-none transition-colors duration-150"
                            :class="[getModuleColor(group.module).bg, 'hover:brightness-95 dark:hover:brightness-110']"
                            @click="toggleModuleExpand(group.module)">
                            <div class="flex items-center gap-3 flex-1 min-w-0" @click.stop>
                                <Checkbox :modelValue="isModuleFullySelected(group)" :binary="true"
                                    @update:modelValue="toggleModule(group)"
                                    :class="{ 'opacity-60': isModulePartiallySelected(group) }" />
                                <div class="flex items-center gap-2.5 flex-1 min-w-0">
                                    <i
                                        :class="[getModuleIcon(group.module), getModuleColor(group.module).text, 'text-lg']"></i>
                                    <span class="font-semibold text-sm capitalize"
                                        :class="getModuleColor(group.module).text">
                                        {{ group.module }}
                                    </span>
                                </div>
                            </div>
                            <div class="flex items-center gap-2">
                                <span class="text-[11px] font-medium px-2 py-0.5 rounded-full"
                                    :class="getModuleColor(group.module).badge">
                                    {{ getModuleSelectedCount(group) }}/{{ group.permissions.length }}
                                </span>
                                <i class="pi text-xs text-surface-400 transition-transform duration-200"
                                    :class="expandedModules.has(group.module) ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
                            </div>
                        </div>

                        <!-- Permission Items (Collapsible) -->
                        <Transition name="collapse">
                            <div v-show="expandedModules.has(group.module)"
                                class="px-4 py-2 bg-surface-50/50 dark:bg-surface-950/30">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-1">
                                    <label v-for="perm in group.permissions" :key="perm.id" :for="perm.id"
                                        class="flex items-center gap-3 px-3 py-2.5 rounded-lg cursor-pointer transition-all duration-150 group/perm"
                                        :class="selectedPermissions.includes(perm.id)
                                            ? 'bg-primary-50 dark:bg-primary-900/20 ring-1 ring-primary-200 dark:ring-primary-800'
                                            : 'hover:bg-surface-100 dark:hover:bg-surface-800'
                                            ">
                                        <Checkbox v-model="selectedPermissions" :inputId="perm.id" :value="perm.id" />
                                        <i
                                            :class="[getActionIcon(perm.name), getActionColor(perm.name), 'text-sm']"></i>
                                        <div class="flex flex-col min-w-0">
                                            <span
                                                class="text-sm font-medium text-surface-800 dark:text-surface-200 truncate">
                                                {{ getActionLabel(perm.name) }}
                                            </span>
                                            <span class="text-[11px] text-surface-400 truncate font-mono">
                                                {{ perm.name }}
                                            </span>
                                        </div>
                                    </label>
                                </div>
                            </div>
                        </Transition>
                    </div>
                </div>

                <small v-if="errors.permission_ids" class="text-red-500">{{ errors.permission_ids }}</small>
            </div>
        </div>

        <div class="flex justify-end gap-3 mt-6 pt-6 border-t border-surface-200 dark:border-surface-800">
            <Button label="Cancel" severity="secondary" outlined @click="emit('cancel')" :disabled="loading" />
            <Button :label="isEditing ? 'Update Role' : 'Create Role'" icon="pi pi-check" type="submit"
                :loading="loading" />
        </div>
    </form>
</template>

<style scoped>
.collapse-enter-active,
.collapse-leave-active {
    transition: all 0.25s ease;
    overflow: hidden;
}

.collapse-enter-from,
.collapse-leave-to {
    max-height: 0;
    opacity: 0;
    padding-top: 0;
    padding-bottom: 0;
}

.collapse-enter-to,
.collapse-leave-from {
    max-height: 600px;
    opacity: 1;
}
</style>
