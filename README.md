Cal.com MCP Server (FastAPI)

Overview

This project implements a Model Context Protocol (MCP) server using FastAPI that exposes scheduling tools from Cal.com.

Features

* List event types (real API integration)
* Create booking (simulated)
* Cancel booking (simulated)
* Reschedule booking (simulated)
* MCP-compatible tool schema

Tech Stack

* FastAPI
* Python
* Cal.com API

Endpoints

* GET /tools → List available tools
* POST /tools/list_event_types → Fetch event types
* POST /tools/create_booking → Create booking
* POST /tools/cancel_booking → Cancel booking
* POST /tools/reschedule_booking → Reschedule booking

Notes

* Cal.com API has limitations for booking creation, so booking-related tools are simulated.
* The server is MCP-compatible and can be used by any AI agent.

Run Project

bash
uvicorn app.main:app --reload

