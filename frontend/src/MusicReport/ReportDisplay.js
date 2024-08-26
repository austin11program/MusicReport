import React, { useEffect, useState, useContext, createContext } from 'react';
import axios from 'axios';
import { DataContext } from './Report';
import './ReportDisplay.css';



function ReportDisplay() {

    const { songTime, artistTime, songData, currentCard, setArtistData, artistData, cardDesign } = useContext(DataContext);

    const [displaySongs, setDisplaySongs] = useState([])
    const [displayArtists, setDisplayArtists] = useState([])

    useEffect(() => {
        let items = [...songData]
            .filter(song => song.term === songTime) // Filter based on the term
            .sort((a, b) => a.rank - b.rank);
        setDisplaySongs(items);
    }, [songData, songTime])

    useEffect(() => {
        let items = [...artistData]
            .filter(artist => artist.term === artistTime) // Filter based on the term
            .sort((a, b) => a.rank - b.rank);
        setDisplayArtists(items);
    }, [artistData, artistTime])

    return (

        <>
            <div style={{ backgroundColor: cardDesign.color }} class="row musicreportcard">
                <ul class="col-lg-6">
                    <h1 className="header">{cardDesign.name}</h1>
     
                    <h1 className="header">Songs</h1>
                    {
                        displaySongs.length > 0 ?
                            displaySongs.map((e) => (
                                <>
                               <h1 className="textsize" key={e.rank}>{e.name}</h1>
                                </>
                            ))
                            :
                            <h1>Empty</h1>
                    }
                    <h1 className="header">Artists</h1>
                    {
                        displayArtists.length > 0 ?
                            displayArtists.map((e) => (
                                <>
                               <h1 className="textsize" key={e.rank}>{e.name}</h1>
                                </>
                            ))
                            :
                            <h1>No</h1>
                    }
                </ul>
                <div class="col-lg-6">
                    <img class="bigimage" src={cardDesign.image} alt="Card Design Image" />
                    <h5 className="header">{
                        cardDesign.imagetext
                    }</h5>
                </div>
            </div>

        </>
    )
}

export default ReportDisplay

// cardDesign.imagemeta.substring(0,6) == "song__" ?
//     <h5>Featured Song</h5> :
//     <h5>Me</h5>