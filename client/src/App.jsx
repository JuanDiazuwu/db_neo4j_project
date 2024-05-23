import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Employees from './pages/Employees'
import Departments from './pages/Departments'

function App() {
  return (
    <>
      <header className=' text-xl font-bold p-1'>
        <a href='/employees' className=' pr-3 hover:bg-slate-200'>Empleados</a>
        <a href='/departments' className='hover:bg-slate-200'>Departamentos</a>
      </header>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<></>}/>
          <Route path='/employees' element={<Employees/>}/>
          <Route path='/departments' element={<Departments/>}/>
        </Routes>
      </BrowserRouter>
    </> 
  )
}

export default App
