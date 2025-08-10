# Agent Communication Protocol Specification

**Status**: Phase 1 Implementation - Task 1.3
**Version**: 1.0
**Author**: Task Graph System Team
**Last Updated**: 2025-08-10

## Overview

This document specifies the standardized communication protocols for agent-to-agent interaction within the AutoDocs MCP Task Graph Workflow System. These protocols enable coordinated multi-agent workflows while maintaining backward compatibility with existing MCP protocol implementation.

## Architecture Overview

### Communication Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Protocol Layer                       │
│  (Existing MCP tools: scan_dependencies, get_package_docs) │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│              Agent Communication Protocol Layer             │
│  (New workflow tools: submit_complex_request, etc.)        │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                Message Routing & Serialization             │
│        (Communication service implementation)              │
└─────────────────────────────────────────────────────────────┘
```

## Core Communication Patterns

### 1. Task Assignment Pattern

**Purpose**: Orchestrator assigns tasks to specialized agents
**Direction**: Orchestrator → Specialized Agent
**Message Type**: `TASK_ASSIGNMENT`

```json
{
  "message_type": "TASK_ASSIGNMENT",
  "message_id": "task_001_assign",
  "source_agent": "workflow_orchestrator",
  "target_agent": "core_services",
  "timestamp": "2025-08-10T10:30:00Z",
  "task": {
    "task_id": "task_001",
    "task_type": "dependency_analysis",
    "priority": "high",
    "parameters": {
      "package_name": "fastapi",
      "version_constraint": ">=0.68.0",
      "context_scope": "runtime"
    },
    "dependencies": ["task_000"],
    "expected_output": "PackageDependencyContext",
    "timeout_seconds": 60
  },
  "workflow_context": {
    "workflow_id": "wf_12345",
    "user_request": "Analyze FastAPI ecosystem for project integration",
    "context_budget": 50000,
    "quality_requirements": ["validation", "completeness"]
  }
}
```

### 2. Progress Reporting Pattern

**Purpose**: Agents report task progress to orchestrator
**Direction**: Specialized Agent → Orchestrator
**Message Type**: `PROGRESS_REPORT`

```json
{
  "message_type": "PROGRESS_REPORT",
  "message_id": "task_001_progress",
  "source_agent": "core_services",
  "target_agent": "workflow_orchestrator",
  "timestamp": "2025-08-10T10:31:30Z",
  "task_id": "task_001",
  "status": "in_progress",
  "progress_percentage": 65,
  "intermediate_results": {
    "discovered_dependencies": 12,
    "analyzed_packages": 8,
    "estimated_completion": "2025-08-10T10:32:15Z"
  },
  "metrics": {
    "cache_hits": 6,
    "cache_misses": 2,
    "api_calls": 2,
    "token_usage": 1250
  },
  "issues": []
}
```

### 3. Task Completion Pattern

**Purpose**: Agents deliver final results to orchestrator
**Direction**: Specialized Agent → Orchestrator
**Message Type**: `TASK_COMPLETION`

```json
{
  "message_type": "TASK_COMPLETION",
  "message_id": "task_001_complete",
  "source_agent": "core_services",
  "target_agent": "workflow_orchestrator",
  "timestamp": "2025-08-10T10:32:10Z",
  "task_id": "task_001",
  "status": "completed",
  "execution_time_seconds": 95,
  "result": {
    "primary_package": {
      "name": "fastapi",
      "version": "0.104.1",
      "documentation": "...",
      "dependencies": [...]
    },
    "runtime_dependencies": [...],
    "context_metadata": {
      "token_count": 2450,
      "quality_score": 0.95
    }
  },
  "performance_metrics": {
    "cache_hit_rate": 0.75,
    "api_response_time_avg": 120,
    "total_token_usage": 2450
  },
  "quality_validation": {
    "validation_passed": true,
    "completeness_score": 0.98,
    "accuracy_indicators": {...}
  }
}
```

### 4. Agent Collaboration Pattern

**Purpose**: Agents coordinate directly for complex tasks
**Direction**: Bidirectional between Specialized Agents
**Message Type**: `COLLABORATION_REQUEST`

```json
{
  "message_type": "COLLABORATION_REQUEST",
  "message_id": "collab_001",
  "source_agent": "core_services",
  "target_agent": "testing_specialist",
  "timestamp": "2025-08-10T10:33:00Z",
  "collaboration_type": "validation_request",
  "context": {
    "workflow_id": "wf_12345",
    "requesting_task_id": "task_001",
    "shared_context": {
      "package_analysis": {...},
      "quality_requirements": [...]
    }
  },
  "request": {
    "validation_type": "dependency_compatibility",
    "target_data": {...},
    "validation_criteria": [...],
    "urgency": "normal"
  }
}
```

### 5. Error Handling Pattern

**Purpose**: Report and coordinate error recovery
**Direction**: Any Agent → Orchestrator
**Message Type**: `ERROR_REPORT`

```json
{
  "message_type": "ERROR_REPORT",
  "message_id": "error_001",
  "source_agent": "core_services",
  "target_agent": "workflow_orchestrator",
  "timestamp": "2025-08-10T10:35:00Z",
  "task_id": "task_002",
  "error": {
    "error_type": "NetworkTimeout",
    "error_code": "NET_001",
    "message": "PyPI API request timed out",
    "recoverable": true,
    "suggested_action": "retry_with_backoff",
    "context": {
      "package_name": "requests",
      "attempt_number": 2,
      "timeout_duration": 30
    }
  },
  "recovery_options": [
    {
      "option": "retry_task",
      "probability_success": 0.85,
      "estimated_delay": 15
    },
    {
      "option": "fallback_cached",
      "probability_success": 0.95,
      "quality_impact": "minor"
    }
  ]
}
```

## Message Serialization and Validation

### Message Schema Structure

All agent communication messages follow this base schema:

```python
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    TASK_ASSIGNMENT = "TASK_ASSIGNMENT"
    PROGRESS_REPORT = "PROGRESS_REPORT"
    TASK_COMPLETION = "TASK_COMPLETION"
    COLLABORATION_REQUEST = "COLLABORATION_REQUEST"
    COLLABORATION_RESPONSE = "COLLABORATION_RESPONSE"
    ERROR_REPORT = "ERROR_REPORT"
    CONTEXT_SYNC = "CONTEXT_SYNC"
    WORKFLOW_STATUS = "WORKFLOW_STATUS"

class AgentMessage(BaseModel):
    """Base message for agent-to-agent communication."""
    message_type: MessageType
    message_id: str = Field(..., description="Unique message identifier")
    source_agent: str = Field(..., description="Sending agent identifier")
    target_agent: str = Field(..., description="Target agent identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = Field(None, description="For message threading")
    priority: str = Field(default="normal", description="Message priority level")
    payload: Dict[str, Any] = Field(..., description="Message-specific data")
```

### Message Routing Rules

1. **Direct Agent Communication**
   - Messages between specialized agents route directly
   - No orchestrator intervention required
   - Used for collaboration and validation requests

2. **Orchestrator-Mediated Communication**
   - Task assignments and completions always go through orchestrator
   - Progress reports always go to orchestrator
   - Error reports typically go to orchestrator unless agent-specific

3. **Broadcast Communication**
   - Context synchronization messages broadcast to relevant agents
   - Workflow status updates broadcast to all participating agents
   - System notifications broadcast as needed

### Message Persistence and Reliability

```python
class MessageDelivery(BaseModel):
    """Message delivery tracking and reliability."""
    message_id: str
    attempts: int = 0
    max_attempts: int = 3
    delivery_status: str = "pending"  # pending, delivered, failed, expired
    created_at: datetime
    delivered_at: Optional[datetime] = None
    error_details: Optional[str] = None

    def should_retry(self) -> bool:
        return self.attempts < self.max_attempts and self.delivery_status == "pending"
```

## Communication Service Implementation

### Core Service Architecture

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
import asyncio
import json
from datetime import datetime, timedelta

class CommunicationService(ABC):
    """Abstract base for agent communication service."""

    @abstractmethod
    async def send_message(self, message: AgentMessage) -> bool:
        """Send message to target agent."""
        pass

    @abstractmethod
    async def register_handler(self, message_type: MessageType, handler: Callable) -> None:
        """Register message handler for specific message type."""
        pass

    @abstractmethod
    async def start_listening(self) -> None:
        """Start listening for incoming messages."""
        pass

    @abstractmethod
    async def stop_listening(self) -> None:
        """Stop listening and cleanup resources."""
        pass

class InProcessCommunicationService(CommunicationService):
    """In-process message routing for single-process deployment."""

    def __init__(self):
        self.message_handlers: Dict[str, Dict[MessageType, Callable]] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.delivery_tracking: Dict[str, MessageDelivery] = {}
        self.running = False

    async def send_message(self, message: AgentMessage) -> bool:
        """Route message to target agent handler."""
        delivery = MessageDelivery(
            message_id=message.message_id,
            created_at=datetime.utcnow()
        )
        self.delivery_tracking[message.message_id] = delivery

        try:
            target_handlers = self.message_handlers.get(message.target_agent, {})
            handler = target_handlers.get(message.message_type)

            if handler:
                await self.message_queue.put((handler, message))
                delivery.delivery_status = "delivered"
                delivery.delivered_at = datetime.utcnow()
                return True
            else:
                delivery.delivery_status = "failed"
                delivery.error_details = f"No handler for {message.message_type} on {message.target_agent}"
                return False

        except Exception as e:
            delivery.attempts += 1
            delivery.error_details = str(e)

            if delivery.should_retry():
                # Schedule retry
                asyncio.create_task(self._retry_message(message, delivery))
            else:
                delivery.delivery_status = "failed"

            return False

    async def register_handler(self, agent_id: str, message_type: MessageType, handler: Callable) -> None:
        """Register message handler for agent and message type."""
        if agent_id not in self.message_handlers:
            self.message_handlers[agent_id] = {}
        self.message_handlers[agent_id][message_type] = handler

    async def start_listening(self) -> None:
        """Start processing message queue."""
        self.running = True
        asyncio.create_task(self._process_messages())

    async def stop_listening(self) -> None:
        """Stop processing and cleanup."""
        self.running = False

    async def _process_messages(self) -> None:
        """Process messages from queue."""
        while self.running:
            try:
                handler, message = await asyncio.wait_for(
                    self.message_queue.get(), timeout=1.0
                )
                await handler(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                # Log error but continue processing
                print(f"Error processing message: {e}")

    async def _retry_message(self, message: AgentMessage, delivery: MessageDelivery) -> None:
        """Retry failed message delivery."""
        await asyncio.sleep(2 ** delivery.attempts)  # Exponential backoff
        await self.send_message(message)
```

## MCP Tool Extensions

### New MCP Tools for Workflow Operations

#### 1. submit_complex_request

```python
@mcp.tool
async def submit_complex_request(
    request_description: str,
    context_scope: str = "smart",
    priority: str = "normal",
    quality_requirements: List[str] = None
) -> Dict[str, Any]:
    """
    Submit a complex request for multi-agent workflow processing.

    Args:
        request_description: Natural language description of the complex task
        context_scope: Scope for dependency context ("primary_only", "runtime", "smart")
        priority: Request priority ("low", "normal", "high", "urgent")
        quality_requirements: List of quality requirements ("validation", "completeness", "accuracy")

    Returns:
        Workflow execution details and tracking information
    """
    if communication_service is None or workflow_orchestrator is None:
        return {
            "success": False,
            "error": {
                "code": "workflow_not_initialized",
                "message": "Workflow orchestration not available",
                "suggestion": "System may be starting up or in maintenance mode"
            }
        }

    try:
        # Create workflow request
        workflow_request = ComplexWorkflowRequest(
            description=request_description,
            context_scope=context_scope,
            priority=priority,
            quality_requirements=quality_requirements or ["validation"],
            submitted_at=datetime.utcnow()
        )

        # Submit to orchestrator
        workflow_id = await workflow_orchestrator.submit_request(workflow_request)

        return {
            "success": True,
            "workflow_id": workflow_id,
            "status": "submitted",
            "estimated_completion": "calculating",
            "tracking_url": f"/workflow/{workflow_id}/status"
        }

    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "workflow_submission_failed",
                "message": str(e),
                "suggestion": "Check request parameters and try again"
            }
        }
```

#### 2. get_workflow_status

```python
@mcp.tool
async def get_workflow_status(workflow_id: str) -> Dict[str, Any]:
    """
    Get detailed status of a workflow execution.

    Args:
        workflow_id: Unique identifier for the workflow

    Returns:
        Comprehensive workflow status and progress information
    """
    if workflow_orchestrator is None:
        return {
            "success": False,
            "error": {
                "code": "workflow_not_initialized",
                "message": "Workflow orchestration not available"
            }
        }

    try:
        status = await workflow_orchestrator.get_workflow_status(workflow_id)

        return {
            "success": True,
            "workflow_id": workflow_id,
            "status": status.status,
            "progress_percentage": status.progress_percentage,
            "current_phase": status.current_phase,
            "active_tasks": status.active_tasks,
            "completed_tasks": status.completed_tasks,
            "failed_tasks": status.failed_tasks,
            "estimated_completion": status.estimated_completion,
            "performance_metrics": status.performance_metrics,
            "intermediate_results": status.intermediate_results
        }

    except WorkflowNotFound:
        return {
            "success": False,
            "error": {
                "code": "workflow_not_found",
                "message": f"Workflow {workflow_id} not found",
                "suggestion": "Check workflow ID and ensure it exists"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "status_retrieval_failed",
                "message": str(e)
            }
        }
```

#### 3. agent_collaboration_request

```python
@mcp.tool
async def agent_collaboration_request(
    source_agent: str,
    target_agent: str,
    collaboration_type: str,
    request_data: Dict[str, Any],
    timeout_seconds: int = 60
) -> Dict[str, Any]:
    """
    Request direct collaboration between agents.

    Args:
        source_agent: Agent making the collaboration request
        target_agent: Agent being requested to collaborate
        collaboration_type: Type of collaboration ("validation", "enhancement", "review")
        request_data: Collaboration-specific data and parameters
        timeout_seconds: Maximum time to wait for collaboration response

    Returns:
        Collaboration response and results
    """
    if communication_service is None:
        return {
            "success": False,
            "error": {
                "code": "communication_not_initialized",
                "message": "Agent communication not available"
            }
        }

    try:
        # Create collaboration message
        collaboration_message = AgentMessage(
            message_type=MessageType.COLLABORATION_REQUEST,
            message_id=f"collab_{datetime.utcnow().timestamp()}",
            source_agent=source_agent,
            target_agent=target_agent,
            payload={
                "collaboration_type": collaboration_type,
                "request_data": request_data,
                "timeout_seconds": timeout_seconds
            }
        )

        # Send collaboration request
        success = await communication_service.send_message(collaboration_message)

        if success:
            # Wait for response
            response = await communication_service.wait_for_response(
                collaboration_message.message_id,
                timeout_seconds=timeout_seconds
            )

            return {
                "success": True,
                "collaboration_id": collaboration_message.message_id,
                "response": response,
                "collaboration_type": collaboration_type
            }
        else:
            return {
                "success": False,
                "error": {
                    "code": "collaboration_delivery_failed",
                    "message": "Failed to deliver collaboration request",
                    "suggestion": "Check target agent availability"
                }
            }

    except asyncio.TimeoutError:
        return {
            "success": False,
            "error": {
                "code": "collaboration_timeout",
                "message": f"Collaboration timed out after {timeout_seconds} seconds",
                "suggestion": "Try with longer timeout or check target agent status"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "collaboration_failed",
                "message": str(e)
            }
        }
```

## Quality Assurance and Validation

### Message Validation

```python
class MessageValidator:
    """Validates agent communication messages."""

    @staticmethod
    def validate_message(message: AgentMessage) -> List[str]:
        """Validate message structure and content."""
        errors = []

        # Required field validation
        if not message.message_id:
            errors.append("message_id is required")
        if not message.source_agent:
            errors.append("source_agent is required")
        if not message.target_agent:
            errors.append("target_agent is required")

        # Agent ID validation
        valid_agents = {
            "workflow_orchestrator", "context_coordinator", "core_services",
            "testing_specialist", "production_ops", "docs_integration",
            "mcp_protocol", "technical_writer", "product_manager",
            "agent_design_architect"
        }

        if message.source_agent not in valid_agents:
            errors.append(f"Invalid source_agent: {message.source_agent}")
        if message.target_agent not in valid_agents:
            errors.append(f"Invalid target_agent: {message.target_agent}")

        # Message type specific validation
        if message.message_type == MessageType.TASK_ASSIGNMENT:
            if "task" not in message.payload:
                errors.append("TASK_ASSIGNMENT requires task in payload")
        elif message.message_type == MessageType.PROGRESS_REPORT:
            if "task_id" not in message.payload:
                errors.append("PROGRESS_REPORT requires task_id in payload")

        return errors
```

### Protocol Compatibility

```python
class ProtocolCompatibility:
    """Ensures backward compatibility with existing MCP protocol."""

    @staticmethod
    def wrap_legacy_tool(tool_name: str, tool_function: Callable) -> Callable:
        """Wrap existing MCP tool to work with workflow system."""
        async def wrapped_tool(*args, **kwargs):
            # Execute original tool
            result = await tool_function(*args, **kwargs)

            # Add workflow compatibility metadata
            if isinstance(result, dict) and result.get("success"):
                result["workflow_compatible"] = True
                result["agent_source"] = "legacy_mcp_tool"
                result["communication_protocol"] = "mcp_direct"

            return result

        return wrapped_tool

    @staticmethod
    def ensure_backward_compatibility(workflow_result: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure workflow results are compatible with existing clients."""
        # Maintain existing response structure
        if "context" in workflow_result:
            # Transform workflow context to legacy format
            workflow_result["data"] = workflow_result.get("context", {})

        # Preserve success/error structure
        if "workflow_status" in workflow_result:
            workflow_result["success"] = workflow_result["workflow_status"] == "completed"

        return workflow_result
```

## Integration with Existing MCP Server

### Server Extension Points

```python
# In main.py - Service initialization
async def initialize_communication_services() -> None:
    """Initialize agent communication services alongside existing services."""
    global communication_service, workflow_orchestrator

    # Initialize communication service
    communication_service = InProcessCommunicationService()
    await communication_service.start_listening()

    # Initialize workflow orchestrator
    workflow_orchestrator = WorkflowOrchestrator(communication_service)

    # Register message handlers for existing agents
    await register_agent_handlers()

    logger.info("Agent communication services initialized")

async def register_agent_handlers() -> None:
    """Register message handlers for all agent types."""
    # Core services agent handlers
    await communication_service.register_handler(
        "core_services",
        MessageType.TASK_ASSIGNMENT,
        handle_core_services_task
    )

    # Testing specialist handlers
    await communication_service.register_handler(
        "testing_specialist",
        MessageType.COLLABORATION_REQUEST,
        handle_testing_collaboration
    )

    # Additional agent handlers...
```

### Error Handling Integration

```python
def integrate_workflow_errors_with_existing_error_handling():
    """Integrate workflow errors with existing AutoDocs error handling."""

    # Extend existing ErrorFormatter
    class WorkflowErrorFormatter(ErrorFormatter):
        @classmethod
        def format_workflow_error(cls, error: Exception, workflow_context: Dict[str, Any]) -> Dict[str, Any]:
            base_error = cls.format_exception(error, workflow_context)

            # Add workflow-specific error context
            base_error.update({
                "workflow_id": workflow_context.get("workflow_id"),
                "failed_task": workflow_context.get("failed_task"),
                "agent_involved": workflow_context.get("agent_involved"),
                "recovery_options": cls._get_workflow_recovery_options(error, workflow_context)
            })

            return base_error
```

## Security and Authentication

### Message Security

```python
class SecureMessageTransport:
    """Secure transport for agent messages."""

    def __init__(self, encryption_key: Optional[str] = None):
        self.encryption_enabled = encryption_key is not None
        self.encryption_key = encryption_key

    def encrypt_message(self, message: AgentMessage) -> str:
        """Encrypt sensitive message content."""
        if not self.encryption_enabled:
            return message.json()

        # Implement encryption for sensitive payloads
        # (Implementation depends on security requirements)
        return message.json()  # Placeholder

    def decrypt_message(self, encrypted_data: str) -> AgentMessage:
        """Decrypt message content."""
        if not self.encryption_enabled:
            return AgentMessage.parse_raw(encrypted_data)

        # Implement decryption
        return AgentMessage.parse_raw(encrypted_data)  # Placeholder
```

### Agent Authentication

```python
class AgentAuthenticator:
    """Authenticate agent communications."""

    def __init__(self):
        self.trusted_agents = {
            "workflow_orchestrator": {"permissions": ["all"]},
            "context_coordinator": {"permissions": ["context_management"]},
            "core_services": {"permissions": ["task_execution", "api_access"]},
            # ... other agents
        }

    def authenticate_message(self, message: AgentMessage) -> bool:
        """Verify message authenticity."""
        source_agent = message.source_agent

        # Check if agent is trusted
        if source_agent not in self.trusted_agents:
            return False

        # Verify message signature (if implemented)
        # return self._verify_signature(message)

        return True

    def authorize_message(self, message: AgentMessage) -> bool:
        """Authorize message based on agent permissions."""
        source_agent = message.source_agent
        agent_config = self.trusted_agents.get(source_agent, {})
        permissions = agent_config.get("permissions", [])

        # Check if agent has permission for message type
        required_permission = self._get_required_permission(message.message_type)

        return "all" in permissions or required_permission in permissions

    def _get_required_permission(self, message_type: MessageType) -> str:
        """Get required permission for message type."""
        permission_map = {
            MessageType.TASK_ASSIGNMENT: "task_management",
            MessageType.PROGRESS_REPORT: "progress_reporting",
            MessageType.COLLABORATION_REQUEST: "agent_collaboration",
            MessageType.ERROR_REPORT: "error_reporting"
        }
        return permission_map.get(message_type, "unknown")
```

## Performance Considerations

### Message Throughput Optimization

```python
class PerformanceOptimizedCommunication(InProcessCommunicationService):
    """Performance optimized version of communication service."""

    def __init__(self, batch_size: int = 10, batch_timeout: float = 0.1):
        super().__init__()
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.message_batch: List[Tuple[Callable, AgentMessage]] = []

    async def _process_messages(self) -> None:
        """Process messages in batches for better throughput."""
        while self.running:
            # Collect batch of messages
            batch_start = asyncio.get_event_loop().time()

            while (len(self.message_batch) < self.batch_size and
                   (asyncio.get_event_loop().time() - batch_start) < self.batch_timeout):
                try:
                    handler, message = await asyncio.wait_for(
                        self.message_queue.get(),
                        timeout=self.batch_timeout
                    )
                    self.message_batch.append((handler, message))
                except asyncio.TimeoutError:
                    break

            # Process batch concurrently
            if self.message_batch:
                tasks = [
                    asyncio.create_task(handler(message))
                    for handler, message in self.message_batch
                ]
                await asyncio.gather(*tasks, return_exceptions=True)
                self.message_batch.clear()
```

### Memory Management

```python
class MessageMemoryManager:
    """Manage memory usage for message storage and tracking."""

    def __init__(self, max_messages: int = 10000, cleanup_interval: int = 300):
        self.max_messages = max_messages
        self.cleanup_interval = cleanup_interval
        self.message_history: Dict[str, Tuple[datetime, AgentMessage]] = {}
        self._start_cleanup_task()

    def store_message(self, message: AgentMessage) -> None:
        """Store message with automatic cleanup."""
        if len(self.message_history) >= self.max_messages:
            self._cleanup_old_messages()

        self.message_history[message.message_id] = (datetime.utcnow(), message)

    def _cleanup_old_messages(self) -> None:
        """Remove old messages to free memory."""
        cutoff_time = datetime.utcnow() - timedelta(seconds=self.cleanup_interval)

        messages_to_remove = [
            msg_id for msg_id, (timestamp, _) in self.message_history.items()
            if timestamp < cutoff_time
        ]

        for msg_id in messages_to_remove:
            del self.message_history[msg_id]

    def _start_cleanup_task(self) -> None:
        """Start periodic cleanup task."""
        asyncio.create_task(self._periodic_cleanup())

    async def _periodic_cleanup(self) -> None:
        """Periodic cleanup of old messages."""
        while True:
            await asyncio.sleep(self.cleanup_interval)
            self._cleanup_old_messages()
```

## Testing and Validation

### Communication Protocol Testing

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

class TestAgentCommunication:
    """Test suite for agent communication protocols."""

    @pytest.fixture
    async def communication_service(self):
        service = InProcessCommunicationService()
        await service.start_listening()
        yield service
        await service.stop_listening()

    @pytest.mark.asyncio
    async def test_task_assignment_flow(self, communication_service):
        """Test complete task assignment and completion flow."""
        # Setup mock handlers
        task_handler = AsyncMock()
        await communication_service.register_handler(
            "core_services",
            MessageType.TASK_ASSIGNMENT,
            task_handler
        )

        # Create task assignment message
        task_message = AgentMessage(
            message_type=MessageType.TASK_ASSIGNMENT,
            message_id="test_task_001",
            source_agent="workflow_orchestrator",
            target_agent="core_services",
            payload={
                "task": {
                    "task_id": "test_task_001",
                    "task_type": "dependency_analysis",
                    "parameters": {"package_name": "requests"}
                }
            }
        )

        # Send message
        success = await communication_service.send_message(task_message)
        assert success

        # Verify handler was called
        await asyncio.sleep(0.1)  # Allow message processing
        task_handler.assert_called_once()

        # Verify message content
        called_message = task_handler.call_args[0][0]
        assert called_message.message_type == MessageType.TASK_ASSIGNMENT
        assert called_message.payload["task"]["task_id"] == "test_task_001"

    @pytest.mark.asyncio
    async def test_collaboration_pattern(self, communication_service):
        """Test agent-to-agent collaboration pattern."""
        # Setup handlers for both agents
        validation_handler = AsyncMock()
        await communication_service.register_handler(
            "testing_specialist",
            MessageType.COLLABORATION_REQUEST,
            validation_handler
        )

        # Create collaboration request
        collab_message = AgentMessage(
            message_type=MessageType.COLLABORATION_REQUEST,
            message_id="collab_001",
            source_agent="core_services",
            target_agent="testing_specialist",
            payload={
                "collaboration_type": "validation_request",
                "request_data": {"package_analysis": {...}}
            }
        )

        # Send collaboration request
        success = await communication_service.send_message(collab_message)
        assert success

        # Verify handler was called
        await asyncio.sleep(0.1)
        validation_handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_message_validation(self):
        """Test message validation functionality."""
        # Valid message
        valid_message = AgentMessage(
            message_type=MessageType.TASK_ASSIGNMENT,
            message_id="valid_001",
            source_agent="workflow_orchestrator",
            target_agent="core_services",
            payload={"task": {"task_id": "test"}}
        )

        errors = MessageValidator.validate_message(valid_message)
        assert len(errors) == 0

        # Invalid message - missing required field
        invalid_message = AgentMessage(
            message_type=MessageType.TASK_ASSIGNMENT,
            message_id="",  # Empty message ID
            source_agent="workflow_orchestrator",
            target_agent="core_services",
            payload={}
        )

        errors = MessageValidator.validate_message(invalid_message)
        assert len(errors) > 0
        assert any("message_id is required" in error for error in errors)

    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self, communication_service):
        """Test error handling and message recovery."""
        # Setup handler that raises an exception
        failing_handler = AsyncMock(side_effect=Exception("Handler failed"))
        await communication_service.register_handler(
            "core_services",
            MessageType.TASK_ASSIGNMENT,
            failing_handler
        )

        # Create message
        message = AgentMessage(
            message_type=MessageType.TASK_ASSIGNMENT,
            message_id="failing_task_001",
            source_agent="workflow_orchestrator",
            target_agent="core_services",
            payload={"task": {"task_id": "failing_task"}}
        )

        # Send message
        success = await communication_service.send_message(message)

        # Should initially fail but have retry tracking
        delivery = communication_service.delivery_tracking.get(message.message_id)
        assert delivery is not None
        assert delivery.attempts > 0
```

## Documentation and Examples

### Usage Examples

```python
# Example 1: Simple task assignment
async def assign_documentation_task():
    """Example of assigning a documentation task to an agent."""
    message = AgentMessage(
        message_type=MessageType.TASK_ASSIGNMENT,
        message_id="doc_task_001",
        source_agent="workflow_orchestrator",
        target_agent="core_services",
        payload={
            "task": {
                "task_id": "doc_task_001",
                "task_type": "get_package_docs_with_context",
                "parameters": {
                    "package_name": "fastapi",
                    "version_constraint": ">=0.68.0",
                    "include_dependencies": True,
                    "context_scope": "smart"
                }
            }
        }
    )

    await communication_service.send_message(message)

# Example 2: Agent collaboration for validation
async def request_validation_collaboration():
    """Example of requesting validation collaboration between agents."""
    message = AgentMessage(
        message_type=MessageType.COLLABORATION_REQUEST,
        message_id="validation_collab_001",
        source_agent="core_services",
        target_agent="testing_specialist",
        payload={
            "collaboration_type": "dependency_validation",
            "request_data": {
                "package_analysis": {...},
                "validation_criteria": ["compatibility", "security", "performance"]
            }
        }
    )

    await communication_service.send_message(message)

# Example 3: Progress reporting
async def report_task_progress():
    """Example of reporting task progress to orchestrator."""
    message = AgentMessage(
        message_type=MessageType.PROGRESS_REPORT,
        message_id="progress_001",
        source_agent="core_services",
        target_agent="workflow_orchestrator",
        payload={
            "task_id": "doc_task_001",
            "status": "in_progress",
            "progress_percentage": 65,
            "intermediate_results": {
                "packages_analyzed": 5,
                "dependencies_resolved": 12
            }
        }
    )

    await communication_service.send_message(message)
```

## Future Enhancements

### Planned Protocol Extensions

1. **Stream Processing Support**
   - Support for streaming large datasets between agents
   - Incremental result delivery for long-running tasks
   - Real-time progress updates

2. **Advanced Routing**
   - Load balancing across multiple instances of the same agent type
   - Geographic routing for distributed deployments
   - Priority-based message queuing

3. **Enhanced Security**
   - Message encryption for sensitive data
   - Digital signatures for message authentication
   - Role-based access control for message types

4. **Performance Optimizations**
   - Message compression for large payloads
   - Connection pooling for external communications
   - Adaptive batching based on system load

5. **Monitoring and Observability**
   - Detailed message flow tracing
   - Performance metrics collection
   - Anomaly detection in communication patterns

## Conclusion

This Agent Communication Protocol Framework provides a robust, scalable foundation for multi-agent coordination within the AutoDocs MCP Task Graph Workflow System. The protocol maintains backward compatibility with existing MCP tools while enabling sophisticated agent-to-agent collaboration patterns.

Key benefits of this implementation:

1. **Standardized Communication**: Consistent message formats across all agent interactions
2. **Backward Compatibility**: Existing MCP tools continue to work without modification
3. **Extensible Architecture**: New message types and agents can be easily added
4. **Robust Error Handling**: Comprehensive error detection and recovery mechanisms
5. **Performance Optimized**: Efficient message routing and processing
6. **Security Aware**: Authentication and authorization for agent communications

The protocol supports both simple point-to-point communication and complex multi-agent workflows, providing the foundation for emergent intelligence through coordinated agent collaboration.
