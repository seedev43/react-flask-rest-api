import React from 'react'
import { useNavigate } from 'react-router-dom'

const Home = () => {
  let navigate = useNavigate()

  const routes = (routeName = '') => {
    if(routeName === 'tiktok') {
      navigate('/tiktokdl')
    } else if(routeName === 'convert-page') {
      navigate('/convert-word-to-pdf')
    }
  }

  return (
    <>
    <button className='btn btn-custom' onClick={ () => routes('tiktok') }>TikTok Downloader</button>
    <button className='btn btn-custom' onClick={ () => routes('convert-page') }>Convert File Word To PDF</button>
    </>
  )
}

export default Home