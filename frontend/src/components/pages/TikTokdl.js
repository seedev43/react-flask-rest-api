import React, { useState } from 'react'

const TikTokdl = () => {
  const [tiktokUrl, setTiktokUrl] = useState("")
  const [message, setMessage] = useState({})
  const [result, setResult] = useState({})
  const [buttonDisable, setButtonDisable] = useState(false)
  const [alert, setAlert] = useState(false)

  const showAlert = () => {
    let typeAlert = ""
    
    if(!message.success) {
      typeAlert = "alert danger"
    } else {
      typeAlert = "alert success"
    }
    return <div className={ typeAlert }>{ message.msg }</div>
  }

  const TikTokDownloader = async(event) => {
    event.preventDefault()

    setResult({})
    setAlert(false)
    setButtonDisable(true)
    
    try {

      if(tiktokUrl.trim().length === 0) {
          setMessage({"success": false, "msg": "Url is required"})
          setAlert(true)
          setButtonDisable(false)

      } else {

        let exc = await fetch("/api/tiktokdl", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded"
          },
          body: `url=${tiktokUrl}`
        })
        let res = await exc.json()
        if(res.success) {
          setResult(res)
          setMessage(res)
          setAlert(true)
          setButtonDisable(false)
        } else {
          setMessage(res)
          setAlert(true)
          setButtonDisable(false)
        }
      }

    } catch(error) {
      setMessage(error.message)
      setAlert(true)
      setButtonDisable(false)
    }

  }
  return (
    <div>
      <h5 className="text-center">TikTok Downloader</h5>
      <form onSubmit={ TikTokDownloader }>
      { alert && showAlert() }
        
        <input type="text" className="form-input" name="link_url" value={tiktokUrl} onChange={(element) => setTiktokUrl(element.target.value)} placeholder="Ex: https://vt.tiktok.com/ZSwWCk5o"/>
        <button disabled={ buttonDisable } className="btn btn-custom">Submit</button>
      </form>
        { result.success && (<div>
          <hr/>
          { result.links.map((link, index) => (
            <>
            <a href={ link } key={ index } target="_blank" rel="noopener noreferrer"><button className="btn btn-custom">Download Now [{ index + 1 }]</button></a>
            </>
          )) }
          </div>
        ) }
    </div>
  )
}

export default TikTokdl