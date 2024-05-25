import React from 'react'
import { useState } from 'react'
import axios from 'axios'

function Departments() {
  const [statePage, setStatePage] = useState(5)
  const [departmentsList, setDepartmentsList] = useState([]);
  const [message, setMessage] = useState('')
  const [messageStatus, setMessageStatus] = useState(true)

  const createState = (e) => {
    e.preventDefault();
    setStatePage(0)
    setMessage('')
  }
  const readState = (e) => {
    e.preventDefault();
    setStatePage(1)
    setMessage('')
    readEvent()
  }
  const updateState = (e) => {
    e.preventDefault();
    setStatePage(2)
    setMessage('')
  }
  const deleteState = (e) => {
    e.preventDefault();
    setStatePage(3)
    setMessage('')
  }
  const createEvent = async (e) => {
    e.preventDefault();
    const list = []
    Array.from(e.target.elements).forEach((element)=>{list.push(element.value)})
    try {
      const res = await axios.post('http://127.0.0.1:8000/departments',{
        'DEPTNO':list[0],
        'DNAME':list[1],
        'LOC':list[2]
      });
      console.log(res)
      if(res.status == 200){
        setMessage('Se agrego un nuevo empleado')
        setMessageStatus(true)
      }
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
      if(res.status == 200){
        setMessageStatus(true)
        setDepartmentsList(res.data)
      }
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
    const params = {
      'DNAME':list[1],
        'LOC':list[2]
  };

  const filteredParams = Object.fromEntries(
      Object.entries(params).filter(([_, value]) => value != null && value !== '')
  );

    try {
      const res = await axios.put(`http://127.0.0.1:8000/departments/${list[0]}`,filteredParams);
      console.log(res)
      if(res.status == 200){
        setMessage('Se completo la modificación')
        setMessageStatus(true)
      }
    } catch (e) {
      if(e.request.status == 422){
        setMessage('Se ingresaron los datos incorrectos')
        setMessageStatus(false)
      }
      if(e.request.status == 404){
        setMessage('Departamento inexistente')
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
      if(res.status == 200){
        setMessage('Se elimino exitosamente el departamento')
        setMessageStatus(true)
      }
      
    } catch (e) {
      if(e.request.status == 422){
        setMessage('Se ingresaron los datos incorrectos')
        setMessageStatus(false)
      }
      if(e.request.status == 404){
        setMessage('Departamento inexistente')
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
        <button className=' p-1 hover:bg-slate-800 bg-slate-900 mx-2 rounded-sm px-2 font-medium' onClick={createState}>Crear DEPT</button>
        <button className=' p-1 hover:bg-slate-800 bg-slate-900 mx-2 rounded-sm px-2 font-medium' onClick={deleteState}>Eliminar DEPT</button>
        <button className=' p-1 hover:bg-slate-800 bg-slate-900 mx-2 rounded-sm px-2 font-medium' onClick={updateState}>Modificar DEPT</button>
        <button className=' p-1 hover:bg-slate-800 bg-slate-900 mx-2 rounded-sm px-2 font-medium' onClick={readState}>Consultar DEPT</button>
      </header>
      {
        statePage == 0 ?
          <div>
            <form onSubmit={createEvent} className=' p-3'>
              <p>ID del departamento</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <p>Nombre del departamento</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='text'></input>
              <p>Localización del departamento</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='text'></input>
              <button className=' bg-orange-500 m-5 p-1 px-2 rounded-md font-semibold'>Subir</button>
              {message ? messageStatus == true ?<p className=' text-green-500'>{message}</p>:<p className=' text-red-500'>{message}</p>:<></>}
            </form>
          </div>:
        statePage == 1 ? 
          <div className='p-5'>
            <table>
              <thead>
                <tr>
                  <th className=' border p-2 text-center'>ID</th>
                  <th className=' border p-2 text-center'>Nombre del departamento</th>
                  <th className=' border p-2 text-center'>Localización</th>
                </tr>
              </thead>
              <tbody>
                {departmentsList.map(department => (
                <tr key={department.DEPTNO}>
                  <td className=' border p-2 text-center'>{department.DEPTNO}</td>
                  <td className=' border p-2 text-center'>{department.DNAME}</td>
                  <td className=' border p-2 text-center'>{department.LOC}</td>
                </tr>
                ))}
              </tbody>
            </table>
            {message ? messageStatus == true ?<p className=' text-green-500'>{message}</p>:<p className=' text-red-500'>{message}</p>:<></>}
          </div>:
        statePage == 2 ? 
        <div>
          <form onSubmit={updateEvent} className=' p-3'>
          <p>ID del departamento</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <p>Nombre del departamento</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='text'></input>
              <p>Localización del departamento</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='text'></input>
              <button className=' bg-orange-500 m-5 p-1 px-2 rounded-md font-semibold'>Modificar</button>
              {message ? messageStatus == true ?<p className=' text-green-500'>{message}</p>:<p className=' text-red-500'>{message}</p>:<></>}
            </form>
        </div>:
        statePage == 3 ? 
        <div className=' p-3'>
          <form onSubmit={deleteEvent}>
            <p>ID del departamento</p>
            <input className=' bg-slate-200 text-black rounded-sm' type='number'></input>
            <button className=' bg-orange-500 m-5 p-1 px-2 rounded-md font-semibold'>Eliminar</button>
            {message ? messageStatus == true ?<p className=' text-green-500'>{message}</p>:<p className=' text-red-500'>{message}</p>:<></>}
          </form>
        </div>:
        <></>
      }
    </div>
  )
}

export default Departments