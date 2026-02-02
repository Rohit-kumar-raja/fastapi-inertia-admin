<script setup lang="ts">
import AppDataTable from '@/Components/AppDataTable.vue';
import { admin } from '@/core';
import AdminLayout from '@/Layouts/AdminLayout.vue';

const tempData = {
    title: "Tag Groups",
    dataApi: admin.USERS_API, // API for table fetch
    headers: [
        {
            field: "s_no",
            label: "S.No.",
            filter: false,
            sortable: false,
            class: "w-[5%]",
        },
        {
            field: "name",
            label: "Name",
        },
    ],
    export: {
        columns: ["id", "name",],

    }

}


</script>

<template>
    <AppDataTable :config="tempData" >

    </AppDataTable>
</template>