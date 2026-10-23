# 🚀 Serverless URL Shortener on AWS (Infraestructura como Código)

Un acortador de URLs nativo de la nube, altamente escalable y de costo cero (FinOps-friendly). Construido completamente con arquitectura Serverless en AWS y aprovisionado automáticamente usando Terraform.

Este proyecto demuestra el ciclo de vida completo del desarrollo de software en la nube: desde un Producto Mínimo Viable (MVP) hasta una arquitectura empresarial desacoplada.

## 🛠️ Tech Stack

*   **Lógica / Backend:** AWS Lambda (Python 3.12)
*   **Base de Datos:** Amazon DynamoDB (NoSQL)
*   **Infraestructura como Código (IaC):** Terraform
*   **API / Red:** AWS Lambda Function URLs
*   **Región:** Desplegado en `eu-west-1` (Irlanda) para optimizar la latencia en Europa y cumplir con normativas de residencia de datos (GDPR).

---

## 🏗️ Evolución de la Arquitectura

El proyecto está estructurado en dos fases para demostrar el proceso de escalado de una aplicación:

### 1. Fase V1: MVP (Costo Cero y Rápida Iteración)
Ubicado en la carpeta `/v1-mvp`.
Diseñado para validar la lógica del negocio con la menor fricción y costo posible. Utiliza **Lambda Function URLs** públicas para evitar los costos fijos de API Gateway, y una tabla de **DynamoDB** bajo demanda.

![Arquitectura V1 MVP](enlace-a-tu-imagen-v1.png) *(Nota: Aquí debes subir una imagen de tu diagrama de Draw.io o Excalidraw)*

### 2. Fase V2: Enterprise-Ready (Próximamente / En desarrollo)
Ubicado en la carpeta `/v2-enterprise`.
Evolución de la arquitectura para soportar tráfico viral y analíticas:
*   **Amazon CloudFront:** Caché perimetral para reducir lecturas en la base de datos ante picos de tráfico.
*   **Amazon API Gateway + AWS WAF:** Rate limiting y protección contra ataques DDoS.
*   **Amazon SQS:** Desacoplamiento asíncrono para ingesta de métricas de uso sin penalizar el tiempo de respuesta del usuario.

---

## 🧠 Decisiones de Diseño (Trade-offs)

*   **¿Por qué DynamoDB y no RDS (SQL)?** Un acortador de URLs requiere búsquedas ultrarrápidas por clave principal (el código corto). DynamoDB ofrece latencias de un solo dígito de milisegundo y se integra perfectamente con el modelo de pago por uso, a diferencia de una base de datos relacional tradicional que requiere un servidor encendido 24/7.
*   **¿Por qué Lambda Function URLs en la V1?** Para un MVP o proyecto de bajo tráfico, API Gateway añade complejidad y posibles costos si se supera la capa gratuita (1 millón de peticiones). Lambda Function URLs permite exponer la API a internet de forma nativa y 100% gratuita.

## 💰 Estrategia FinOps (Control de Costos)

Esta arquitectura está diseñada para mantenerse permanentemente en la **Capa Siempre Gratuita (Always Free)** de AWS:
*   **Cómputo a demanda:** AWS Lambda escala a cero. Si no hay tráfico, el costo es de $0.00.
*   **DynamoDB Pay-Per-Request:** Capacidad de lectura/escritura bajo demanda.
*   **Limpieza Automática (TTL):** Se configuró el atributo `Time To Live (TTL)` en DynamoDB para que los registros caduquen y se borren automáticamente a los 6 meses, evitando pagar por almacenamiento de datos obsoletos sin necesidad de procesos batch adicionales.

---

## 🚀 Guía de Despliegue Rápido (Quick Start)

Cualquier persona con credenciales de AWS puede levantar este proyecto en su cuenta en menos de 2 minutos utilizando Terraform.

### Prerrequisitos
*   AWS CLI configurado (`aws configure`).
*   Terraform instalado.

### Pasos para desplegar
1. Clona el repositorio:
   ```bash
   git clone [https://github.com/](https://github.com/)[TU_USUARIO]/serverless-url-shortener-aws.git
   cd serverless-url-shortener-aws/v1-mvp