import { Button, Container, Text, Flex, defaultSystem, ChakraProvider } from '@chakra-ui/react'
import Header from './Header'

function TodoButton() {
    return (
        <Button asChild size="xl">
            <a href="/todo-list">Go to To-Do List</a>
        </Button>
    )
}
export default function HomePage() {
  return (
    <ChakraProvider value={defaultSystem}>
        <Header />
        <Container maxW="container.xl" pt="100px">
            <TodoButton />
        </Container>
    </ChakraProvider>
  )
}
