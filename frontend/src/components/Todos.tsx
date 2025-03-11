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
    Text,
    DialogActionTrigger,
} from "@chakra-ui/react";

// Todo interface
interface Todo {
    id: string;
    item: string;
}

// Context for managing global state across components
const TodosContext = createContext({
    todos: [], fetchTodos: () => {}
});

// Todos Component
export default function Todos() {
    const [todos, setTodos] = useState([]);
    const fetchTodos = () => {
        fetch("http://localhost:8000/todo")
            .then(response => response.json())
            .then(data => setTodos(data.data))
            .catch(error => console.error("Error:", error));
    };

    useEffect(() => {
        fetchTodos();
    }, []);

    return (
        <TodosContext.Provider value={{todos, fetchTodos}}>
            <Container maxW="container.xl" pt="100px">
                <Stack gap={5}>
                    {todos.map((todo: Todo) => (
                        <b key={todo.id}>{todo.item}</b>
                    ))}
                </Stack>
            </Container>
        </TodosContext.Provider>
    );
}
