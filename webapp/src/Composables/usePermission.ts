import { computed, ref } from 'vue'

/**
 * In-memory permission state for the current user.
 * Shared across all components using the composable.
 */
const permissions = ref<string[]>([])
const isSuperAdmin = computed(() => permissions.value.includes('*'))

/**
 * Vue composable for permission checking.
 *
 * Usage:
 *   const { hasPermission, hasAnyPermission, isSuperAdmin } = usePermission()
 *   if (hasPermission('admin.user.write')) { ... }
 */
export function usePermission() {
    /**
     * Load permissions from the login response or localStorage.
     */
    function loadPermissions(perms: string[]) {
        permissions.value = perms
        localStorage.setItem('user_permissions', JSON.stringify(perms))
    }

    /**
     * Initialize permissions from localStorage (e.g. on page reload).
     */
    function initPermissions() {
        const stored = localStorage.getItem('user_permissions')
        if (stored) {
            try {
                permissions.value = JSON.parse(stored)
            } catch {
                permissions.value = []
            }
        }
    }

    /**
     * Clear all permissions (e.g. on logout).
     */
    function clearPermissions() {
        permissions.value = []
        localStorage.removeItem('user_permissions')
    }

    /**
     * Check if the user has a specific permission.
     * SuperAdmins (permission = '*') bypass all checks.
     */
    function hasPermission(permission: string): boolean {
        if (isSuperAdmin.value) return true
        return permissions.value.includes(permission)
    }

    /**
     * Check if the user has ANY of the specified permissions.
     */
    function hasAnyPermission(...permissionList: string[]): boolean {
        if (isSuperAdmin.value) return true
        return permissionList.some((p) => permissions.value.includes(p))
    }

    /**
     * Check if the user has ALL of the specified permissions.
     */
    function hasAllPermissions(...permissionList: string[]): boolean {
        if (isSuperAdmin.value) return true
        return permissionList.every((p) => permissions.value.includes(p))
    }

    return {
        permissions: computed(() => permissions.value),
        isSuperAdmin,
        loadPermissions,
        initPermissions,
        clearPermissions,
        hasPermission,
        hasAnyPermission,
        hasAllPermissions,
    }
}
