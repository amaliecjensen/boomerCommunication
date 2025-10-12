# Email assistent

> En intelligent Gmail email assistent der automatisk filtrerer vigtige emails og sender SMS notifikationer ved hjælp af AI.

## Beskrivelse

Dette projekt er en smart email listener der overvåger din Gmail inbox 24/7 og bruger ChatGPT til at evaluere om indkommende emails er vigtige. Kun når en email vurderes som vigtig, får du en SMS notifikation - så du hurtigt kan blive opmærksom på vigtige mails.

## Features

- **Realtime Gmail overvågning** via Google Cloud Pub/Sub
- **AI-baseret email evaluering** med ChatGPT/OpenAI
- **SMS notifikationer** via Twilio 
- **Vector database** til historisk læring og mønstergenkendelse
- **Spam filtering** - ingen notifikationer for ligegyldige emails

## Arkitektur

```
1. Gmail → Pub/Sub: "Ny email! historyId: 123456"
2. Systemet modtager Pub/Sub notification
3. Gmail API: "Giv mig email indhold for historyId 123456"
4. Gmail API returnerer fuld email data
5. ChatGPT evaluerer email
6. Email gemmes i vector database
7. SMS sendes (hvis vigtig)
```

## Teknologier

- **Python 3.10+**
- **Google Cloud Pub/Sub** - Gmail notifications
- **Gmail API** - Email adgang
- **OpenAI GPT-3.5-turbo** - AI evaluering via LangChain
- **Twilio** - SMS beskeder
- **ChromaDB** - Vector database
- **Sentence Transformers** - Text embeddings

**Lavet med ❤️ af Amalie Jensen**

*Intelligent email filtering for the modern boomer* 🚀