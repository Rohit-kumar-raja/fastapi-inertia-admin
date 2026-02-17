<script setup lang="ts">
import AppDataTable from '@/Components/AppDataTable.vue';
import AppModal from '@/Components/AppModal.vue';
import RoleForm from './Form.vue';
import { admin } from '@/core';
import { ref } from 'vue';
import axios from 'axios';
import { useToast } from 'primevue/usetoast';

const toast = useToast();
const tableRef = ref();

const config = {
    title: "Roles",
    dataApi: admin.ROLES_FILTER_API,
    headers: [
        { field: "name", label: "Name", sortable: true },
        { field: "description", label: "Description", sortable: true },
        { field: "created_at", label: "Created At", sortable: true },
        { field: "updated_at", label: "Updated At", sortable: true }
    ],
    actions: {
        addRecord: { isEnabled: true },
        editRecord: { isEnabled: true },
        deleteRecord: { isEnabled: true }
    }
};

// Modal & Form State
const showModal = ref(false);
const selectedRole = ref<any>(null);

const openCreateModal = () => {
    selectedRole.value = null;
    showModal.value = true;
};

const openEditModal = (role: any) => {
    selectedRole.value = role;
    showModal.value = true;
};

const handleFormSuccess = () => {
    showModal.value = false;
    refreshTable();
};

const deleteRole = async (role: any) => {
    try {
        await axios.delete(`${admin.ROLES_API}/${role.id}`);
        toast.add({ severity: 'success', summary: 'Success', detail: 'Role deleted successfully', life: 3000 });
        refreshTable();
    } catch (error) {
        console.error('Error deleting role:', error);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete role', life: 3000 });
    }
};

const handleTableAction = (event: any) => {
    switch (event.type) {
        case 'create':
            openCreateModal();
            break;
        case 'edit':
            openEditModal(event.row);
            break;
        case 'delete':
            deleteRole(event.row);
            break;
    }
};

const refreshTable = () => {
    if (tableRef.value) {
        tableRef.value.filterData();
    }
};
</script>

<template>
    <div class="space-y-4">
        <AppDataTable ref="tableRef" :config="config" @action="handleTableAction" />

        <AppModal v-model:visible="showModal" :header="selectedRole ? 'Edit Role' : 'Create Role'" width="50rem">
            <RoleForm :role="selectedRole" @success="handleFormSuccess" @cancel="showModal = false" />
        </AppModal>
    </div>
</template>
