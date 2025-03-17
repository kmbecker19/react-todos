import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router'
import HomePage from './components/HomePage.tsx'
import CreateUserPage from './components/CreateUserPage.tsx'
import App from './App.tsx'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="todo-list" element={<App />} />
        <Route path="create-user" element={<CreateUserPage />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
