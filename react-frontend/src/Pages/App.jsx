import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className='flex justify-around mb-16'>
        <a href="https://vitejs.dev" target="_blank">
          <img src="./static/assets/images/vite.svg" className="logo p-0" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src="./static/assets/images/react.svg" className="logo react p-0" alt="React logo" />
        </a>
      </div>
      <h1 className='text-4xl font-bold'>Vite + React</h1>
      <div className="card">
        <button className='my-8 rounded-lg pt-2 pr-5 pb-2 pl-5 text-base font-medium bg-gray-900 cursor-pointer hover:border-indigo-500'
          onClick={() => setCount((count) => count + 1)}>
          Button has been pressed {count} times
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
