import React, { useEffect, useState, createContext } from 'react';
import UserStats from './UserStats';
import CardSelect from './CardSelect';
import DesignEdit from './DesignEdit';
import './ReportControls.css';

export const DataContext = createContext();


function ReportButtons() {


    return (

        <>
            <div class="d-flex flex-column justify-content-start fullpage" >

                <UserStats></UserStats>
                <CardSelect></CardSelect>
                <DesignEdit></DesignEdit>

            </div>


        </>
    )
}

export default ReportButtons