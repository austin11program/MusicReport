import React, { useEffect, useState, createContext } from 'react';
import { useLocation } from 'react-router-dom';

import axios from 'axios';
import ReportDisplay from './ReportDisplay';
import LoginScreen from './ReportLoginScreen';
import ReportButtons from './ReportButtons';
import api from './api';


export const DataContext = createContext();

function Report() {

    const [userId, setUserId] = useState([""])
    const [demoActive, setDemoActive] = useState("")

    const [songData, setSongData] = useState(["", "", ""])
    const [artistData, setArtistData] = useState(["", "", ""])
    const [songTime, setSongTime] = useState("")
    const [artistTime, setArtistTime] = useState("")

    const [currentCard, setCurrentCard] = useState("My First Card")
    const [cardDesign, setCardDesign] = useState({ "color": "lightblue", "name": "My First Card" })

    const [initalized, setInitalized] = useState(false)
    const [loggedIn, setLoggedIn] = useState(false)
    const [token, setToken] = useState(false)

    useEffect(() => {
        if (token) {
            setLoggedIn(true)
        }
    }, [token])

    useEffect(() => {
        const fetchData = async () => {
            try {
                if (loggedIn) {
                    const response = await api.get('/musicreport/userStats/', {
                        params: {
                            name: currentCard,
                            demo : false
                        }
                    });
                    setDemoActive("user")
                    setSongData(response.data.songs);
                    setArtistData(response.data.artists);
                    setArtistTime("short_term")
                    setSongTime("short_term")
                    setUserId(response.data.userId)
                    setInitalized(true)
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
        fetchData()
    }, [loggedIn])

    const handleChange = () => {
        console.log("demo")
        const fetchDemo = async () => {
            try {

                const response = await api.get('/musicreport/demopage/', {
                    params: {
                        name: 'demo_music_report_id_USER_DATA%',
                        userId: "demo_music_report_id"
                    }
                });
                setSongData(response.data.songs);
                setArtistData(response.data.artists);
                setArtistTime("short_term")
                setSongTime("short_term")
                setUserId(response.data.userId)
                setCurrentCard("demo_music_report_id_USER_DATA%")
                console.log("Done")
                setDemoActive("demo")
                setInitalized(true)

            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
        fetchDemo()
    };

    return (
        <>
            <div className="d-flex justify-content-center">
                <h1 className="p-5">Report</h1>
            </div>

            <DataContext.Provider value={{ userId,initalized,demoActive, setInitalized, songData, setSongData, artistData, setArtistData, setToken, token, currentCard, setCurrentCard, cardDesign, setCardDesign, artistTime, setArtistTime, songTime, setSongTime }}  >

                <div className="row">
                    {
                        loggedIn || demoActive ?
                            (
                                <>
                                    <div className="col-lg-6 d-flex justify-content-end">
                                        <ReportDisplay></ReportDisplay>
                                    </div>
                                    {/* <div className="col-lg-1"></div> */}
                                    <div className="col-lg-5 ms-5 ">
                                        <ReportButtons></ReportButtons>
                                    </div>
                                </>
                            ) :
                            (<div className="col-lg-12">
                                <LoginScreen changeState={handleChange}> </LoginScreen>
                            </div>
                            )
                    }
                </div>
            </DataContext.Provider>

        </>
    )
}

export default Report