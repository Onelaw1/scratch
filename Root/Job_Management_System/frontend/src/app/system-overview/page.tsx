"use client";

import { Container, Button, Group, Alert, Text, Divider, Title } from "@mantine/core";
import { IconDownload, IconPrinter, IconInfoCircle } from "@tabler/icons-react";
import { EnterpriseArchitectureMap } from "@/components/EnterpriseArchitectureMap";
import { UserRoleSpace3D } from "@/components/UserRoleSpace3D";
import { DataSchemaSpec } from "@/components/DataSchemaSpec";
import { SecurityArchitectureDiagram } from "@/components/SecurityArchitectureDiagram";
import { BlueprintArchitecture } from "@/components/BlueprintArchitecture";

export default function SystemOverviewPage() {
    return (
        <Container size="xl" py="xl" style={{ maxWidth: '1600px' }}> {/* Maximum width for dense report */}

            {/* Toolbar */}
            <Group justify="space-between" mb="xs" className="print:hidden">
                <Alert icon={<IconInfoCircle size={16} />} title="Architecture Mode" color="blue" variant="light" p="xs">
                    <Text size="xs">This view is optimized for ISP Strategic Planning Reports. Scroll down for full appendices.</Text>
                </Alert>
                <Group>
                    <Button variant="default" size="xs" leftSection={<IconPrinter size={14} />} onClick={() => window.print()}>Print / PDF</Button>
                    <Button variant="filled" color="dark" size="xs" leftSection={<IconDownload size={14} />}>Export Report</Button>
                </Group>
            </Group>

            {/* 1. Main Architecture (The Strategic View) */}
            <EnterpriseArchitectureMap />

            <Divider my="xl" variant="dashed" label="Technical Appendices" labelPosition="center" />

            {/* 2. User Permissions Matrix (3D Space) */}
            <UserRoleSpace3D />

            {/* 3. Data Schema (ERD) */}
            <DataSchemaSpec />

            {/* 4. Security Procedures */}
            <SecurityArchitectureDiagram />

            {/* 5. Information Architecture (Blueprint Wireflow) */}
            <BlueprintArchitecture />

        </Container>
    );
}
