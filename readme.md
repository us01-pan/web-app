## 1. Створення та налаштування CI/CD пайплайна
![image](https://github.com/user-attachments/assets/9e23b0da-6791-4b8a-96ba-ed2d81e12982)

#### Загальний опис
В файлі jenkinsfile  код пайплану, що автоматизує процес створення, тестування та розгортання веб-додатку за допомогою Docker. Ось короткий огляд кожного етапу:
1. **Checkout Code**:
       - Клонує репозиторій з GitHub, використовуючи гілку `main`.
2. **Build Docker Image**:
       - Створює Docker-образ і присвоює ім'я образу, вказане в змінній середовища `DOCKER_IMAGE`.
3. **Run Container**:
       - Запускає Docker-контейнер 
4. **Test Application**:
       - Тестує додаток, надсилаючи HTTP-запит на `localhost:8000`, щоб переконатися, що він працює належним чином.
5. **Push to Docker Registry**:
       - Авторизується в Docker Hub за допомогою збережених у Jenkins облікових даних і пушить створений Docker-образ у Docker-реєстр в приватний репозиторій
6. **Deploy to Production**:
       - Виконується розгортання на продакшн-сервері. Використовуються SSH-ключі для підключення до сервера та виконання команд для оновлення контейнерів через Docker Compose.
7. **Check Production Status**:
       - Перевіряється доступність додатку на продакшн-сервері, відправляючи HTTP-запит на сервер. Якщо відповідь не 200, викликається помилка.
**Post-блок**:
- Після завершення всіх етапів pipeline зупиняє і видаляє контейнер, якщо він був запущений.
### Вставка та налаштування  pipeline:

1. **Створення нової Jenkins job**:
    - Увійдіть в Jenkins.
    - Перейдіть до **Jenkins > New Item**.
    - Введіть ім'я для нового проєкту і виберіть **Pipeline**.
    - Натисніть **OK**.
2. **Налаштування Pipeline**:
       - Відкрийте створену job і перейдіть до вкладки **Pipeline**.
    - Виберіть **Pipeline script** в полі **Definition**.
    - Вставте весь код з файлу jenkinsfile у поле **Pipeline script**.
3. **Конфігурація облікових даних**:
       - Перейдіть до **Jenkins > Manage Jenkins > Manage Credentials**.
    - Додайте облікові дані для SSH (`prodssh`) і Docker Hub (`dockerhub_cred`)
4. **Налаштування змінних середовища** (за необхідності):
     Визначте змінні середовища в розділі **Build Environment**   також в кроці деплою замінити юзера під яким виконується деплой  наприклад `ubuntu`
    ` ssh -o StrictHostKeyChecking=no -i /$SSH_KEY ubuntu@${PROD_SERVER_IP} '`
5. На прод- сервері помістити в папку /opt/pandaweb файл `docker-compose.yml`, приклад `docker-compose.yml` в репозиторії
6. **Запуск pipeline**:
       - Після збереження змін ви можете запустити pipeline, натиснувши **Build Now** на головній сторінці job.

## 2. Налаштування моніторингу

### 1. Встановлення Prometheus та Alertmanager

- Використовуйте файл `docker-compose.yml`, розташований у папці `monitoring/prometheus/docker-compose.yml`, для запуску контейнерів Prometheus та Alertmanager.

- Файл конфігурації Prometheus доступний у папці `/monitoring/prometheus/prometheus.yml`.

> **Примітка**: Файл `prometheus.yml` містить необхідні налаштування для збору метрик та інтеграції з Alertmanager. Потрібно тільеи змінити адрес серверу

---

## 2. Встановлення експортерів Node Exporter і cAdvisor

- Для збору метрик з веб-сервера потрібно встановити експортери приклад можна побачити в файлі `docker-compose.yml`, розташований у папці `/monitoring/docker-compose.yml`.
- Експортери:
       - **Node Exporter** — забезпечує інформацію про стан вузла (CPU, RAM, файлові системи).
       - **cAdvisor** — забезпечує інформацію про контейнери Docker.
        

---

## 3. Налаштування Grafana

### Запуск Grafana

1. Запустіть Grafana 
### Додавання джерела даних Prometheus

1. У меню Grafana натисніть **Configuration → Data Sources → Add data source**.
2. Оберіть **Prometheus**.
3. Вкажіть URL: `http://<IP>:9090`.
### Імпорт готової панелі моніторингу

1. У меню Grafana натисніть **+ → Import**.
2. Вставте JSON-код із файлу `Monitoring dashboard.json`.
3. Натисніть **Load**, щоб завантажити панель.


## 4. Приклади алертів

Приклади конфігурацій алертів для Alertmanager можна знайти в файлі `monitoring/prometheus/alerts.yml`. Файл включає в собі 2 алерта на котроль ОЗУ та CPU і  можливість відправки повідомлень у Telegram. Для цього необхідно створити бота та чат, керуючись інструкціями на сайті: [https://core.telegram.org/bots/tutorial](https://core.telegram.org/bots/tutorial). Після цього потрібно замінити відповідні дані на свої:

- `chat_id: -00000000000`
- `bot_token: "323424234346:AA5656768682343_t_pF2324C9dOKc"`
       
## 5. Приклад візуалізації даних
![image](https://github.com/user-attachments/assets/2c28494b-36f2-43ab-b530-ed42b8b40bd3)

