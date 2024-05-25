import React from 'react'
import { useState } from 'react'
import axios from 'axios'

function Employees() {
  const [statePage, setStatePage] = useState(5)
  const [employeesList, setEmployeesList] = useState([]);
  const [message, setMessage] = useState('');
  const [messageStatus, setMessageStatus] = useState(true);

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
    const params = {
      'EMPNO': list[0],
      'ENAME': list[1],
      'JOB': list[2],
      'MGR': list[3],
      'HIREDATE': list[4],
      'SAL': list[5],
      'COMM': list[6],
      'DEPTNO': list[7]
  };

  const filteredParams = Object.fromEntries(
      Object.entries(params).filter(([_, value]) => value != null && value !== '')
  );
    Array.from(e.target.elements).forEach((element)=>{list.push(element.value)})
    try {
      const res = await axios.post('http://127.0.0.1:8000/employees',filteredParams);
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
      const res = await axios.get(`http://127.0.0.1:8000/employees`);
      if(res.status == 200){
        setMessageStatus(true)
        setEmployeesList(res.data)
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
      'ENAME': list[1],
      'JOB': list[2],
      'MGR': list[3],
      'HIREDATE': list[4],
      'SAL': list[5],
      'COMM': list[6],
      'DEPTNO': list[7]
  };

  const filteredParams = Object.fromEntries(
      Object.entries(params).filter(([_, value]) => value != null && value !== '')
  );

  try {
      const res = await axios.put(`http://127.0.0.1:8000/employees/${list[0]}`, filteredParams);
      if(res.status == 200){
        setMessage('Se completo la modificación')
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
      if(e.request.status == 404){
        setMessage('Empleado inexistente')
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
      const res = await axios.delete(`http://127.0.0.1:8000/employees/${list[0]}`);
      if(res.status == 200){
        setMessage('Se elimino exitosamente al empleado')
        setMessageStatus(true)
      }
      
    } catch (e) {
      if(e.request.status == 422){
        setMessage('Se ingresaron los datos incorrectos')
        setMessageStatus(false)
      }
      if(e.request.status == 404){
        setMessage('Empleado inexistente')
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
        <button className=' p-1 hover:bg-slate-800 bg-slate-900 mx-2 rounded-sm px-2 font-medium' onClick={createState}>Crear EMP</button>
        <button className=' p-1 hover:bg-slate-800 bg-slate-900 mx-2 rounded-sm px-2 font-medium' onClick={deleteState}>Eliminar EMP</button>
        <button className=' p-1 hover:bg-slate-800 bg-slate-900 mx-2 rounded-sm px-2 font-medium' onClick={updateState}>Modificar EMP</button>
        <button className=' p-1 hover:bg-slate-800 bg-slate-900 mx-2 rounded-sm px-2 font-medium' onClick={readState}>Consultar EMP</button>
      </header>
      {
        statePage == 0 ?
          <div>
            <form onSubmit={createEvent} className=' p-3'>
              <p>ID del empleado</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <p>Nombre del empleado</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='text'></input>
              <p>Puesto</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='text'></input>
              <p>ID del manager</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <p>Fechas de contratación</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='date'></input>
              <p>Salario</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <p>Comisión</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <p>ID del departamento</p>
              <input className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <button className=' bg-orange-500 m-5 p-1 px-2 rounded-md font-semibold'>Subir</button>
              {message ? messageStatus == true ?<p className=' text-green-500'>{message}</p>:<p className=' text-red-500'>{message}</p>:<></>}
            </form>
          </div>:
        statePage == 1 ? 
          <div className='p-5'>
            <table >
              <thead>
                <tr >
                  <th className=' border p-2 text-center'>ID</th>
                  <th className=' border p-2 text-center'>Nombre</th>
                  <th className=' border p-2 text-center'>Puesto</th>
                  <th className=' border p-2 text-center'>Manager</th>
                  <th className=' border p-2 text-center'>Fecha de contratación</th>
                  <th className=' border p-2 text-center'>Salario</th>
                  <th className=' border p-2 text-center'>Comisión</th>
                  <th className=' border p-2 text-center'>ID del departamento</th>
                </tr>
              </thead>
              <tbody>
                {employeesList.map(employee => (
                <tr key={employee.EMPNO}>
                  <td className=' border p-2 text-center'>{employee.EMPNO}</td>
                  <td className=' border p-2 text-center'>{employee.ENAME}</td>
                  <td className=' border p-2 text-center'>{employee.JOB}</td>
                  <td className=' border p-2 text-center'>{employee.MGR}</td>
                  <td className=' border p-2 text-center'>{employee.HIREDATE}</td>
                  <td className=' border p-2 text-center'>{employee.SAL}</td>
                  <td className=' border p-2 text-center'>{employee.COMM}</td>
                  <td className=' border p-2 text-center'>{employee.DEPTNO}</td>
                </tr>))}
              </tbody>
            </table>
            {message ? messageStatus == true ?<p className=' text-green-500'>{message}</p>:<p className=' text-red-500'>{message}</p>:<></>}
          </div>:
        statePage == 2 ? 
        <div>
          <form onSubmit={updateEvent} className=' p-3'>
              <p>ID del empleado</p>
              <input value={null} className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <p>Nombre del empleado</p>
              <input value={null} className=' bg-slate-200 text-black rounded-sm' type='text'></input>
              <p>Puesto</p>
              <input value={null} className=' bg-slate-200 text-black rounded-sm' type='text'></input>
              <p>ID del manager</p>
              <input value={null} className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <p>Fechas de contratación</p>
              <input value={null} className=' bg-slate-200 text-black rounded-sm' type='date'></input>
              <p>Salario</p>
              <input value={null} className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <p>Comisión</p>
              <input value={null} className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <p>ID del departamento</p>
              <input value={null} className=' bg-slate-200 text-black rounded-sm' type='number'></input>
              <button className=' bg-orange-500 m-5 p-1 px-2 rounded-md font-semibold'>Modificar</button>
              {message ? messageStatus == true ?<p className=' text-green-500'>{message}</p>:<p className=' text-red-500'>{message}</p>:<></>}
            </form>
        </div>:
        statePage == 3 ? 
        <div className='p-3'>
          <form onSubmit={deleteEvent}>
            <p>ID del empleado</p>
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

export default Employees