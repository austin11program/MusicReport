import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import React from 'react';
import Home from './components/Home';
import Report from './MusicReport/Report'

function App() {
  return (
    <Router>

      {/* Navbar stays outside of the Routes */}
      <nav className="navbar navbar-expand-lg navbar-light bg-light ">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">Home</Link>
          {/* <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button> */}
          <div className=" navbar-collapse" id="navbarNavAltMarkup">
            <div className="navbar-nav">
              <Link className="nav-link" aria-current="page" to="/musicreport">Music Report</Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Routes for different pages */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/musicreport" element={< Report />} />
        <Route path="*" element={<><h1>Not Found</h1></>} /> {/* For handling 404 errors */}
      </Routes>
    </Router>
  );

}

export default App;
