import React, { useCallback, useMemo } from 'react';
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  BackgroundVariant,
  MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';

const initialNodes: Node[] = [
  {
    id: 'agent-1',
    type: 'input',
    position: { x: 100, y: 100 },
    data: { label: 'Orchestrator', agent_id: 'orchestrator', status: 'idle' },
    style: { background: '#e6f7ff', border: '2px solid #1890ff', borderRadius: 8 },
  },
  {
    id: 'agent-2',
    type: 'default',
    position: { x: 350, y: 50 },
    data: { label: 'Research Agent', agent_id: 'research', status: 'idle' },
    style: { background: '#f6ffed', border: '2px solid #52c41a', borderRadius: 8 },
  },
  {
    id: 'agent-3',
    type: 'default',
    position: { x: 350, y: 150 },
    data: { label: 'Analysis Agent', agent_id: 'analysis', status: 'idle' },
    style: { background: '#fff7e6', border: '2px solid #fa8c16', borderRadius: 8 },
  },
  {
    id: 'agent-4',
    type: 'output',
    position: { x: 600, y: 100 },
    data: { label: 'Output Agent', agent_id: 'output', status: 'idle' },
    style: { background: '#f9f0ff', border: '2px solid #722ed1', borderRadius: 8 },
  },
];

const initialEdges: Edge[] = [
  {
    id: 'e1-2',
    source: 'agent-1',
    target: 'agent-2',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: 'e1-3',
    source: 'agent-1',
    target: 'agent-3',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: 'e2-4',
    source: 'agent-2',
    target: 'agent-4',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: 'e3-4',
    source: 'agent-3',
    target: 'agent-4',
    animated: true,
    markerEnd: { type: MarkerType.ArrowClosed },
  },
];

const FlowCanvas: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const proOptions = useMemo(() => ({ hideAttribution: true }), []);

  return (
    <div style={{ width: '100%', height: 500 }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
        proOptions={proOptions}
      >
        <Controls />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
      </ReactFlow>
    </div>
  );
};

export default FlowCanvas;
