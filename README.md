# SpectrumGrapher
Построитель спектрограм на базе показаний устройств Arinst

## Установка
1. Клонируем репозиторий
```
git clone https://github.com/IlyaDanilenko/SpectrumGrapher.git
```
3. Устанавливаем необходимые библиотеки Python
```
cd SpectrumGrapher
pip install -r requirements.txt
```

## Запуск приложения
```
python main.py --start [начальная частота сканирвоания] --stop [конечная частота сканирования] --step [шаг сканирования]
```