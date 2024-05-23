import React from 'react'
import { useState } from 'react'
import axios from 'axios'

function Departments() {
  const [statePage, setStatePage] = useState(5)
  const [message, setMessage] = useState('')
  const [messageStatus, setMessageStatus] = useState(true)

  const createState = (e) => {
    e.preventDefault();
    setStatePage(0)
  }
  const readState = (e) => {
    e.preventDefault();
    setStatePage(1)
    readEvent()
  }
  const updateState = (e) => {
    e.preventDefault();
    setStatePage(2)
  }
  const deleteState = (e) => {
    e.preventDefault();
    setStatePage(3)
  }
  const createEvent = async (e) => {
    e.preventDefault();
    const list = []
    Array.from(e.target.elements).forEach((element)=>{list.push(element.value)})
    try {
      const res = await axios.post('http://127.0.0.1:8000/departments',{
        'DEPNO':list[0],
        'DNAME':list[1],
        'LOC':list[2]
      });
      console.log(res)
      
    } catch (e) {
      if(e.request.status == 422){
        setMessage('Se ingresaron los datos incorrectos')
        setMessageStatus(false)
      }
      if(e.request.status == 0)
      {
        setMessage('Error del servidor')
        setMessageStatus(false)
      }
      else {
        console.log(e)
      }
    }

  }
  const readEvent = async (e) => {
    try {
      const res = await axios.get(`http://127.0.0.1:8000/departments`);
      console.log(res)
      
    } catch (e) {
      if(e.request.status == 422){
        setMessage('Se ingresaron los datos incorrectos')
        setMessageStatus(false)
      }
      if(e.request.status == 0)
      {
        setMessage('Error del servidor')
        setMessageStatus(false)
      }
      else {
        console.log(e)
      }
    }
  }
  const updateEvent = async (e) => {
    e.preventDefault();
    const list = []
    Array.from(e.target.elements).forEach((element)=>{list.push(element.value)})
    try {
      const res = await axios.put(`http://127.0.0.1:8000/departments/${list[0]}`,{
        'DNAME':list[1],
        'LOC':list[2],
      });
      console.log(res)
      
    } catch (e) {
      if(e.request.status == 422){
        setMessage('Se ingresaron los datos incorrectos')
        setMessageStatus(false)
      }
      if(e.request.status == 0)
      {
        setMessage('Error del servidor')
        setMessageStatus(false)
      }
      else {
        console.log(e)
      }
    }
  }
  const deleteEvent = async (e) => {
    e.preventDefault();
    const list = []
    Array.from(e.target.elements).forEach((element)=>{list.push(element.value)})
    try {
      const res = await axios.delete(`http://127.0.0.1:8000/departments/${list[0]}`);
      console.log(res)
      
    } catch (e) {
      if(e.request.status == 422){
        setMessage('Se ingresaron los datos incorrectos')
        setMessageStatus(false)
      }
      if(e.request.status == 0)
      {
        setMessage('Error del servidor')
        setMessageStatus(false)
      }
      else {
        console.log(e)
      }
    }
  }



  return (
    <div>
      <header className=' p-2 text-lg'>
        <button className=' p-1 hover:bg-slate-200' onClick={createState}>Crear</button>
        <button className=' p-1 hover:bg-slate-200' onClick={deleteState}>Eliminar</button>
        <button className=' p-1 hover:bg-slate-200' onClick={updateState}>Modificar</button>
        <button className=' p-1 hover:bg-slate-200' onClick={readState}>Consultar</button>
      </header>
      {
        statePage == 0 ?
          <div>
            <form onSubmit={createEvent} className=' p-3'>
              <p>ID del departamento</p>
              <input className=' bg-slate-200' type='number'></input>
              <p>Nombre del departamento</p>
              <input className=' bg-slate-200' type='text'></input>
              <p>Localización del departamento</p>
              <input className=' bg-slate-200' type='text'></input>
              <button>Subir</button>
              {message ? messageStatus == true ?<p className=' text-green-500'>{message}</p>:<p className=' text-red-500'>{message}</p>:<></>}
            </form>
          </div>:
        statePage == 1 ? 
          <div>
            <p>Leer</p>
            {message ? messageStatus == true ?<p className=' text-green-500'>{message}</p>:<p className=' text-red-500'>{message}</p>:<></>}
          </div>:
        statePage == 2 ? 
        <div>
          <form onSubmit={updateEvent} className=' p-3'>
          <p>ID del departamento</p>
              <input className=' bg-slate-200' type='number'></input>
              <p>Nombre del departamento</p>
              <input className=' bg-slate-200' type='text'></input>
              <p>Localización del departamento</p>
              <input className=' bg-slate-200' type='text'></input>
              <button>Subir</button>
              {message ? messageStatus == true ?<p className=' text-green-500'>{message}</p>:<p className=' text-red-500'>{message}</p>:<></>}
            </form>
        </div>:
        statePage == 3 ? 
        <div>
          <form onSubmit={deleteEvent}>
            <p>ID del departamento</p>
            <input className=' bg-slate-200' type='number'></input>
            <button>Eliminar</button>
            {message ? messageStatus == true ?<p className=' text-green-500'>{message}</p>:<p className=' text-red-500'>{message}</p>:<></>}
          </form>
        </div>:
        <></>
      }
    </div>
  )
}

export default Departments