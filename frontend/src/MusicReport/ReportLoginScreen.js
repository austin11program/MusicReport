import React, { useEffect, useState, createContext } from 'react';
import LoginButton from './aDebug';
import './Login.css';
import AboutProject from './AboutProject';

function LoginScreen() {


    return (
        <>
            <div class="d-flex flex-column justify-content-center align-items-center" >
                <div className="d-flex mb-5">
                    <LoginButton redirectUrl="report"></LoginButton>
                    <button className='btn btn-danger loginbutton ms-5'>
                        Demo
                    </button>
                </div>

                <AboutProject></AboutProject>



            </div>


        </>
    )
}

export default LoginScreen