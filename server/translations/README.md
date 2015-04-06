# Translations

## Generate template

`$ pybabel extract -F babel.cfg -o messages.pot .`

## Add a language

`$ pybabel init -i messages.pot -d translations -l it`

## Compile translations

`$ pybabel compile -d translations`
