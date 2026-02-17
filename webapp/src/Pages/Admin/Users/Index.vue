<script setup lang="ts">
import AppDataTable from '@/Components/AppDataTable.vue';
import AppModal from '@/Components/AppModal.vue';
import UserForm from './Form.vue';
import { admin } from '@/core';
import { ref } from 'vue';
import axios from 'axios';
import { useToast } from 'primevue/usetoast';

const toast = useToast();
const tableRef = ref();

const config = {
    title: "Users",
    dataApi: admin.USERS_FILTER_API,
    headers: [
        { field: "s_no", label: "S.No.", filter: false, sortable: false, class: "w-[5%]" },
        { field: "username", label: "Username" },
        { field: "email", label: "Email" },
        { field: "roles", label: "Roles" },
        { field: "is_active", label: "Status" }
    ],
    export: { columns: ["id", "email"] },
    actions: {
        addRecord: { isEnabled: true },
        editRecord: { isEnabled: true },
        deleteRecord: { isEnabled: true }
    }
};

// Modal & Form State
const showModal = ref(false);
const selectedUser = ref<any>(null);

const openCreateModal = () => {
    selectedUser.value = null;
    showModal.value = true;
};

const openEditModal = (user: any) => {
    selectedUser.value = user;
    showModal.value = true;
};

const handleFormSuccess = () => {
    showModal.value = false;
    refreshTable();
};

const deleteUser = async (user: any) => {
    try {
        await axios.delete(`${admin.USERS_API}/${user.id}`);
        toast.add({ severity: 'success', summary: 'Success', detail: 'User deleted successfully', life: 3000 });
        refreshTable();
    } catch (error) {
        console.error('Error deleting user:', error);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete user', life: 3000 });
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
            deleteUser(event.row);
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
        <AppDataTable ref="tableRef" :config="config" @action="handleTableAction">
            <template #roles="{ data }">
                <div class="flex gap-2 flex-wrap">
                    <Tag v-for="role in data.roles" :key="role.id" :value="role.name" severity="info" rounded></Tag>
                </div>
            </template>
            <template #is_active="{ data }">
                <Tag :value="data.is_active ? 'Active' : 'Inactive'" :severity="data.is_active ? 'success' : 'danger'"
                    rounded></Tag>
            </template>
        </AppDataTable>

        <AppModal v-model:visible="showModal" :header="selectedUser ? 'Edit User' : 'Create User'" width="50rem">
            <UserForm :user="selectedUser" @success="handleFormSuccess" @cancel="showModal = false" />
        </AppModal>
    </div>
</template>