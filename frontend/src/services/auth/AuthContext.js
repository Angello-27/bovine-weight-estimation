// frontend\src\services\auth\AuthContext.js

import React, { createContext, useContext, useEffect, useState } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth must be used within AuthProvider');
    return context;
};

export const AuthProvider = ({ children }) => {

    const [id, setID] = useState(() => {
        return sessionStorage.getItem('id');
    });

    const [username, setUsername] = useState(() => {
        return sessionStorage.getItem('username');
    });

    const [role, setRole] = useState(() => {
        return sessionStorage.getItem('role');
    });

    useEffect(() => {
        if (id) sessionStorage.setItem('id', id);
        else sessionStorage.removeItem('id');

        if (username) sessionStorage.setItem('username', username);
        else sessionStorage.removeItem('username');

        if (role) sessionStorage.setItem('role', role);
        else sessionStorage.removeItem('role');

    }, [id, username, role]);

    const login = (id, username, role) => {
        setID(id);
        setUsername(username);
        setRole(role);
    };

    const logout = () => {
        setID(null);
        setUsername(null);
        setRole(null);
    };

    return (
        <AuthContext.Provider value={{ id, username, role, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
