import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { DataContext } from './Report'; 
import './Login.css';


function LoginButton(props) { 

    const [codeRequest, setCodeRequest] = useState(false);
    const { setToken } = useContext(DataContext);

    const handleLogin = async () => {
        try {
            const response = await axios.get('http://localhost:8000/musicreport/login/', {
                params: {
                    redirectUrl: props.redirectUrl
                }            });
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
                    const response = await axios.get('http://localhost:8000/musicreport/getToken/', {
                        params: {
                            code: code,
                            redirectUrl: props.redirectUrl
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
    }, [props.redirectUrl]);

    return (
        <div>
            <button className ="btn btn-success loginbutton" onClick={handleLogin}>Login</button>
        </div>
    );
};

export default LoginButton;
