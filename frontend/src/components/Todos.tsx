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

// Shell for adding todo
function AddTodo() {
    const [item, setItem] = useState("");
    const {todos, fetchTodos} = useContext(TodosContext);

    // Form handling functions
    const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
        setItem(event.target.value);
    };
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const newTodo = {
            "id": todos.length + 1,
            "item": item
        };
        fetch("http://localhost:8000/todo", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newTodo)
        }).then(fetchTodos);
    };
    return (
        <form onSubmit={handleSubmit}>
            <Input
                pr="4.5rem"
                type="text"
                placeholder="Add a todo item"
                aria-label="Add a todo item"
                onChange={handleInput}
            />
        </form>
    );
}

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
                <AddTodo />
                <Stack gap={5}>
                    {todos.map((todo: Todo) => (
                        <b key={todo.id}>{todo.item}</b>
                    ))}
                </Stack>
            </Container>
        </TodosContext.Provider>
    );
}
