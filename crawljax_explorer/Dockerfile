# Imagem base oficial do Maven com Java 17
FROM maven:3.9-eclipse-temurin-17

# Instala o Chromium, o driver e todas as dependências necessárias para sandbox headless
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libxss1 \
    fonts-liberation \
    libgbm1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Usa cache persistente do Maven para evitar baixar novamente a arvore pesada
# de dependencias do Crawljax a cada alteracao de codigo.
COPY pom.xml .
COPY src ./src
RUN --mount=type=cache,target=/root/.m2 mvn clean package -B

# Define variáveis de ambiente para o Chrome rodar lisinho no Docker
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

# Comando que será executado quando o container subir
CMD ["java", "-jar", "target/crawljax-explorer-1.0-SNAPSHOT-jar-with-dependencies.jar"]
