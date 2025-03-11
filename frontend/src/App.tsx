import { ChakraProvider, defaultSystem } from '@chakra-ui/react'
import Header from './components/Header'
import Todos from './components/Todos'
import './App.css'

function App() {

  return (
   <ChakraProvider value={defaultSystem}>
    <Header />
    <Todos />
   </ChakraProvider>
  )
}

export default App
