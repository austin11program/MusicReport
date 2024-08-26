import React, { useEffect, useState, createContext, useContext } from 'react';
import UserStats from './UserStats';
import axios from 'axios';
import { DataContext } from './Report';
import SearchComponent from './SearchComponent';
import './ReportControls.css';
import api from './api';


function CardSelect() {

    const { currentCard, setCurrentCard, setCardDesign, setArtistTime, setSongTime } = useContext(DataContext)

    const [newName, setNewName] = useState("")
    const [showInputs, setShowInputs] = useState(false)

    const [nameQuery, setNameQuery] = useState("")

    const handleDelete = async () => {
        try {
            const response = await api.get("/musicreport/deleteCurrentCard/", {
                params: {
                    name: currentCard
                }
            });
            if (response.data.error) {
                return
            }
            setCurrentCard(response.data.name); // Accessing 'name' from the 'data' object
            setCardDesign(response.data.design);
            setArtistTime(response.data.artistTime)
            setSongTime(response.data.songTime)
        } catch (error) {
            console.error("Error deleting the card:", error);
        }
    }

    const handleCreate = () => {
        if (!showInputs) {
            setShowInputs(true)
            return
        }
        setShowInputs(false)
    }

    const handleSubmit = async () => {
        try {
            const response = await api.get("/musicreport/createNewCard/", {
                params: {
                    name: newName
                }
            })

            setCurrentCard(response.data.name); // Accessing 'name' from the 'data' object
            setCardDesign(response.data.design);

            setSongTime(response.data.songTime)
            setArtistTime(response.data.artistTime)

            setNewName("")
            setShowInputs(false)
        } catch (error) {
            console.error("Error creating new card:", error);
        }
    }

    return (

        <>
            <div className="mb-4">
                <h1 className="header">Report Select</h1>





                <div class="d-flex flex-row justify-content-start align-items-start" >
                    <button
                        type="button"
                        onClick={handleDelete}
                        class="btn btn-secondary reportbutton"
                    >Delete Report</button>

                    <div class="d-flex flex-column justify-content-start ">
                        <button
                            type="button"
                            onClick={handleCreate}
                            class="btn btn-secondary reportbutton createNew "
                        >Create New</button>

                        {showInputs && (<>


                                <input
                                    onChange={(e) => setNewName(e.target.value)}
                                    placeholder='enter new card name'
                                    class="reportinput createNew"

                                ></input>
                                <button
                                    onClick={handleSubmit}
                                    class="btn btn-secondary reportbutton createNew"
                                >Submit</button>
                        </>
                        )}


                    </div>
                    <SearchComponent></SearchComponent>


                </div>
            </div>

        </>
    )
}

export default CardSelect;