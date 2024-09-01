import React, { useEffect, useState, createContext, useContext } from 'react';
import axios from 'axios';
import { DataContext } from './Report';
import './ReportControls.css';
import api from './api';


function DesignEdit() {

    const { userId, songTime, demoActive, artistTime, currentCard, setCardDesign, cardDesign } = useContext(DataContext);

    const [hide, setHide] = useState(true)
    const [imageList, setImageList] = useState([])

    useEffect(() => {

        const fetchImages = async () => {
            try {
                const response = await api.get("/musicreport/imagelist/", {
                    params: {
                        name: currentCard,
                        songRange: songTime,
                        artistRange: artistTime,
                        userId: userId,
                        demo: demoActive
                    }
                });
                setImageList(response.data.data)
            }
            catch (e) {
                console.log("error in fetching image results", e)
            }
        };
        fetchImages()

    }, [artistTime, songTime])

    const handleImageSelect = async (e) => {
        try {
            const response = await api.get("/musicreport/setdesignimage/", {
                params: {
                    type: e.type,
                   id: e.id,
                  name: currentCard,
                  userId: userId,
                   demo: demoActive
                }
            });
            setCardDesign(response.data.design)

        } catch (e) {
            console.log("error in fetching image select", e)
        }
    }

    const handleSelect = () => {
        if (!hide) {
            setHide(true)
            return
        }
        setHide(false)
    }



    return (

        <>
            <h1 className="header">Design Edit</h1>
            <div class="d-flex flex-row justify-content-start align-items-start" >


                <div class="d-flex flex-column ">
                    <button
                        type="button"
                        class="btn btn-secondary reportbutton fixedwidth"
                        onClick={handleSelect}
                    >Change Image
                    </button>
                    <div class="row">

                        {hide && (
                            imageList.map((e, index) => (
                                (
                                    <div key={index} class="col-lg-2 ">
                                        <img src={e.image} className="designEditImage" onClick={() => handleImageSelect(e)} />
                                    </div>
                                )
                            ))
                        )
                        }
                    </div>
                </div>

            </div>



        </>
    )
}

export default DesignEdit;

