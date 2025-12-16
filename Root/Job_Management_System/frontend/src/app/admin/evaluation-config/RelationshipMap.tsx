'use client';

import React, { useEffect, useState } from 'react';
import { Card, Text, Group, Badge, ScrollArea, LoadingOverlay, Box } from '@mantine/core';
import { api, EvaluationAssignment } from '@/lib/api';

interface RelationshipMapProps {
    sessionId: string;
}

export function RelationshipMap({ sessionId }: RelationshipMapProps) {
    const [assignments, setAssignments] = useState<EvaluationAssignment[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (sessionId) {
            loadData();
        }
    }, [sessionId]);

    const loadData = async () => {
        setLoading(true);
        try {
            const data = await api.getAssignments(sessionId);
            setAssignments(data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    // Visualization Logic
    // Left: Raters, Right: Targets
    const raters = Array.from(new Set(assignments.map(a => a.rater_user_id)));
    const targets = Array.from(new Set(assignments.map(a => a.target_job_position_id)));

    const canvasHeight = Math.max(raters.length, targets.length) * 60 + 100;
    const canvasWidth = 800;

    const raterY = (index: number) => 50 + index * 60;
    const targetY = (index: number) => 50 + index * 60;

    const getRaterY = (id: string) => raterY(raters.indexOf(id));
    const getTargetY = (id: string) => targetY(targets.indexOf(id));

    const getColor = (role: string) => {
        switch (role) {
            case 'PEER': return '#228be6'; // Blue
            case 'SUPERVISOR_1': return '#fa5252'; // Red
            case 'SUPERVISOR_2': return '#be4bdb'; // Grape
            case 'SELF': return '#40c057'; // Green
            default: return '#868e96'; // Gray
        }
    };

    return (
        <Card withBorder shadow="sm" mt="md" pos="relative" style={{ minHeight: 400 }}>
            <LoadingOverlay visible={loading} />
            <Text fw={700} mb="md">Evaluation Structure Map</Text>

            <Group mb="md">
                <Badge color="blue">Peer</Badge>
                <Badge color="red">Supervisor 1</Badge>
                <Badge color="grape">Supervisor 2</Badge>
                <Badge color="green">Self</Badge>
            </Group>

            <ScrollArea h={500}>
                <svg width={canvasWidth} height={canvasHeight}>
                    {/* Links */}
                    {assignments.map(a => {
                        const startY = getRaterY(a.rater_user_id);
                        const endY = getTargetY(a.target_job_position_id);
                        const roleColor = getColor(a.rater_role);

                        return (
                            <path
                                key={a.id}
                                d={`M 200 ${startY} C 400 ${startY}, 400 ${endY}, 600 ${endY}`}
                                fill="none"
                                stroke={roleColor}
                                strokeWidth="2"
                                opacity="0.6"
                            />
                        );
                    })}

                    {/* Nodes - Raters */}
                    {raters.map((r, i) => (
                        <g key={r} transform={`translate(50, ${raterY(i) - 15})`}>
                            <rect width="150" height="30" rx="5" fill="#e7f5ff" stroke="#228be6" />
                            <text x="75" y="20" textAnchor="middle" fontSize="12" fill="#1c7ed6">
                                Rater: {r.substring(0, 8)}...
                            </text>
                        </g>
                    ))}

                    {/* Nodes - Targets */}
                    {targets.map((t, i) => (
                        <g key={t} transform={`translate(600, ${targetY(i) - 15})`}>
                            <rect width="150" height="30" rx="5" fill="#f3f0ff" stroke="#7950f2" />
                            <text x="75" y="20" textAnchor="middle" fontSize="12" fill="#5f3dc4">
                                Job: {t.substring(0, 8)}...
                            </text>
                        </g>
                    ))}

                    {/* Labels */}
                    <text x="125" y="20" textAnchor="middle" fontWeight="bold">Evaluators</text>
                    <text x="675" y="20" textAnchor="middle" fontWeight="bold">Target Jobs</text>
                </svg>
            </ScrollArea>

            {assignments.length === 0 && !loading && (
                <Box ta="center" py="xl">
                    <Text c="dimmed">No assignments found for this session.</Text>
                </Box>
            )}
        </Card>
    );
}
