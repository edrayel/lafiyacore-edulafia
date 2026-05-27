import { useAuthStore } from '../stores/authStore';
import { navSections } from '../config/navigation.config';

export const Perm = {
  VIEW_FINANCE:    'finance:view',
  VIEW_HEALTH:     'health:view',
  VIEW_ADMIN:      'admin:view',
  VIEW_PROPRIETOR: 'proprietor:view',
} as const;

type Permission = (typeof Perm)[keyof typeof Perm];

export const ROLE_PERMISSIONS: Record<string, Permission[] | ['*']> = {
  superadmin:      ['*'],
  owner:           ['*'],
  admin:           ['finance:view', 'health:view', 'admin:view', 'proprietor:view'],
  principal:       ['finance:view'],
  vice_principal:  ['finance:view', 'health:view'],
  nurse:           ['health:view'],
  health_officer:  ['health:view'],
  bursar:          ['finance:view'],
  accountant:      ['finance:view'],
};

export function hasPermission(perm: Permission | string): boolean {
  const user = useAuthStore.getState().user;
  if (!user) return false;
  const perms = ROLE_PERMISSIONS[user.role];
  if (!perms) return false;
  return (perms as string[]).includes('*') || (perms as string[]).includes(perm);
}

export function useNavPermissions() {
  const user = useAuthStore((s) => s.user);
  if (!user) return [];
  const perms = ROLE_PERMISSIONS[user.role];
  if (!perms) return [];

  return navSections
    .map((section) => ({
      ...section,
      items: section.items.filter((item) => {
        if (!('perm' in item) || !item.perm) return true;
        if ((perms as string[]).includes('*')) return true;
        return (perms as string[]).includes(item.perm as string);
      }),
    }))
    .filter((s) => s.items.length > 0);
}
