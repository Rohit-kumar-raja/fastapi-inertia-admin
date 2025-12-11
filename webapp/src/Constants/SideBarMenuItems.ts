import { ref } from "vue";

export const SideBarMenuItems = ref([
    {
        label: 'Dashboard',
        icon: 'house',
        route: '/dashboard'
    },

    {
        label: 'Projects',
        icon: 'folder',
        items: [
            { label: 'Construction', route: '/projects/construction' },
            { label: 'Maintenance', route: '/projects/maintenance' }
        ]
    },
    {
        label: 'Analytics',
        icon: 'chart-bar',
        route: '/analytics'
    },
    {
        label: 'Reports',
        icon: 'file',
        route: '/reports'
    },
    {
        separator: true
    },
    {
        label: 'Companies',
        icon: 'building',
        badge: 17,
        route: '/companies'
    },
    {
        label: 'People',
        icon: 'users',
        badge: 164,
        route: '/people'
    },
    {
        label: 'Settings',
        icon: 'cog',
        route: '/settings'
    },
    {
        separator: true
    },
    {
        label: 'Administration',
        icon: 'shield-halved',
        items: [
            { label: 'Users', route: '/admin/users' },
            { label: 'Roles', route: '/admin/roles' }
        ]
    }
]);