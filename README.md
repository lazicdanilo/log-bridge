# Log Bridge

Lib for bridging communication and logging between server

Library for communication and logging between server (Raspberry Pi, user PC, etc...) and client (MCU, SoC, etc...).

Example connection between Raspberry Pi and MCU:

```plaintext
┌────────────┐   Interface   ┌─────────────────┐
│     MCU    │    (USART)    │    Raspberry    │
│     App    │◄─────────────►│     Pi App      │
│ (C client) │               │ (Python server) │
└────────────┘               └─────────────────┘
```

## Server

Server is a python script that usually runs on Raspberry Pi or user PC.

## Client

Client is a C program that usually runs on MCU.
