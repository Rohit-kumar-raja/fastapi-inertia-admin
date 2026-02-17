<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { router } from '@inertiajs/vue3';

const tempData = {
    title: "Roles",
    columns: [
        {
            field: "name",
            header: "Name",
            sortable: true
        },
        {
            field: "description",
            header: "Description",
            sortable: true
        },
        {
            field: "created_at",
            header: "Created At",
            sortable: true
        },
        {
            field: "updated_at",
            header: "Updated At",
            sortable: true
        }
    ],
    actions: [
        {
            label: "Edit",
            icon: "pi pi-pencil",
            action: (event: any) => {
                router.visit(`/admin/roles/${event.data.id}/edit`);
            }
        },
        {
            label: "Delete",
            icon: "pi pi-trash",
            action: (event: any) => {
                router.visit(`/admin/roles/${event.data.id}`);
            }
        }
    ]
}

</script>

<template>
    <AppDataTable :config="tempData" />
</template>
