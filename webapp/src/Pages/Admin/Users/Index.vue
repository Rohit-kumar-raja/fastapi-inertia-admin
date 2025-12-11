<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { router } from '@inertiajs/vue3';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import Tag from 'primevue/tag';
import axios from 'axios';

const users = ref([]);
const loading = ref(false);
const totalRecords = ref(0);
const filters = ref({
    global: { value: '', matchMode: 'contains' }
});

const lazyParams = ref({
    first: 0,
    rows: 10,
    page: 0,
    sortField: null,
    sortOrder: null,
    filters: filters.value
});

const loadUsers = async (event?: any) => {
    loading.value = true;
    
    const params = {
        draw: 1,
        start: event?.first || 0,
        length: event?.rows || 10,
        search: { value: filters.value.global.value || '' },
        order: event?.sortField ? [{
            column: event.sortField,
            dir: event.sortOrder === 1 ? 'asc' : 'desc'
        }] : [],
        columns: []
    };

    try {
        const response = await axios.post('/api/v1/users/filter', params);
        users.value = response.data.data.data;
        totalRecords.value = response.data.data.recordsFiltered;
    } catch (error) {
        console.error('Error loading users:', error);
    } finally {
        loading.value = false;
    }
};

const onPage = (event: any) => {
    lazyParams.value = event;
    loadUsers(event);
};

const onSort = (event: any) => {
    lazyParams.value = event;
    loadUsers(event);
};

const onFilter = () => {
    lazyParams.value.first = 0;
    loadUsers(lazyParams.value);
};

const createUser = () => {
    router.visit('/admin/users/create');
};

const editUser = (userId: string) => {
    router.visit(`/admin/users/${userId}/edit`);
};

const deleteUser = async (userId: string) => {
    if (confirm('Are you sure you want to delete this user?')) {
        try {
            await axios.delete(`/api/v1/users/${userId}`);
            loadUsers(lazyParams.value);
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    }
};

const resetPassword = async (userId: string) => {
    if (confirm('Are you sure you want to reset this user\'s password?')) {
        try {
            await axios.post(`/api/v1/users/reset-password/${userId}`);
            alert('Password reset successfully');
        } catch (error) {
            console.error('Error resetting password:', error);
        }
    }
};

onMounted(() => {
    loadUsers();
});
</script>

<template>
    <div class="p-6">
        <div class="mb-6">
            <h1 class="text-3xl font-bold text-surface-900 dark:text-surface-0 mb-2">Users Management</h1>
            <p class="text-surface-600 dark:text-surface-400">Manage system users, roles, and permissions</p>
        </div>

        <div class="bg-white dark:bg-surface-900 rounded-xl shadow-sm border border-surface-200 dark:border-surface-800">
            <div class="p-6 border-b border-surface-200 dark:border-surface-800">
                <div class="flex justify-between items-center">
                    <IconField iconPosition="left">
                        <InputIcon class="pi pi-search" />
                        <InputText 
                            v-model="filters.global.value" 
                            placeholder="Search users..." 
                            @input="onFilter"
                            class="w-80"
                        />
                    </IconField>
                    <Button 
                        label="Create User" 
                        icon="pi pi-plus" 
                        @click="createUser"
                        severity="primary"
                    />
                </div>
            </div>

            <DataTable 
                :value="users" 
                :lazy="true"
                :paginator="true" 
                :rows="10"
                :totalRecords="totalRecords"
                :loading="loading"
                @page="onPage"
                @sort="onSort"
                :rowsPerPageOptions="[5, 10, 20, 50]"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} users"
                stripedRows
            >
                <Column field="username" header="Username" sortable>
                    <template #body="{ data }">
                        <div class="font-semibold text-surface-900 dark:text-surface-0">
                            {{ data.username }}
                        </div>
                    </template>
                </Column>
                
                <Column field="email" header="Email" sortable>
                    <template #body="{ data }">
                        <div class="text-surface-600 dark:text-surface-400">
                            {{ data.email }}
                        </div>
                    </template>
                </Column>

                <Column field="phone" header="Phone" sortable>
                    <template #body="{ data }">
                        <div class="text-surface-600 dark:text-surface-400">
                            {{ data.phone || '-' }}
                        </div>
                    </template>
                </Column>

                <Column field="roles" header="Roles">
                    <template #body="{ data }">
                        <div class="flex gap-1 flex-wrap">
                            <Tag 
                                v-for="role in data.roles" 
                                :key="role.id" 
                                :value="role.name"
                                severity="info"
                            />
                            <span v-if="!data.roles || data.roles.length === 0" class="text-surface-400">No roles</span>
                        </div>
                    </template>
                </Column>

                <Column field="is_superuser" header="Superuser" sortable>
                    <template #body="{ data }">
                        <Tag 
                            :value="data.is_superuser ? 'Yes' : 'No'" 
                            :severity="data.is_superuser ? 'danger' : 'secondary'"
                        />
                    </template>
                </Column>

                <Column field="is_active" header="Status" sortable>
                    <template #body="{ data }">
                        <Tag 
                            :value="data.is_active ? 'Active' : 'Inactive'" 
                            :severity="data.is_active ? 'success' : 'warning'"
                        />
                    </template>
                </Column>

                <Column header="Actions" :exportable="false">
                    <template #body="{ data }">
                        <div class="flex gap-2">
                            <Button 
                                icon="pi pi-pencil" 
                                rounded 
                                text 
                                severity="info"
                                @click="editUser(data.id)"
                                v-tooltip.top="'Edit'"
                            />
                            <Button 
                                icon="pi pi-key" 
                                rounded 
                                text 
                                severity="warning"
                                @click="resetPassword(data.id)"
                                v-tooltip.top="'Reset Password'"
                            />
                            <Button 
                                icon="pi pi-trash" 
                                rounded 
                                text 
                                severity="danger"
                                @click="deleteUser(data.id)"
                                v-tooltip.top="'Delete'"
                            />
                        </div>
                    </template>
                </Column>

                <template #empty>
                    <div class="text-center py-8 text-surface-400">
                        No users found.
                    </div>
                </template>
            </DataTable>
        </div>
    </div>
</template>
