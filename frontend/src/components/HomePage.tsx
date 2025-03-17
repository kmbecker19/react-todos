import { Button, Container, Text, Flex, defaultSystem, ChakraProvider, Heading } from '@chakra-ui/react'
import Header from './Header'

function TodoButton() {
  return (
    <Button asChild size="xl">
      <a href="/todo-list">Go to To-Do List</a>
    </Button>
  )
}

function CreateUserButton() {
  return (
    <Button asChild size="xl">
      <a href="/create-user">Create a New User</a>
    </Button>
  )
}

export default function HomePage() {
  return (
    <ChakraProvider value={defaultSystem}>
      <Header />
      <Container maxW="container.xl" pt="100px">
        <Flex as="nav" justify="center" margin="20">
          <Heading as="h1" size="md">Welcome to the Home Page!</Heading>
        </Flex>
        <Flex justify="center" align="center" margin="20" gap={5}>
          <TodoButton />
          <CreateUserButton />
        </Flex>
      </Container>
    </ChakraProvider>
  )
}
