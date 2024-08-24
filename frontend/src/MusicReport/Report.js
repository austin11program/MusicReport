import React, { useEffect, useState, createContext } from 'react';
import { useLocation } from 'react-router-dom';

import axios from 'axios';
import ReportDisplay from './ReportDisplay';
import LoginScreen from './ReportLoginScreen';
import ReportButtons from './ReportButtons';

export const DataContext = createContext();

function Report() {

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
                    const response = await axios.get('http://localhost:8000/musicreport/userStats/', {
                        params: {
                            name: currentCard
                        }
                    });
                    setSongData(response.data.songs);
                    setArtistData(response.data.artists);
                    setArtistTime("short_term")
                    setSongTime("short_term")
                    setInitalized(true)
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
        fetchData()
    }, [loggedIn])




    return (
        <>
            <div className="d-flex justify-content-center">
                <h1 className="p-5">Report</h1>
            </div>

            <DataContext.Provider value={{ initalized, setInitalized, songData, setSongData, artistData, setArtistData, setToken, token, currentCard, setCurrentCard, cardDesign, setCardDesign, artistTime, setArtistTime, songTime, setSongTime }}  >

                <div className="row">
                    {
                        loggedIn ?
                            (
                                <>
                                    <div className="col-lg-6 d-flex justify-content-end">
                                        <ReportDisplay></ReportDisplay>
                                    </div>
                                    <div className="col-lg-1"></div>
                                    <div className="col-lg-4 ">
                                        <ReportButtons></ReportButtons>
                                    </div>
                                </>
                            ) :
                            (<div className="col-lg-12">
                                <LoginScreen> </LoginScreen>
                            </div>
                            )
                    }
                </div>
            </DataContext.Provider>

        </>
    )
}

export default Report