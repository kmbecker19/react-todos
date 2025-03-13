import React, { useEffect, useState, createContext, useContext } from "react";
import {
  Box,
  Button,
  Container,
  Flex,
  Input,
  DialogBody,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
  Stack,
  HStack,
  Text,
  DialogActionTrigger,
  SelectRoot,
  SelectTrigger,
  SelectValueText,
  SelectContent,
  SelectItem,
  createListCollection,
  SelectValueChangeDetails,
} from "@chakra-ui/react";

// Todo interface
interface Todo {
  id: string;
  item: string;
  priority: number;
}

interface UpdateTodoProps {
  item: string;
  id: string;
  priority: number;
  fetchTodos: () => void;
}

interface TodoHelperProps {
  item: string;
  id: string;
  priority: number;
  fetchTodos: () => void;
}

interface DeleteTodoProps {
  id: string;
  fetchTodos: () => void;
}

// Context for managing global state across components
const TodosContext = createContext({
  todos: [], fetchTodos: () => { }
});

// Delete Todo Component
function DeleteTodo({ id, fetchTodos }: DeleteTodoProps) {
  const deleteTodo = async () => {
    await fetch(`http://localhost:8000/sql/todo/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ id: id })
    });
    await fetchTodos();
  };
  return (
    <Button h="1.5rem" size="sm" marginLeft={2} onClick={deleteTodo}>Delete Todo</Button>
  )
}

const priorities = createListCollection({
  items: [
    { label: "High", value: 3 },
    { label: "Medium", value: 2 },
    { label: "Low", value: 1 },
  ],
});

interface SelectPriorityProps {
  setPriority: (p: number) => void;
}

// TODO: fix logic for changing prirority number
function SelectPriority({ setPriority }: SelectPriorityProps) {
  const handleChange = (details: SelectValueChangeDetails) => {
    setPriority(parseInt(details.value[0]));
  };

  return (
    <SelectRoot collection={priorities} size="sm" maxW="200px" onValueChange={handleChange}>
      <SelectTrigger>
        <SelectValueText placeholder="Priority" />
      </SelectTrigger>
      <SelectContent>
        {priorities.items.map((p) => (
          <SelectItem item={p} key={p.value}>
            <Text color="black">{p.label}</Text>
          </SelectItem>
        ))}
      </SelectContent>
    </SelectRoot>
  );
}

function UpdateTodo({ item, id, fetchTodos }: UpdateTodoProps) {
  const [todo, setTodo] = useState(item);
  const updateTodo = async () => {
    await fetch(`http://localhost:8000/sql/todo/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ item: todo })
    });
    await fetchTodos();
  };
  return (
    <DialogRoot>
      <DialogTrigger asChild>
        <Button h="1.5rem" size="sm">
          Update Todo
        </Button>
      </DialogTrigger>
      <DialogContent
        position="fixed"
        top="50%"
        left="50%"
        transform="translate(-50%, -50%)"
        bg="white"
        p={6}
        rounded="md"
        shadow="xl"
        maxW="md"
        w="90%"
        zIndex={1000}
      >
        <DialogHeader>
          <DialogTitle>Update Todo</DialogTitle>
        </DialogHeader>
        <DialogBody>
          <Input
            pr="4.5rem"
            type="text"
            placeholder="Add a todo item"
            aria-label="Add a todo item"
            value={todo}
            onChange={event => setTodo(event.target.value)}
          />
        </DialogBody>
        <DialogFooter>
          <DialogActionTrigger asChild>
            <Button variant="outline" size="sm">Cancel</Button>
          </DialogActionTrigger>
          <Button size="sm" onClick={updateTodo}>Save</Button>
        </DialogFooter>
      </DialogContent>
    </DialogRoot>
  );
}

// Shell for adding todo
function AddTodo() {
  const [item, setItem] = useState("");
  const { todos, fetchTodos } = useContext(TodosContext);
  const [priority, setPriority] = useState(0);

  // Form handling functions
  const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    setItem(event.target.value);
  };
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const newTodo = {
      "item": item,
      "priority": priority ? priority : undefined,
    };
    fetch("http://localhost:8000/sql/todo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(newTodo)
    }).then(fetchTodos);
    setItem("")
  };
  return (
    <form onSubmit={handleSubmit}>
      <HStack align="top">
        <Input
          pr="4.5rem"
          type="text"
          placeholder="Add a todo item"
          aria-label="Add a todo item"
          value={item}
          onChange={handleInput}
        />
        <SelectPriority setPriority={setPriority} />
        <Button type="submit" >Add Item</Button>
      </HStack>
    </form>
  );
}

function TodoHelper({ item, id, priority, fetchTodos }: TodoHelperProps) {
  return (
    <Box p={1} shadow="sm">
      <Flex justify="space-between">
        <Text mt={4} as="div">
          {item}
          <Flex align="end">
            <UpdateTodo item={item} id={id} priority={priority} fetchTodos={fetchTodos} />
            <DeleteTodo id={id} fetchTodos={fetchTodos} />
          </Flex>
        </Text>
      </Flex>
    </Box>
  );
}

// Todos Component
export default function Todos() {
  const [todos, setTodos] = useState([]);
  const fetchTodos = () => {
    fetch("http://localhost:8000/sql/todo")
      .then(response => response.json())
      .then(data => setTodos(data))
      .catch(error => console.error("Error:", error));
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <TodosContext.Provider value={{ todos, fetchTodos }}>
      <Container maxW="container.xl" pt="100px">
        <AddTodo />
        <Stack gap={5}>
          {todos.map((todo: Todo) => (
            <TodoHelper id={todo.id} item={todo.item} priority={todo.priority} fetchTodos={fetchTodos} />
          ))}
        </Stack>
      </Container>
    </TodosContext.Provider>
  );
}
