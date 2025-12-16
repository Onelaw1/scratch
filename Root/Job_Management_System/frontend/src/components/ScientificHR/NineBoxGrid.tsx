"use client";

import React, { useState } from "react";
import { Paper, SimpleGrid, Text, Group, Badge, Avatar, Tooltip, ActionIcon, Menu } from "@mantine/core";
import { IconDotsVertical, IconUser } from "@tabler/icons-react";

// Definitions for 9 Boxes
const BOX_DEFINITIONS: Record<number, { title: string; color: string; desc: string }> = {
    9: { title: "Star Superformer", color: "blue", desc: "Top Performance, High Potential" },
    8: { title: "High Potential", color: "cyan", desc: "Mod Performance, High Potential" },
    7: { title: "Enigma", color: "yellow", desc: "Low Performance, High Potential" },
    6: { title: "High Performer", color: "green", desc: "High Performance, Mod Potential" },
    5: { title: "Core Player", color: "gray", desc: "Mod Performance, Mod Potential" },
    4: { title: "Inconsistent", color: "orange", desc: "Low Performance, Mod Potential" },
    3: { title: "Trusted Pro", color: "teal", desc: "High Performance, Low Potential" },
    2: { title: "Effective", color: "gray", desc: "Mod Performance, Low Potential" },
    1: { title: "Risk / Exit", color: "red", desc: "Low Performance, Low Potential" },
};

interface Employee {
    id: string;
    review_id: string;
    name: string;
    dept: string;
    performance: number;
    potential: number;
    box: number;
}

interface NineBoxGridProps {
    employees: Employee[];
    onMove: (reviewId: string, targetBox: number) => void;
}

export function NineBoxGrid({ employees, onMove }: NineBoxGridProps) {

    // Group employees by box
    const grouped = employees.reduce((acc, emp) => {
        acc[emp.box] = acc[emp.box] || [];
        acc[emp.box].push(emp);
        return acc;
    }, {} as Record<number, Employee[]>);

    // Render a single box
    const renderBox = (boxId: number) => {
        const meta = BOX_DEFINITIONS[boxId];
        const emps = grouped[boxId] || [];

        return (
            <Paper
                key={boxId}
                withBorder
                p="sm"
                className={`min-h-[180px] flex flex-col relative transition-colors hover:bg-gray-50`}
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => {
                    e.preventDefault();
                    const reviewId = e.dataTransfer.getData("reviewId");
                    if (reviewId) onMove(reviewId, boxId);
                }}
            >
                <div className="flex justify-between items-start mb-2">
                    <div>
                        <Text fz="xs" fw={700} c="dimmed">Box {boxId}</Text>
                        <Text fw={700} size="sm" c={meta.color}>{meta.title}</Text>
                    </div>
                    <Badge variant="light" color={meta.color} size="sm">{emps.length}</Badge>
                </div>

                <div className="flex-1 space-y-2 overflow-y-auto max-h-[150px] pr-1">
                    {emps.map(emp => (
                        <div
                            key={emp.id}
                            draggable
                            onDragStart={(e) => {
                                e.dataTransfer.setData("reviewId", emp.review_id);
                                e.dataTransfer.effectAllowed = "move";
                            }}
                            className="bg-white p-2 rounded border border-gray-200 shadow-sm cursor-grab active:cursor-grabbing hover:border-blue-400 group"
                        >
                            <Group gap="xs" wrap="nowrap">
                                <Avatar size="sm" radius="xl" color="blue">{emp.name.slice(0, 2)}</Avatar>
                                <div className="flex-1 min-w-0">
                                    <Text size="xs" fw={600} truncate>{emp.name}</Text>
                                    <Text size="xs" c="dimmed" truncate>{emp.dept}</Text>
                                    <Text size="xs" c="dimmed" fz={9}>
                                        Perf:{emp.performance} Pot:{emp.potential}
                                    </Text>
                                </div>
                                <Menu shadow="md" width={150}>
                                    <Menu.Target>
                                        <ActionIcon variant="subtle" size="xs" className="opacity-0 group-hover:opacity-100">
                                            <IconDotsVertical size={12} />
                                        </ActionIcon>
                                    </Menu.Target>
                                    <Menu.Dropdown>
                                        <Menu.Label>Move to...</Menu.Label>
                                        {[9, 8, 7, 6, 5, 4, 3, 2, 1].filter(b => b !== boxId).map(b => (
                                            <Menu.Item key={b} onClick={() => onMove(emp.review_id, b)}>
                                                Box {b} ({BOX_DEFINITIONS[b].title})
                                            </Menu.Item>
                                        ))}
                                    </Menu.Dropdown>
                                </Menu>
                            </Group>
                        </div>
                    ))}
                </div>
            </Paper>
        );
    };

    return (
        <div className="grid grid-cols-3 gap-4">
            {/* Row 1 (Top) -> Box 7, 8, 9 */}
            {renderBox(7)} {renderBox(8)} {renderBox(9)}

            {/* Row 2 (Mid) -> Box 4, 5, 6 */}
            {renderBox(4)} {renderBox(5)} {renderBox(6)}

            {/* Row 3 (Bot) -> Box 1, 2, 3 */}
            {renderBox(1)} {renderBox(2)} {renderBox(3)}
        </div>
    );
}
