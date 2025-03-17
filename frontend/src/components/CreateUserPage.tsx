import { useForm, SubmitHandler } from 'react-hook-form';
import {
  Button,
  Container,
  Input,
  Heading,
  Flex,
  Field,
  Stack,
  ChakraProvider,
  defaultSystem,
} from '@chakra-ui/react';

import Header from './Header';

interface FormValues {
  username: string;
  password: string;
}

function CreateUserForm() {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<FormValues>();

  const registerUser: SubmitHandler<FormValues> = (data) => {
    fetch('http://localhost:8000/auth/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
      .then(response => response.json())
      .then(user => console.log('User created:', user))
      .catch(error => console.error('Error creating user:', error));
  };

  return (
    <form onSubmit={handleSubmit(registerUser)}>
      <Stack gap={5} align='flex-start' maxW='sm'>
        <Field.Root invalid={!!errors.username}>
          <Field.Label>Username</Field.Label>
          <Input {...register('username')} />
          <Field.ErrorText>{errors.username?.message}</Field.ErrorText>
        </Field.Root>

        <Field.Root invalid={!!errors.password}>
          <Field.Label>Password</Field.Label>
          <Input {...register('password')} />
          <Field.ErrorText>{errors.password?.message}</Field.ErrorText>
        </Field.Root>

        <Button type='submit'>Create User</Button>
      </Stack>
    </form>
  );
}

export default function CreateUserPage() {
  return (
    <ChakraProvider value={defaultSystem}>
      <Header />
      <Container maxW='container.xl' pt='100px'>
        <Flex as='nav' justify='center' margin='20'>
          <Heading as='h1' size='md'>Create a New User</Heading>
        </Flex>
        <CreateUserForm />
      </Container>
    </ChakraProvider>
  );
}