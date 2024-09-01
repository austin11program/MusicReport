import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import './ReportControls.css';
import { DataContext } from './Report';
import api from './api';

function UserStats() {

    const { userId, initalized, demoActive, setInitalized, setCardDesign, currentCard, artistTime, setArtistTime, songTime, setSongTime } = useContext(DataContext);

    useEffect(() => {
        const fetchData = async () => {
            if (initalized) {
                try {
                    const response = await api.get('/musicreport/setsongrange/', {
                        params: {
                            range: songTime,
                            name: currentCard,
                            userId: userId,
                            demo: demoActive
                        }
                    });
                    setCardDesign(response.data.design)
                } catch (error) {
                    console.error("Error fetching data:", error);
                }
            }

        };
        fetchData();
    }, [songTime]);

    useEffect(() => {
        const fetchData = async () => {
            if (initalized) {
                try {
                    const response = await api.get('/musicreport/setartistrange/', {
                        params: {
                            range: artistTime,
                            name: currentCard,
                            userId: userId,
                            demo: demoActive
                        }
                    });

                } catch (error) {
                    console.error("Error fetching data:", error);
                }
            }

        };
        fetchData();
    }, [artistTime]);

    return (
        <>
            <div className ="mb-4">
                <h1 className="header">Artists Range</h1>
                <div class="d-flex flex-row justify-content-start align-items-start" >

                    <button
                        type="button"
                        class="btn btn-secondary reportbutton"
                        id="dsf"
                        name="artistRange"
                        value="long_term"
                        onClick={() => setArtistTime("long_term")}
                    >1 year</button>
                    <button
                        type="button"
                        class="btn btn-secondary reportbutton "
                        name="artistRange"
                        value="long_term"
                        onClick={() => setArtistTime("medium_term")}
                    >6 months</button>
                    <button
                        type="button"
                        class="btn btn-secondary reportbutton "
                        name="artistRange"
                        value="long_term"
                        onClick={() => setArtistTime("short_term")}
                    >1 month</button>
                </div>
            </div>
            <div className = 'mb-4'>
                <h1 className="header">Song Range</h1>
                <div class="d-flex flex-row justify-content-start align-items-start" >

                    <button
                        type="button"
                        class="btn btn-secondary reportbutton"
                        name="songRange"
                        value="long_term"
                        onClick={() => setSongTime("long_term")}
                    >1 year</button>
                    <button
                        type="button"
                        class="btn btn-secondary reportbutton"
                        name="songRange"
                        value="long_term"
                        onClick={() => setSongTime("medium_term")}
                    >6 months</button>
                    <button
                        type="button"
                        class="btn btn-secondary reportbutton"
                        name="songRange"
                        value="long_term"
                        onClick={() => setSongTime("short_term")}
                    >1 month</button>
                </div>
            </div>
        </>
    )
}

export default UserStats