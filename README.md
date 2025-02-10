python --version
   ```

2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   # или
   venv\Scripts\activate     # для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install streamlit matplotlib numpy sqlalchemy
   ```

4. Запустите приложение:
   ```bash
   streamlit run main.py
   ```

5. Откройте браузер и перейдите по адресу:
   ```
   http://localhost:5000