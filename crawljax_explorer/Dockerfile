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

# Copia o pom.xml e baixa as dependências (isso otimiza o cache do Docker)
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copia o código fonte (que vamos criar em seguida) e compila o projeto
COPY src ./src
RUN mvn clean package -DskipTests

# Define variáveis de ambiente para o Chrome rodar lisinho no Docker
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

# Comando que será executado quando o container subir
CMD ["java", "-jar", "target/crawljax-explorer-1.0-SNAPSHOT-jar-with-dependencies.jar"]