import React, { useEffect, useState, createContext } from 'react';
import './Home.css'

export const DataContext = createContext();

function Home() {


    return (
        <>
            <div className="row mt-5">

                <div className="col-lg-2">

                </div>
                <div className="col-lg-4 d-flex justify-content-start flex-column">
                    <h1 className="headertext">Austin Nguyen</h1>
                    <h1 className="subheader" >Student at University of Texas</h1>
                    <h1 className="bodytext">Hi, I'm Austin. I'm seeking a summer 2025 internship and other
                        tech opportunities.
                    </h1>
                    <a href="mailto:austinnguyennn@gmail.com?" className="profilebutton">Contact Me</a>

                    <div class="icon-container">
                        <a href="https://www.linkedin.com/in/austin-nguyen-ut/" target="_blank" class="icon" title="LinkedIn">
                            <img src="linkedin.png" alt="LinkedIn" />
                        </a>
                        <a href="mailto:austinnguyennn@gmail.com" target="_blank" class="icon" title="Email">
                            <img src="emailicon.jpeg" alt="Email" />
                        </a>
                        <a href="https://gitlab.com/austinnguyennn" target="_blank" class="icon" title="GitLab">
                            <img src="gitlabicon.png" alt="GitLab" />
                        </a>
                        <a href="https://github.com/austin11program" target="_blank" class="icon" title="GitHub">
                            <img src="githubicon.png" alt="GitHub" />
                        </a>

                    </div>
                </div>

                <img className="col-lg-3 circle-photo" src="IMG_3827.jpeg">

                </img>



            </div>
        </>
    )
}

export default Home