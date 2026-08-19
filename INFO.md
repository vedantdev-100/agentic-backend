                 CLIENT
                    │
                    ▼
              main.py
                    │
                    ▼
              api/chat.py
                    │
                    ▼
          schemas/chat.py
          (validate request)
                    │
                    ▼
        services/chat_service.py
                    │
                    ▼
              graph/builder.py
                    │
                    ▼
              LangGraph
                    │
              ┌─────┴─────┐
              ▼           ▼
          chat_node      tools
              │           │
              │      ┌────┴────┐
              │      ▼         ▼
              │    Local      MCP
              │    Tools      Tools
              │      └────┬────┘
              │           ▼
              │       sanitize
              │           │
              └─────◄─────┘
                    │
                    ▼
                  Groq
                    │
                    ▼
                Response
                    │
                    ▼
              Client receives