import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Employees from './pages/Employees'
import Departments from './pages/Departments'

function App() {
  return (
    <>
      <header className=' text-xl font-bold p-1 bg-black'>
        <div className='flex flex-row font-black text-3xl text-white'>
          <a href='/' className=' text-orange-500'>Corp</a><a href='/' className=' text-white'>Tex</a>
        </div>
        <div className=' text-white px-3 py-2 bg-gray-950'>
          <a href='/employees' className=' bg-slate-700 pr-3 hover:bg-slate-800 px-2 rounded-sm mr-4'>Empleados</a>
          <a href='/departments' className='bg-slate-700 hover:bg-slate-800 px-2 rounded-sm'>Departamentos</a>
        </div>
      </header>
      <body className=' bg-slate-600'>
        <BrowserRouter>
          <Routes>
            <Route path='/' element={<></>}/>
            <Route path='/employees' element={<Employees/>}/>
            <Route path='/departments' element={<Departments/>}/>
          </Routes>
        </BrowserRouter>
      </body>
    </> 
  )
}

export default App
