"use client";
import { useAuth } from "@/contexts/AuthContext";
import { ReactNode } from "react";

interface RoleGuardProps {
    children: ReactNode;
    requiredRoles?: string[];
    fallback?: ReactNode;
    requireAll?: boolean; // If true, requires ALL roles in requiredRoles (rare, usually 'any')
}

export function RoleGuard({ children, requiredRoles = [], fallback = null, requireAll = false }: RoleGuardProps) {
    const { user, hasRole } = useAuth();

    // If no user, we can't verify roles.
    // If AuthGuard is used upstream, this might technically be unreachable, 
    // but safe to return fallback.
    if (!user) {
        return <>{fallback}</>;
    }

    if (requiredRoles.length === 0) {
        return <>{children}</>;
    }

    let hasAccess = false;

    // Check for Super Admin bypass implicitly handled by hasRole('ADMIN') logic inside AuthContext 
    // or we check explicit matches here.

    if (requireAll) {
        hasAccess = requiredRoles.every(role => hasRole(role));
    } else {
        hasAccess = requiredRoles.some(role => hasRole(role));
    }

    if (hasAccess) {
        return <>{children}</>;
    }

    return <>{fallback}</>;
}
