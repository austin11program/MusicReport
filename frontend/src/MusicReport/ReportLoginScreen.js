import React, { useEffect, useState, createContext } from 'react';
import LoginButton from './aDebug';
import './Login.css';
import AboutProject from './AboutProject';

function LoginScreen({ changeState }) {

    return (
        <>
            <div class="d-flex flex-column justify-content-center align-items-center" >
                <div className="d-flex mb-5">
                    <LoginButton redirectUrl="https://musicreportfrontend-git-main-austin11programs-projects.vercel.app/musicreport"></LoginButton>
                    <button className='btn btn-danger loginbutton ms-5'
                        onClick={changeState}>
                        Demo
                    </button>
                </div>
                <AboutProject></AboutProject>
            </div>
        </>
    )
}

export default LoginScreen