"use client";
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { jwtDecode } from 'jwt-decode';

interface UserProfile {
    id: string;
    sub: string;
    roles: string[];
    name?: string;
}

interface AuthContextType {
    user: UserProfile | null;
    token: string | null;
    login: (token: string) => void;
    logout: () => void;
    hasRole: (role: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<UserProfile | null>(null);
    const [token, setToken] = useState<string | null>(null);

    useEffect(() => {
        // Load from localStorage on mount
        const storedToken = localStorage.getItem('token');
        if (storedToken) {
            try {
                const decoded: any = jwtDecode(storedToken);
                // Check expiry if existing
                if (decoded.exp && decoded.exp * 1000 < Date.now()) {
                    logout();
                } else {
                    setToken(storedToken);
                    setUser({
                        id: decoded.sub,
                        sub: decoded.sub,
                        roles: decoded.role || decoded.roles || [], // Handle both 'role' and 'roles'
                        name: decoded.name || 'User'
                    });
                }
            } catch (e) {
                logout();
            }
        }
    }, []);

    const login = (newToken: string) => {
        localStorage.setItem('token', newToken);
        setToken(newToken);
        try {
            const decoded: any = jwtDecode(newToken);
            setUser({
                id: decoded.sub,
                sub: decoded.sub,
                roles: decoded.role || decoded.roles || [],
                name: decoded.name || 'User'
            });
        } catch (e) {
            console.error("Invalid token");
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
    };

    const hasRole = (role: string) => {
        if (!user) return false;
        const userRoles = user.roles || [];
        if (userRoles.includes('ADMIN') || userRoles.includes('SUPER_ADMIN')) return true; // Power users
        return userRoles.includes(role);
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout, hasRole }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
