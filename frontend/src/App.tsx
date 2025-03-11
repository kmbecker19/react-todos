import { ChakraProvider, defaultSystem } from '@chakra-ui/react'
import Header from './components/Header'
import './App.css'

function App() {

  return (
   <ChakraProvider value={defaultSystem}>
    <Header />
   </ChakraProvider>
  )
}

export default App
