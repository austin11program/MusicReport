import React, { useState, useContext } from 'react';
import axios from 'axios';
import { DataContext } from './Report';
import './ReportControls.css';


const SearchComponent = () => {

    const { setCurrentCard, setCardDesign, setArtistTime, setSongTime } = useContext(DataContext)

    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [hide, setHide] = useState(true);

    const handleSearch = async (e) => {
        setQuery(e.target.value);
        try {
            const response = await axios.get("http://localhost:8000/musicreport/searchquery/", {
                params: {
                    name: e.target.value
                }
            });
            setResults(response.data.results);
        } catch (error) {
            console.error("Error fetching search results:", error);
        }
    };

    const handleSelectResult = async (result) => {
        try {
            const response = await axios.get("http://localhost:8000/musicreport/getCard/", {
                params: {
                    name: result
                }
            });

            setCurrentCard(response.data.name); 
            setCardDesign(response.data.design);
            setSongTime(response.data.songTime);
            setArtistTime(response.data.artistTime);
            setQuery(""); 
            setResults([]);
        } catch (error) {
            console.error("Error selecting result:", error);
        }
    };

    const handleBlur = () => {
        setTimeout(() => setHide(true), 200);
    };

    const handleFocus = () => {
        setHide(false)
    };


    return (
        <div>
            <input
                type="text"
                value={query}
                onChange={handleSearch}
                placeholder="Search..."
                onBlur={handleBlur}
                onFocus={handleFocus}
                class="reportinput" 
            />

            {results.length > 0 && !hide && (
                <>
                    {
                        results.map((result, index) => (
                            <h5
                                key={index}
                                className=" reportresults"
                                onClick={() => handleSelectResult(result.name)}>
                                {result.name}
                                </h5>
                        ))}
                </>
            )}
        </div>
    );
};

export default SearchComponent;
