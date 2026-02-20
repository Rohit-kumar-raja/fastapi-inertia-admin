import { ref } from "vue";
import {
    faHouse, faFolder, faChartBar, faFile, faBuilding, faUsers, faCog
} from "@fortawesome/free-solid-svg-icons";

export const SideBarMenuItems = ref([
    {
        label: 'Dashboard',
        icon: faHouse,
        route: '/admin/dashboard'
    },

    {
        label: 'Projects',
        icon: faFolder,
        items: [
            { label: 'Construction', route: '/projects/construction' },
            { label: 'Maintenance', route: '/projects/maintenance' }
        ]
    },
    {
        label: 'Analytics',
        icon: faChartBar,
        route: '/analytics'
    },
    {
        label: 'Reports',
        icon: faFile,
        route: '/reports'
    },
    {
        separator: true
    },
    {
        label: 'Companies',
        icon: faBuilding,
        badge: 17,
        route: '/companies'
    },
    {
        label: 'People',
        icon: faUsers,
        badge: 164,
        route: '/people'
    },
    {
        label: 'Settings',
        icon: faCog,
        route: '/admin/settings'
    },
    {
        separator: true
    },
    {
        label: 'Administration',
        icon: faUsers,
        items: [
            { label: 'Users', route: '/admin/administration/users' },
            { label: 'Roles', route: '/admin/administration/roles' }
        ]
    }
]);