import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { DataContext } from './Report';
import './Login.css';
import api from './api';


function LoginButton() {

    const [codeRequest, setCodeRequest] = useState(false);
    const { setToken } = useContext(DataContext);

    const handleLogin = async () => {
        try {
            console.log(process.env.REACT_APP_REDIRECT_URL)
            console.log(process.env.REACT_APP_REDIRECT_URL)
            const response = await api.get('/musicreport/login/', {
                params: {
                    // redirectUrl: process.env.REACT_APP_REDIRECT_URL
                }
            });
            window.location.href = response.data.auth_url; // Redirect the browser
            setCodeRequest(true);
        } catch (error) {
            console.error('Error during login request:', error);
        }
    };

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        if (code) {
            const fetchToken = async () => {
                try {
                    console.log(process.env.REACT_APP_REDIRECT_URL)
                    const response = await api.get('/musicreport/getToken/', {
                        params: {
                            code: code,
                            // redirectUrl: process.env.REACT_APP_REDIRECT_URL
                        },
                        withCredentials: true
                    });
                    if (response.data.success) {
                        setToken(true);
                    }
                } catch (error) {
                    console.error('Error during token retrieval:', error);
                }
            };
            fetchToken();
        }
    }, []);

    return (
        <div>
            <button className="btn btn-success loginbutton" onClick={handleLogin}>Login</button>
        </div>
    );
};

export default LoginButton;
