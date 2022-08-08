import React, { useState } from 'react'

const Cvw2pdf = () => {

  const [selectedFile, setSelectedFile] = useState(null)
  const [buttonDisable, setButtonDisable] = useState(false)
  const [message, setMessage] = useState({})
  const [result, setResult] = useState({})
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

  const fileDataName = () => {
    if(selectedFile) {
      return (
        <>
          Filename: { selectedFile.name }
        </>
      )
    } else {
      return (
        <>
          No File Choosen
        </>
      )
    }
  }

  const uploadFile = async (event) => {
    event.preventDefault()

    setResult({})
    setAlert(false)
    setButtonDisable(true)
    

    try {
      if (selectedFile === null) {
        setMessage({"success": false, "msg": "File empty"})
        setAlert(true)
        setButtonDisable(false)
      } else {
        let typeFile = (/\.[0-9a-z]+$/i.exec(selectedFile.type)) ? /\.[0-9a-z]+$/i.exec(selectedFile.type)[0] : "etc"
        
        if(typeFile !== ".document") {
          setMessage({"success": false, "msg": "Only Document Files"})
          setAlert(true)
          setButtonDisable(false)
        } else {

          const form = new FormData()
          form.append("file", selectedFile)
          form.append("filename", selectedFile.name)

          const fetchApi = await fetch("/api/convert-word-to-pdf", {
            method: "POST",
            body: form
          })

          const response = await fetchApi.json()

          if(response.success) {
            setResult(response)
            setMessage(response)
            setAlert(true)
            setButtonDisable(false)
          } else {
            setMessage(response)
            setAlert(true)
            setButtonDisable(false)
          }
        }
      }
    } catch (error) {
      setMessage({"success": false, "msg": error.message})
      setAlert(true)
      setButtonDisable(false)
    }


  }

  return (
    <div>
      <h5 className="text-center">Convert File Word to PDF</h5>
        { alert && showAlert() }
      <form onSubmit={ uploadFile }>
        <div className="upload-btn-wrapper">
          <button className="btn-upload">Choose File</button>
          <label>{ fileDataName() }</label>
          <input type="file" name="file" onChange={ (event) => setSelectedFile(event.target.files[0]) } />
        </div>
        <button disabled={ buttonDisable } className="btn btn-custom">Convert Now</button>
      </form>
      {result.success && (
        <div>
          <hr/>
          <a href={result.download_url} target="_blank" rel="noopener noreferrer"><button className="btn btn-custom">Download File</button></a>

        </div>
      )}
    </div>
  )
}

export default Cvw2pdf