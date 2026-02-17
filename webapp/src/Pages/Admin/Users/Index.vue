<script setup lang="ts">
import AppDataTable from '@/Components/AppDataTable.vue';
import { admin } from '@/core';

const tempData = {
    title: "Users",
    dataApi: admin.USERS_FILTER_API, // API for table fetch
    headers: [
        {
            field: "s_no",
            label: "S.No.",
            filter: false,
            sortable: false,
            class: "w-[5%]",
        },
        {
            field: "username",
            label: "Username",
        },
        {
            field: "email",
            label: "Email",
        },
        {
            field: "roles",
            label: "Roles",
        },
        {
            field: "is_active",
            label: "Status",

        }
    ],
    export: {
        columns: ["id", "email",],

    }

}


</script>

<template>
    <AppDataTable :config="tempData">

        <template #roles="{ data }">
            <div class="flex gap-2">
                <Tag v-for="role in data.roles" :key="role.id">
                    {{ role.name }}
                </Tag>
            </div>
        </template>
    </AppDataTable>
</template>