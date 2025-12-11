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

const roles = ref([]);
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

const loadRoles = async (event?: any) => {
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
        const response = await axios.post('/api/v1/roles/filter', params);
        roles.value = response.data.data.data;
        totalRecords.value = response.data.data.recordsFiltered;
    } catch (error) {
        console.error('Error loading roles:', error);
    } finally {
        loading.value = false;
    }
};

const onPage = (event: any) => {
    lazyParams.value = event;
    loadRoles(event);
};

const onSort = (event: any) => {
    lazyParams.value = event;
    loadRoles(event);
};

const onFilter = () => {
    lazyParams.value.first = 0;
    loadRoles(lazyParams.value);
};

const createRole = () => {
    router.visit('/admin/roles/create');
};

const editRole = (roleId: string) => {
    router.visit(`/admin/roles/${roleId}/edit`);
};

const deleteRole = async (roleId: string) => {
    if (confirm('Are you sure you want to delete this role?')) {
        try {
            await axios.delete(`/api/v1/roles/${roleId}`);
            loadRoles(lazyParams.value);
        } catch (error) {
            console.error('Error deleting role:', error);
        }
    }
};

onMounted(() => {
    loadRoles();
});
</script>

<template>
    <div class="p-6">
        <div class="mb-6">
            <h1 class="text-3xl font-bold text-surface-900 dark:text-surface-0 mb-2">Roles Management</h1>
            <p class="text-surface-600 dark:text-surface-400">Manage roles and their permissions</p>
        </div>

        <div
            class="bg-white dark:bg-surface-900 rounded-xl shadow-sm border border-surface-200 dark:border-surface-800">
            <div class="p-6 border-b border-surface-200 dark:border-surface-800">
                <div class="flex justify-between items-center">
                    <IconField iconPosition="left">
                        <InputIcon class="pi pi-search" />
                        <InputText v-model="filters.global.value" placeholder="Search roles..." @input="onFilter"
                            class="w-80" />
                    </IconField>
                    <Button label="Create Role" icon="pi pi-plus" @click="createRole" severity="primary" />
                </div>
            </div>

            <DataTable :value="roles" :lazy="true" :paginator="true" :rows="10" :totalRecords="totalRecords"
                :loading="loading" @page="onPage" @sort="onSort" :rowsPerPageOptions="[5, 10, 20, 50]"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} roles" stripedRows>
                <Column field="name" header="Role Name" sortable>
                    <template #body="{ data }">
                        <div class="font-semibold text-surface-900 dark:text-surface-0">
                            {{ data.name }}
                        </div>
                    </template>
                </Column>

                <Column field="routes" header="Permissions">
                    <template #body="{ data }">
                        <Tag :value="`${data.routes?.length || 0} permissions`" severity="info" />
                    </template>
                </Column>

                <Column field="users" header="Users">
                    <template #body="{ data }">
                        <Tag :value="`${data.users?.length || 0} users`" severity="secondary" />
                    </template>
                </Column>

                <Column field="is_active" header="Status" sortable>
                    <template #body="{ data }">
                        <Tag :value="data.is_active ? 'Active' : 'Inactive'"
                            :severity="data.is_active ? 'success' : 'warning'" />
                    </template>
                </Column>

                <Column header="Actions" :exportable="false">
                    <template #body="{ data }">
                        <div class="flex gap-2">
                            <Button icon="pi pi-pencil" rounded text severity="info" @click="editRole(data.id)"
                                v-tooltip.top="'Edit'" />
                            <Button icon="pi pi-trash" rounded text severity="danger" @click="deleteRole(data.id)"
                                v-tooltip.top="'Delete'" />
                        </div>
                    </template>
                </Column>

                <template #empty>
                    <div class="text-center py-8 text-surface-400">
                        No roles found.
                    </div>
                </template>
            </DataTable>
        </div>
    </div>
</template>
