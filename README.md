# FastAPI CRUD

A lightweight RESTful CRUD service built with FastAPI that manages a collection
of items in memory. The project is packaged as a small, self-contained Python
application designed to be deployed as a Docker container and exposed to the
public internet through a Cloudflare Tunnel.

## Overview

The service exposes a simple `Item` resource identified by a UUID, with a
`name` and a `description` field. Items are validated through Pydantic schemas
and stored in an in-process dictionary, making the application ideal as a
reference implementation, a learning project, or a starting point for a more
feature-rich backend.

The API follows the conventional REST layout:

In addition to the JSON endpoints below, FastAPI automatically exposes an
interactive API documentation surface:

- `GET /docs` — Swagger UI with a full, executable description of every
  endpoint, including request and response schemas.
- `GET /redoc` — ReDoc, an alternative read-only API reference.
- `GET /openapi.json` — the raw OpenAPI 3 schema describing the service.

These are useful for exploring the API, trying out requests from the browser,
and generating client code.

- `POST /items/` — create a new item and return it together with its
  generated identifier.
- `GET /items/` — list every item currently stored.
- `GET /items/{item_id}` — retrieve a single item by its identifier, returning
  a 404 response when it does not exist.
- `PUT /items/{item_id}` — replace an existing item, returning a 404 response
  when the identifier is unknown.
- `DELETE /items/{item_id}` — remove an item from the store, returning a 404
  response when the identifier is unknown.

## Architecture

The application code lives under the `app/` package and is split into a few
focused modules:

- `app/main.py` wires the FastAPI application and defines the HTTP endpoints.
- `app/schemas.py` declares the Pydantic models used for request validation
  and response serialization (`ItemCreate` for inputs and `Item` for fully
  formed resources).
- `app/storage.py` holds the in-memory `Items` dictionary that acts as the
  persistence layer for the service.

## Containerization

The project ships with a multi-service `docker-compose.yml` setup:

- The `app` service builds the application image from the provided
  `Dockerfile`, which is based on `python:3.14.4-alpine3.23` and runs the
  service with Uvicorn on port `8080`.
- The `tunnel` service runs `cloudflared` and connects the local application
  to a Cloudflare Tunnel using a token provided through the
  `CLOUDFLARE_TUNNEL_TOKEN` environment variable, allowing secure public
  access without exposing the container directly.
- The `dagger` service provides an isolated environment for executing the
  Dagger-based pipelines that automate builds and checks.

Both services share a dedicated `cloudflare` bridge network so the tunnel can
reach the application container internally.

## Continuous Integration

A Dagger pipeline under `dagger/` is included to drive build and verification
steps inside a container, keeping the toolchain reproducible and decoupled
from the host machine. This pipeline is meant to be extended into a full
CI/CD workflow.
