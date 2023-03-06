# PathFinder

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Особенности модуля

* ### Алгоритм `algorithm`
Реализовано два алгоритма поиска
```python
PathFinder({...}, algorithm='A*') # По умолчанию 
PathFinder({...}, algorithm='dijkstra')
```

* ### Графическое отображение `draw`

```python
PathFinder({...}, draw=True) # По умолчанию 
PathFinder({...}, draw=False)
```
