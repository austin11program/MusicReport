
import React, { useEffect, useState, createContext } from 'react';
import './Login.css';

function AboutProject() {


    return (
        <>

            <h1 className="header mt-3">About</h1>
            <p className="text body ">Music Report was created as a comprehensive application designed to manage databases and work with APIs</p>

            <h1 className="header mt-3">How to Use</h1>
            <p className="text body ">
                Use the Login button to login with spotify<br/>Use the Demo button for demostration
            </p>
            <img src='umlDiagram.jpg'></img>


        </>
    )
}

export default AboutProject


