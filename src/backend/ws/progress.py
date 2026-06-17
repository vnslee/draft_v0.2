from __future__ import annotations

import json
from collections import defaultdict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

ws_router = APIRouter()


class ConnectionManager:
    def __init__(self) -> None:
        # analysis_id → list of connected WebSocket
        self._connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, analysis_id: str, ws: WebSocket) -> None:
        await ws.accept()
        self._connections[analysis_id].append(ws)

    def disconnect(self, analysis_id: str, ws: WebSocket) -> None:
        conns = self._connections.get(analysis_id, [])
        if ws in conns:
            conns.remove(ws)

    async def broadcast(self, analysis_id: str, payload: dict) -> None:
        dead: list[WebSocket] = []
        for ws in list(self._connections.get(analysis_id, [])):
            try:
                await ws.send_text(json.dumps(payload, ensure_ascii=False))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(analysis_id, ws)


ws_manager = ConnectionManager()


async def broadcast_progress(
    analysis_id: str,
    agent: str,
    progress: int,
    status: str,
    message: str = "",
) -> None:
    await ws_manager.broadcast(
        analysis_id,
        {
            "type": "progress",
            "agent": agent,
            "progress": progress,
            "status": status,
            "message": message,
        },
    )


async def broadcast_completed(analysis_id: str, result_id: str, verdict: str, total_score: float | None) -> None:
    await ws_manager.broadcast(
        analysis_id,
        {
            "type": "completed",
            "result_id": result_id,
            "verdict": verdict,
            "total_score": total_score,
        },
    )


async def broadcast_error(analysis_id: str, agent: str, message: str, recoverable: bool = True) -> None:
    await ws_manager.broadcast(
        analysis_id,
        {
            "type": "error",
            "agent": agent,
            "message": message,
            "recoverable": recoverable,
        },
    )


@ws_router.websocket("/ws/analysis/{analysis_id}")
async def websocket_endpoint(websocket: WebSocket, analysis_id: str) -> None:
    await ws_manager.connect(analysis_id, websocket)
    try:
        while True:
            # 클라이언트 메시지 대기 (연결 유지 목적)
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(analysis_id, websocket)
