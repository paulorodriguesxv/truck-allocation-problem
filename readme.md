
# Truck allocation Problem


It's requires python 3.7.

This cargo x trucks problem belongs to a quadratic assignment problem
category and was solved using hungarian algorithm minimization allocation,
using scipy lib for calculation. The algorithm build steps was documented
at notebook called app_notebook.ipynb.

[pt-BR]
Esse é um problema em que devemos alocar corretamente um caminhão com o 
objetivo de minimizar o valor do frete. Neste exemplo, o problema é resolvido
através do método humgário de minimização de alocação, usando scipy.


# Install

To install dependencies:

```bash
pip install -r requirements.txt
```

## Running

```bash
python /app.py
```

To run tests:
```bash
    python -m pytest -vv -s --cov=. --cov-report xml:coverage/coverage.xml --cov-report term-missing .
```

```bash
    jupyter notebook app_notebook.ipynb
```


Star if you like it.
---------------------

If you like or use this project, consider showing your support by starring it.
