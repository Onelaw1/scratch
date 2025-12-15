"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import {
    Container, Title, Text, Group, Paper, Badge,
    ScrollArea, Loader, Stack, ThemeIcon, Avatar
} from "@mantine/core";
import { notifications } from "@mantine/notifications";
import {
    DragDropContext, Droppable, Draggable, DropResult
} from "@hello-pangea/dnd";
import { IconGripVertical, IconUser, IconClock } from "@tabler/icons-react";
import { api } from "@/lib/api";

interface JobTask {
    id: string;
    task_name: string;
    workload_entries?: any[];
}

interface JobPosition {
    id: string;
    title: string;
    grade?: string;
    tasks: JobTask[];
}

export default function SimulationBoard() {
    const { id } = useParams() as { id: string };
    const [positions, setPositions] = useState<JobPosition[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (id) loadData();
    }, [id]);

    const loadData = async () => {
        try {
            const data = await api.getScenarioPositions(id);
            setPositions(data);
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to load board data', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    const onDragEnd = async (result: DropResult) => {
        const { source, destination, draggableId } = result;
        if (!destination) return;
        if (source.droppableId === destination.droppableId && source.index === destination.index) return;

        // Optimistic Update
        const sourcePosIndex = positions.findIndex(p => p.id === source.droppableId);
        const destPosIndex = positions.findIndex(p => p.id === destination.droppableId);

        const newPositions = [...positions];
        const sourcePos = { ...newPositions[sourcePosIndex] };
        const destPos = { ...newPositions[destPosIndex] };

        const [movedTask] = sourcePos.tasks.splice(source.index, 1);
        destPos.tasks.splice(destination.index, 0, movedTask);

        newPositions[sourcePosIndex] = sourcePos;
        newPositions[destPosIndex] = destPos;

        setPositions(newPositions);

        try {
            await api.moveTask(draggableId, destination.droppableId);
            notifications.show({ title: 'Moved', message: 'Task reassigned successfully', color: 'blue', autoClose: 1000, withCloseButton: false });
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to sync move', color: 'red' });
            loadData();
        }
    };

    if (loading) return <Container py="xl"><Loader /></Container>;

    return (
        <div style={{ height: 'calc(100vh - 60px)', display: 'flex', flexDirection: 'column', background: '#F5F5F7' }}>
            {/* Header - Apple Style Glassmorphism */}
            <div className="z-10 relative px-6 py-4 flex items-center justify-between backdrop-blur-md bg-white/70 border-b border-white/20 shadow-sm transition-all sticky top-0">
                <div>
                    <Group gap="xs">
                        <ThemeIcon variant="light" size="lg" radius="md" color="indigo"><IconClock /></ThemeIcon>
                        <Title order={3} style={{ fontFamily: '-apple-system, BlinkMacSystemFont, sans-serif', fontWeight: 600 }}>Simulation Board</Title>
                    </Group>
                    <Text size="sm" c="dimmed" mt={4} fw={500}>
                        Drag tasks to redesign job roles. Use <Badge variant="outline" size="xs">Space</Badge> to pick up, <Badge variant="outline" size="xs">Arrows</Badge> to move.
                    </Text>
                </div>
            </div>

            <DragDropContext onDragEnd={onDragEnd}>
                <ScrollArea style={{ flex: 1 }} type="auto" offsetScrollbars>
                    <div className="flex gap-6 p-6 h-full min-w-max items-start">
                        {positions.map((pos) => (
                            <Paper
                                key={pos.id}
                                w={340}
                                radius="lg"
                                className="flex flex-col flex-shrink-0 transition-shadow duration-200"
                                style={{
                                    backgroundColor: 'rgba(255, 255, 255, 0.6)',
                                    backdropFilter: 'blur(12px)',
                                    boxShadow: '0 4px 24px rgba(0,0,0,0.04)',
                                    border: '1px solid rgba(255,255,255,0.4)',
                                    maxHeight: '100%'
                                }}
                            >
                                {/* Column Header */}
                                <div className="p-4 border-b border-gray-100/50">
                                    <Group justify="space-between" mb={6} align="center">
                                        <Text fw={700} size="md" c="dark.8" style={{ letterSpacing: '-0.02em' }}>{pos.title}</Text>
                                        <Badge variant="light" color={pos.tasks.length === 0 ? 'red' : 'gray'} size="sm" radius="sm">
                                            {pos.tasks.length}
                                        </Badge>
                                    </Group>
                                    <Group gap="xs">
                                        <Badge size="xs" variant="dot" color="blue">{pos.grade || 'No Grade'}</Badge>
                                    </Group>
                                </div>

                                {/* Droppable Area */}
                                <Droppable droppableId={pos.id}>
                                    {(provided, snapshot) => (
                                        <div
                                            ref={provided.innerRef}
                                            {...provided.droppableProps}
                                            style={{
                                                flex: 1,
                                                padding: '12px',
                                                overflowY: 'auto',
                                                transition: 'background-color 0.2s ease',
                                                backgroundColor: snapshot.isDraggingOver ? 'var(--mantine-color-indigo-0)' : 'transparent',
                                                borderRadius: '0 0 16px 16px'
                                            }}
                                            className="scrollbar-thin"
                                        >
                                            <Stack gap="sm">
                                                {pos.tasks.map((task, index) => (
                                                    <Draggable key={task.id} draggableId={task.id} index={index}>
                                                        {(provided, snapshot) => (
                                                            <div
                                                                ref={provided.innerRef}
                                                                {...provided.draggableProps}
                                                                {...provided.dragHandleProps}
                                                                style={{
                                                                    ...provided.draggableProps.style,
                                                                    transform: snapshot.isDragging ? provided.draggableProps.style?.transform : 'none',
                                                                }}
                                                            >
                                                                <Paper
                                                                    p="md"
                                                                    radius="md"
                                                                    className="transition-all duration-200"
                                                                    style={{
                                                                        backgroundColor: snapshot.isDragging ? 'rgba(255,255,255,0.95)' : '#FFFFFF',
                                                                        boxShadow: snapshot.isDragging
                                                                            ? '0 12px 32px rgba(0,0,0,0.12)'
                                                                            : '0 1px 3px rgba(0,0,0,0.04)',
                                                                        border: snapshot.isDragging ? 'none' : '1px solid rgba(0,0,0,0.02)',
                                                                        transform: snapshot.isDragging ? 'scale(1.02)' : 'scale(1)',
                                                                        zIndex: snapshot.isDragging ? 999 : 1
                                                                    }}
                                                                >
                                                                    <Group align="start" wrap="nowrap" gap="sm">
                                                                        <div className={`mt-1 transition-opacity ${snapshot.isDragging ? 'opacity-100' : 'opacity-40 hover:opacity-100'}`}>
                                                                            <IconGripVertical size={14} />
                                                                        </div>
                                                                        <div style={{ flex: 1 }}>
                                                                            <Text size="sm" fw={600} c="dark.9" lh={1.4} mb={4}>
                                                                                {task.task_name}
                                                                            </Text>
                                                                            {snapshot.isDragging && (
                                                                                <Badge size="xs" variant="gradient" gradient={{ from: 'indigo', to: 'cyan' }}>
                                                                                    Moving...
                                                                                </Badge>
                                                                            )}
                                                                        </div>
                                                                    </Group>
                                                                </Paper>
                                                            </div>
                                                        )}
                                                    </Draggable>
                                                ))}
                                                {provided.placeholder}
                                            </Stack>
                                        </div>
                                    )}
                                </Droppable>
                            </Paper>
                        ))}
                    </div>
                </ScrollArea>
            </DragDropContext>
        </div>
    );
}
