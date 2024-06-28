import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

import Home from './components/pages/Home'
import TikTokdl from './components/pages/TikTokdl'
import Cvw2pdf from './components/pages/Cvw2pdf'

import './css/style.css'
import './css/alerts.css'

const App = () => {
  return (
    <BrowserRouter>
      <div className='container'>
        <div className='body'>
          <h1 className='title'>TKTDW API</h1>
          <h2 className='title'>Social Media Content Scraper</h2>
          <Routes>
            <Route index element={<Home/>} />
            <Route path="/tiktokdl" element={<TikTokdl/>} />
            <Route path="/convert-word-to-pdf" element={<Cvw2pdf/>} />
          </Routes>

        </div>
      </div>
    </BrowserRouter>
  )
}

export default App